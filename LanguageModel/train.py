import os
import math
import pickle

from typing import Union, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F

from dataset import Corpus, bptt_batchify
from model import RNNModel
from tqdm.notebook import tqdm
from torch.nn.utils import clip_grad_norm_


def main(args):
    dir_path = args.dir_path
    rnn_type = args.rnn_type
    output_dir = args.output_dir
    num_epoch = args.num_train_epochs
    batch_size = args.batch_size
    sequence_length = args.sequence_length
    lr = args.learning_rate
    corpus = Corpus(dir_path)

    vocab_size = len(corpus.dictionary)
    model = RNNModel(rnn_type, vocab_size=vocab_size)

    train_data = bptt_batchify(corpus.train, batch_size, sequence_length)
    val_data = bptt_batchify(corpus.valid, batch_size, sequence_length)
    test_data = bptt_batchify(corpus.test, batch_size, sequence_length)

    lr = 20
    best_val_loss = None

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for epoch in range(1, num_epoch+1):
        train(model, train_data, lr)
        val_loss = evaluate(model, val_data)
        print('-' * 89)
        print(f'| End of epoch {epoch:2d} | valid loss {val_loss:5.2f} | valid ppl {math.exp(val_loss):8.2f}')
        print('-' * 89)

        if not best_val_loss or val_loss < best_val_loss:
            torch.save(model, os.path.join(output_dir,'model.pt'))
            best_val_loss = val_loss
        else:
            # 모델이 좋아지지 않으면 학습률을 낮춥니다.
            lr /= 4.0
    
    # Dictonary 저장
    with open(os.path.join(dir_path, 'data_dict.pkl'), 'wb') as f:
        pickle.dump(corpus, f)

    # 가장 좋았던 모았던 모델을 불러옵니다.
    model = torch.load(os.path.join(output_dir,'model.pt'), map_location=device)
    # RNN을 로드하는 경우 메모리 연속적으로 들고오지 않기 때문에 이를 연속화해서 Forward 속도를 올릴 수 있습니다. 
    model.rnn.flatten_parameters()

    test_loss = evaluate(model, test_data)
    print('=' * 89)
    print(f'| End of training | test loss {test_loss:5.2f} | test ppl {math.exp(test_loss):8.2f}')
    print('=' * 89)




            

def train(
    model: RNNModel,
    data: torch.Tensor,     # Shape: (num_sample, batch_size, sequence_length)
    lr: float
):
    model.train()
    batch_size = data.shape[1]
    total_loss = 0.

    hidden = model.init_hidden(batch_size)
    # tqdm을 이용해 진행바를 만들어 봅시다.
    progress_bar = tqdm(data, desc="Train")
    for bid, batch in enumerate(progress_bar, start=1):
        batch = batch.to(model.device)      # RNN Model에 정의했던 device 프로퍼티를 사용

        output, hidden = model(batch, hidden)
        if model.rnn_type == 'LSTM':
            hidden = tuple(tensor.detach() for tensor in hidden)
        else:
            hidden = hidden.detach()

        # 손실 함수는 Negative log likelihood로 계산합니다.
        # https://pytorch.org/docs/stable/generated/torch.nn.NLLLoss.html
        loss = F.nll_loss(output[:, :-1, :].transpose(1, 2), batch[:, 1:])
        
        model.zero_grad()
        loss.backward()
        # clip_grad_norm_을 통해 기울기 폭주 (Gradient Exploding) 문제를 방지합니다.
        clip_grad_norm_(model.parameters(), 0.25)
        for param in model.parameters():
            param.data.add_(param.grad, alpha=-lr)
        
        total_loss += loss.item()
        current_loss = total_loss / bid

        # Perplexity는 계산된 Negative log likelihood의 Exponential 입니다.
        progress_bar.set_description(f"Train - loss {current_loss:5.2f} | ppl {math.exp(current_loss):8.2f} | lr {lr:02.2f}", refresh=False)


# 학습 과정이 아니므로 기울기 계산 과정은 불필요합니다. 
@torch.no_grad()
def evaluate(
    model: RNNModel,
    data: torch.Tensor
):
    ''' 모델 평가 코드
    모델을 받아 해당 데이터에 대해 평가해 평균 Loss 값을 반환합니다.
    위의 Train 코드를 참고하여 작성해보세요.

    Arguments:
    model -- 평가할 RNN 모델
    data -- 평가용 데이터
            dtype: torch.long
            shape: [num_sample, batch_size, sequence_length]

    Return:
    loss -- 계산된 평균 Loss 값
    '''
    model.eval()

    loss: float = None
    total_loss = 0.
    hidden = model.init_hidden(data.shape[1])
    
    for batch in data:
        batch = batch.to(model.device)

        output, hidden = model(batch, hidden)
        total_loss += F.nll_loss(output[:, :-1, :].transpose(1, 2), batch[:, 1:]).item()
    
    loss = total_loss / len(data)
    

    return loss