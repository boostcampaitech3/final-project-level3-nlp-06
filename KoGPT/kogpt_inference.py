import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteriaList, MaxNewTokensCriteria #MaxLengthCriteria
import time

# inference
def generate_text(sequence, max_length, top_k=50, top_p=0.95, temperature=0.85):
    # stopping_criteria = StoppingCriteriaList([MaxLengthCriteria(max_length=max_length)])
    with torch.no_grad():
        model_path = "./output"
        model = AutoModelForCausalLM.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        ids = tokenizer.encode(f'{sequence},', return_tensors='pt')
        outputs = model.generate(
            ids,
            do_sample=True,
            # max_length=max_length,
            pad_token_id=model.config.pad_token_id,
            bos_token_id=model.config.bos_token_id,
            eos_token_id=model.config.eos_token_id,
            top_k=top_k, # Top-K 샘플링
            top_p=top_p, # Top-P 샘플링
            temperature=temperature, # 높을수록 다양한 결과를 내도록 함
            # forced_eos_token_id = 2
            stopping_criteria = StoppingCriteriaList([MaxNewTokensCriteria(max_length=max_length)])
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def main():
    while True:
        try:
            max_len = int(input('생성할 문장 수 입력: '))
            if max_len < 0:
                print('양수를 입력해주세요')
            else:
                break
        except ValueError:
            print('정수로 입력해주세요.')

    input_text = input('입력!: ')
    outputs = []
    
    k = 50
    p = 0.95
    temperature = 0.85
    for _ in range(5):
        start = time.time()
        header = '=' * 15 + f'k: {k}, p:{p}, len:{max_len}, temp:{temperature}' + '=' * 15
        print(header)
        output = generate_text(input_text, max_len, k, p, temperature)
        outputs.append(header + '\n' + output + '\n')
        print(output)
        print('=' * 15, time.time()-start, '='*15)

    # Append 모드로 저장합니다. 결과 확인용!
    with open(f'./RESULT/result_{input_text}.txt', 'a') as f:
        for output in outputs:
            f.write(output)



    
if __name__ == "__main__":
    main()