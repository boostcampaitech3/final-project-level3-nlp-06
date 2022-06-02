import os
import pickle
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import DataCollatorForLanguageModeling, PreTrainedTokenizer
from transformers.utils.logging import *
from datasets import load_metric

from torch.utils.data import Dataset
from typing import List, Optional
from filelock import FileLock
import time
import random
from tqdm import tqdm

logger = get_logger(__name__)

## 네트워크 저장하기
def save(ckpt_dir, net, optim, epoch):
    if not os.path.exists(ckpt_dir):
        os.makedirs(ckpt_dir)

    torch.save({'net': net.state_dict(), 'optim': optim.state_dict()},
               "%s/model_epoch%d.pth" % (ckpt_dir, epoch))

## 네트워크 불러오기
def load(ckpt_dir, net, optim):
    if not os.path.exists(ckpt_dir):
        epoch = 0
        return net, optim, epoch

    ckpt_lst = os.listdir(ckpt_dir)
    ckpt_lst.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    dict_model = torch.load('%s/%s' % (ckpt_dir, ckpt_lst[-1]))

    net.load_state_dict(dict_model['net'])
    optim.load_state_dict(dict_model['optim'])
    epoch = int(ckpt_lst[-1].split('epoch')[1].split('.pth')[0])

    return net, optim, epoch

# def load_dataset(directory_path, tokenizer, block_size=128):
#     dataset = TextDataset(
#         tokenizer=tokenizer,
#         directory_path=directory_path,
#         block_size=block_size
#     )
#     return dataset

def load_dataset(dir_path, test_size=0.2):
    if os.path.isdir(dir_path) is False:
            raise ValueError(f"Input directory path {dir_path} not found")

    if test_size >= 1:
        raise ValueError(f"Input test_size {test_size} is Invalid")

    file_list = []
    for (root, _, files) in os.walk(dir_path):
        for file in files:
            if '.txt' in file:
                file_path = os.path.join(root, file)
                file_list += [file_path]

    random.shuffle(file_list)
    N = int(len(file_list) * (1 - test_size))
    train_dataset, eval_dataset = file_list[:N], file_list[N:]

    return train_dataset, eval_dataset


def load_data_collator(tokenizer, mlm=False):
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=mlm
    )
    return data_collator

## 디렉토리에 있는 텍스트 파일을 모두 읽고 ids 값 반환 (파일의 마지막은 padding 처리)
class TextDataset(Dataset):
    def __init__(
        self,
        tokenizer: PreTrainedTokenizer,
        file_list: List,
        block_size: int = 128,
        overwrite_cache=False,
        cache_dir: Optional[str] = None,
        train: bool = False,
    ):
        
        block_size = block_size - tokenizer.num_special_tokens_to_add(pair=False)
        directory, cache_filename = 'datasets', 'cache'

        cached_features_file = None
        if train:
            cached_features_file = os.path.join(
                cache_dir if cache_dir is not None else directory,
                f"cached_lm_{tokenizer.__class__.__name__}_{block_size}_{cache_filename}_train_{len(file_list)}",
            )
        else:
            cached_features_file = os.path.join(
                cache_dir if cache_dir is not None else directory,
                f"cached_lm_{tokenizer.__class__.__name__}_{block_size}_{cache_filename}_test_{len(file_list)}",
            )

        # Make sure only the first process in distributed training processes the dataset,
        # and the others will use the cache.
        lock_path = cached_features_file + ".lock"
        with FileLock(lock_path):

            if os.path.exists(cached_features_file) and not overwrite_cache:
                start = time.time()
                with open(cached_features_file, "rb") as handle:
                    self.examples = pickle.load(handle)
                logger.info(
                    f"Loading features from cached file {cached_features_file} [took %.3f s]", time.time() - start
                )

            else:
                logger.info(f"Creating features from dataset file at {directory}")

                self.examples = []

                for file in file_list:
                    file_path = file
                    with open(file_path, encoding="utf-8") as f:
                        text = f.read()

                    tokenized_text = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(text))

                    for i in range(0, len(tokenized_text) - block_size + 1, block_size):  # Truncate in block of block_size
                        self.examples.append(
                            tokenizer.build_inputs_with_special_tokens(tokenized_text[i : i + block_size])
                        )

                    ## 마지막 sentence에 패딩 추가
                    idx = block_size * int(len(tokenized_text) / block_size)
                    self.examples.append(
                        tokenizer.build_inputs_with_special_tokens(
                            tokenized_text[idx: len(tokenized_text)],
                            [tokenizer.convert_tokens_to_ids(tokenizer.pad_token)] * (block_size - (len(tokenized_text) - idx + 1))
                        )
                    )

                start = time.time()
                with open(cached_features_file, "wb") as handle:
                    pickle.dump(self.examples, handle, protocol=pickle.HIGHEST_PROTOCOL)
                logger.info(
                    f"Saving features into cached file {cached_features_file} [took {time.time() - start:.3f} s]"
                )

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i) -> torch.Tensor:
        return torch.tensor(self.examples[i], dtype=torch.long)

def perplexity(model, generated_sentence, stride=16):
    max_length = model.config.n_positions
    print('max_length : ', max_length)
    print('generated_sentence : ', len(generated_sentence))
    nlls = []
    for i in tqdm(range(0, len(generated_sentence), stride)):
        begin_loc = max(i + stride - max_length, 0)
        end_loc = min(i + stride, len(generated_sentence))
        trg_len = end_loc - i  # may be different from stride on last loop
        input_ids = generated_sentence[begin_loc:end_loc]
        target_ids = input_ids.clone()
        target_ids[:-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            neg_log_likelihood = outputs[0] * trg_len

        nlls.append(neg_log_likelihood)

    ppl = torch.exp(torch.stack(nlls).sum() / end_loc)
    return ppl.numpy()

def compute_metrics(input_texts):
    # print('predictions : ', input_texts[0], input_texts[0].shape, input_texts[0].size)
    # print('label_id : ', input_texts[1], input_texts[1].shape, input_texts[1].size)
    perplexity = load_metric('perplexity')
    results = perplexity.compute(model_id='models', add_start_token=True, input_texts=input_texts)
    # print('mean_perplexity : ', round(results["mean_perplexity"], 2))
    # print('perplexity : ', round(results["perplexities"][0], 2))
    # print('result : ', results)

    ppl, mean_ppl = round(results["perplexities"][0], 2), round(results["mean_perplexity"], 2)
    return {'perplexity':ppl, 'mean_perplexity':mean_ppl}
