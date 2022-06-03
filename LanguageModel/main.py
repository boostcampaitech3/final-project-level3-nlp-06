## 라이브러리 추가하기
import argparse

from train import *

if __name__ == "__main__":
    ## Parser 생성하기
    parser = argparse.ArgumentParser(description="LanguageModel",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    dir_path = 'data'
    rnn_type = 'LSTM' # 'LSTM', 'GRU', 'RNN_TANH', 'RNN_RELU'
    output_dir = 'models'
    num_train_epochs = 30

    parser.add_argument("--rnn_type", default='LSTM', type=str, dest="rnn_type")
    parser.add_argument("--num_train_epochs", default=30, type=int, dest="num_train_epochs")
    parser.add_argument("--dir_path", default='data', type=str, dest="dir_path")
    parser.add_argument("--output_dir", default="models", type=str, dest="output_dir")
    parser.add_argument("--batch_size", default=16, type=int, dest="batch_size")
    parser.add_argument("--sequence_length", default=64, type=int, dest="sequence_length")
    parser.add_argument("--learning_rate", default=20, type=int, dest="learning_rate")
    
    args = parser.parse_args()
    main(args)
