import argparse

import os
import pickle
import torch
from dataset import Corpus

from tqdm.notebook import trange

def main(args):
    num_words = args.num_words
    temperature = args.temperature
    output_dir = args.output_dir
    dir_path = args.dir_path
    input = args.input

    corpus = None
    with open(os.path.join(dir_path, 'data_dict.pkl'), 'rb') as f:
        corpus = pickle.load(f)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # 가장 좋았던 모았던 모델을 불러옵니다.
    model = torch.load(os.path.join(output_dir,'model.pt'), map_location=device)
    # RNN을 로드하는 경우 메모리 연속적으로 들고오지 않기 때문에 이를 연속화해서 Forward 속도를 올릴 수 있습니다. 
    model.rnn.flatten_parameters()

    hidden = model.init_hidden(1)
    prev = input
    input = corpus.dictionary.token2id[input]
    input = torch.Tensor([[input]])
    input = input.type(torch.long).to(device)

    outputs = []
    for i in trange(num_words, desc="Generation"):
        with torch.no_grad():
            log_prob, hidden = model(input, hidden)

        weights = (log_prob.squeeze() / temperature).exp()
        token_id = torch.multinomial(weights, 1)
        outputs.append(token_id.item())
        input = token_id.unsqueeze(0)

    outputs = [prev] + [corpus.dictionary.id2token[token_id] for token_id in outputs]
    print(' '.join(outputs).replace('<eos>', '\n'))

    with open('generate.txt', 'w') as fd:
        fd.write(' '.join(outputs).replace('<eos>', '\n'))

if __name__ == "__main__":
    ## Parser 생성하기
    parser = argparse.ArgumentParser(description="LanguageModel",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--input", default='초콜릿', type=str, dest="input")
    parser.add_argument("--num_words", default=128, type=int, dest="num_words")
    parser.add_argument("--temperature", default=1.0, type=float, dest="temperature")
    parser.add_argument("--dir_path", default='data', type=str, dest="dir_path")
    parser.add_argument("--output_dir", default="models", type=str, dest="output_dir")

    args = parser.parse_args()
    main(args)

