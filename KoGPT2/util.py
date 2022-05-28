import os
import pickle
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import DataCollatorForLanguageModeling, PreTrainedTokenizer
from transformers.utils.logging import *


from torch.utils.data import Dataset
from typing import Optional
from filelock import FileLock
import time

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

def load_dataset(directory_path, tokenizer, block_size=128):
    dataset = TextDataset(
        tokenizer=tokenizer,
        directory_path=directory_path,
        block_size=block_size
    )
    return dataset


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
        directory_path: str,
        block_size: int,
        overwrite_cache=False,
        cache_dir: Optional[str] = None
    ):
        if os.path.isdir(directory_path) is False:
            raise ValueError(f"Input directory path {directory_path} not found")

        block_size = block_size - tokenizer.num_special_tokens_to_add(pair=False)

        file_list = []
        for (root, _, files) in os.walk(directory_path):
            for file in files:
                if '.txt' in file:
                    file_path = os.path.join(root, file)
                    file_list += [file_path]

        directory, cache_filename = directory_path, "cache"
        cached_features_file = os.path.join(
            cache_dir if cache_dir is not None else directory,
            f"cached_lm_{tokenizer.__class__.__name__}_{block_size}_{cache_filename}{len(file_list)}",
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

def perplexity(output, target):
    output = np.array(output)
    target = np.array(target)
    if output.shape[0] <= target.shape[0]:
        zero_output = np.zeros_like(target)
        zero_output[:output.shape[0]] = output
        output = zero_output
    else:
        zero_output = np.zeros_like(output)
        zero_output[:target.shape[0]] = target
        target = zero_output

    target = torch.FloatTensor(target)
    output = torch.FloatTensor(output)
    loss = F.cross_entropy(output,target)
    return torch.exp(loss)