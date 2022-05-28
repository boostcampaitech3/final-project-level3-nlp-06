import os
import re
import argparse
from tqdm import tqdm
from kss import split_sentences

def preprocessing(dir,filename):
    """경로 내 txt 파일을 전처리하는 함수
    input| dir: 파일 경로"""

    filelist = os.listdir(dir)
    print(f"preprocessing {len(filelist)} files..")

    i = 1
    filename_list = open(os.path.join(dir,'filenames.txt'),'w', encoding='utf-8')
    for file in tqdm(filelist,total=len(filelist)):
        f,ext = os.path.splitext(os.path.join(dir,file))
        if ext == '.txt':
            # txt file --> sentences list
            result = []
            file = open(os.path.join(dir,file),'r')
            lines = file.readlines()

            # 전처리
            for line in lines:
                line = re.sub(r'\n','',line).strip()
                if line:
                    line = re.sub(r"\s+"," ",line).strip()
                    line = re.sub(r"ㅋ|ㅎ|ㅠ|ㅜ","",line)
                    line = re.sub(r"\(.*\)|\s-\s.*","",line)
                    line = re.sub(r"(http|https)?:\/\/\S+\b|www\.(\w+\.)+\S*","",line).strip()
                    # line = re.sub(r"\..",".",line).strip()
                    # line = re.sub(r"\??","?",line)
                    # line = re.sub(r"\!!","!",line)
                    # line = re.sub(r"\,,",",",line).strip()
                    # line = re.sub(r"\“|\”","\"",line)
                    # line = re.sub(r"\‘|\’|\`","\'",line).strip()
                    # 문장 분리
                    line_list = split_sentences(line,use_heuristic=True,use_quotes_brackets_processing=True)
                    for line in line_list:
                        line = '</s>' + line.strip() + '</s>'
                        result.append(line)
        
            new_file = open(os.path.join(dir,filename+str(i)+ext),'w', encoding='utf-8')
            for line in result:
                new_file.write(line+'\n')
            new_file.close()

            filename_list.write(f+ext+'\t'+filename+str(i)+ext+'\n')
            i += 1
    filename_list.close()

    return "Complete !"



def main(args):
    preprocessing(args.dir,args.filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--dir', type=str, default='./dataset/grimm_tale', help='data dir(default: ./dataset/grimm)')
    parser.add_argument('--filename', type=str, default='grimm', help='data filename(default: grimm)')

    args = parser.parse_args()

    main(args)