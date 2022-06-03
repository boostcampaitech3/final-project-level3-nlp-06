import os
import torch

class Dictionary(object):
    def __init__(self):
        self.token2id = {}
        self.id2token = []

    def add_word(self, word):
        if word not in self.token2id:
            self.id2token.append(word)
            self.token2id[word] = len(self.id2token) - 1
        return self.token2id[word]

    def __len__(self):
        return len(self.id2token)

class Corpus(object):
    def __init__(self, path):
        self.dictionary = Dictionary()
        self.train = self.tokenize(os.path.join(path, 'train.txt'))
        self.valid = self.tokenize(os.path.join(path, 'valid.txt'))
        self.test = self.tokenize(os.path.join(path, 'test.txt'))

    def tokenize(self, path):
        """Tokenizes a text file."""
        assert os.path.exists(path)
        # Add words to the dictionary
        with open(path, 'r', encoding="utf-8") as f:
            for line in f:
                words = line.split() + ['<eos>']
                for word in words:
                    self.dictionary.add_word(word)

        # Tokenize file content
        with open(path, 'r', encoding="utf-8") as f:
            idss = []
            for line in f:
                words = line.split() + ['<eos>']
                ids = []
                for word in words:
                    ids.append(self.dictionary.token2id[word])
                idss.append(torch.tensor(ids).type(torch.int64))
            ids = torch.cat(idss)

        return ids

def bptt_batchify(
    data: torch.Tensor,
    batch_size: int,
    sequence_length: int
):
    ''' BPTT 배치화 함수
    한 줄로 길게 구성된 데이터를 받아 BPTT를 위해 배치화합니다.
    batch_size * sequence_length의 배수에 맞지 않아 뒤에 남는 부분은 잘라버립니다.
    이 후 배수에 맞게 조절된 데이터로 BPTT 배치화를 진행합니다.


    Arguments:
    data -- 학습 데이터가 담긴 텐서
            dtype: torch.long
            shape: [data_lentgh]
    batch_size -- 배치 크기
    sequence_length -- 한 샘플의 길이

    Return:
    batches -- 배치화된 텐서
               dtype: torch.long
               shape: [num_sample, batch_size, sequence_length]

    '''
    batches: torch.Tensor = None
    length = data.numel() // (batch_size * sequence_length) \
                           * (batch_size * sequence_length)
    batches = data[:length].reshape(batch_size, -1, sequence_length).transpose(0, 1)

    return batches