from typing import Union, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F

class RNNModel(nn.Module):
    def __init__(self, 
        rnn_type: str,
        vocab_size: int,
        embedding_size: int=200,
        hidden_size: int=200,
        num_hidden_layers: int=2,
        dropout: float=0.5
    ):
        super().__init__()
        self.rnn_type = rnn_type
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layer = num_hidden_layers
        assert rnn_type in {'LSTM', 'GRU', 'RNN_TANH', 'RNN_RELU'}

        # 정수 형태의 id를 고유 벡터 형식으로 나타내기 위하여 학습 가능한 Embedding Layer를 사용합니다.
        # https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html
        self.embedding = nn.Embedding(vocab_size, embedding_size)

        # Dropout은 RNN 사용시 많이 쓰입니다.
        # https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html 
        self.dropout = nn.Dropout(dropout)

        if rnn_type.startswith('RNN'):
            # Pytorch에서 제공하는 기본 RNN을 사용해 봅시다.
            # https://pytorch.org/docs/stable/generated/torch.nn.RNN.html 
            nonlinearity = rnn_type.split('_')[-1].lower()
            self.rnn = nn.RNN(
                embedding_size, 
                hidden_size, 
                num_hidden_layers,
                batch_first=True, 
                nonlinearity=nonlinearity,
                dropout=dropout
            )
        else:
            # Pytorch의 LSTM과 GRU를 사용해 봅시다.
            # LSTM: https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html
            # RGU: https://pytorch.org/docs/stable/generated/torch.nn.GRU.html
            self.rnn = getattr(nn, rnn_type)(
                embedding_size,
                hidden_size,
                num_hidden_layers,
                batch_first=True,
                dropout=dropout
            )

        # 최종적으로 나온 hidden state를 이용해 다음 토큰을 예측하는 출력층을 구성합시다.
        self.projection = nn.Linear(hidden_size, vocab_size)

    def forward(
        self, 
        input: torch.Tensor,
        prev_hidden: Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]
    ):
        """ RNN 모델의 forward 함수 구현
        Arguments:
        input -- 토큰화 및 배치화된 문장들의 텐서
                    dtype: torch.long
                    shape: [batch_size, sequence_lentgh]
        prev_hidden -- 이전의 hidden state
                    dtype: torch.float
                    shape: RNN, GRU - [num_layers, batch_size, hidden_size]
                           LSTM - ([num_layers, batch_size, hidden_size], [num_layers, batch_size, hidden_size])

        Return:
        log_prob -- 다음 토큰을 예측한 확률에 log를 취한 값
                    dtype: torch.float
                    shape: [batch_size, sequence_length, vocab_size]
        next_hidden -- 이후의 hidden state
                    dtype: torch.float
                    shape: RNN, GRU - [num_layers, batch_size, hidden_size]
                           LSTM - ([num_layers, batch_size, hidden_size], [num_layers, batch_size, hidden_size])
        """

        log_prob: torch.Tensor = None
        next_hidden: Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]] = None
        
        emb = self.dropout(self.embedding(input))
        output, next_hidden = self.rnn(emb, prev_hidden)
        log_prob = self.projection(self.dropout(output)).log_softmax(dim=-1)

        
        assert list(log_prob.shape) == list(input.shape) + [self.vocab_size]
        assert prev_hidden.shape == next_hidden if self.rnn_type != 'LSTM' \
          else prev_hidden[0].shape == next_hidden[0].shape == next_hidden[1].shape
        
        return log_prob, next_hidden
    
    def init_hidden(self, batch_size: int):
        """ 첫 hidden state를 반환하는 함수 """
        weight = self.projection.weight
        
        if self.rnn_type == 'LSTM':
            return (weight.new_zeros(self.num_hidden_layer, batch_size, self.hidden_size),
                    weight.new_zeros(self.num_hidden_layer, batch_size, self.hidden_size))
        else:
            return weight.new_zeros(self.num_hidden_layer, batch_size, self.hidden_size)
    
    @property
    def device(self):   # 현재 모델의 device를 반환하는 프로퍼티
        return self.projection.weight.device