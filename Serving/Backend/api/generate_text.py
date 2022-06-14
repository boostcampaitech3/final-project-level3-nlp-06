import numpy as np
import torch
from transformers import AutoModelForCausalLM, PreTrainedTokenizerFast
import gc
gc.collect()
torch.cuda.empty_cache()
torch.manual_seed(1234)
model_path = 'wapari/KoGPT-trinity-tales'

model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = PreTrainedTokenizerFast.from_pretrained(model_path)

model = model.to('cuda')

def sentence_slice(input_str:str, sent_num:int):

    sent_token_rindx = input_str.rfind('</s>')
    sliced = input_str[0:sent_token_rindx]
    sliced = sliced.replace('<unk>', "\"") 
    _temp = sliced.replace('</s>', '', (sent_num*2)+1) 
    _temp_position = _temp.find('</s>') # 이제 여기서 </s>이후 문장은 전부 삭제합니다.
    sliced = _temp[:_temp_position]
    
    # </s>이후 문장은 전부 삭제합니다.
    return  sliced



def generate_model(data, sent_num, temp, rep) :
    with torch.no_grad():
        prompt_ids = tokenizer.encode(data, return_tensors='pt').to('cuda')
        outputs = model.generate(
            prompt_ids,
            do_sample=True,
                    max_length=180,
                    pad_token_id=model.config.pad_token_id,
                    bos_token_id=model.config.bos_token_id,
                    eos_token_id=model.config.eos_token_id,
                    top_k=50, # Top-K 샘플링
                    top_p=0.95, # Top-P 샘플링
                    temperature=temp, # 높을수록 다양한 결과를 내도록 함
                    num_return_sequences=3,
                    repetition_penalty=rep,
                    early_stopping=True,
                    use_cache=True,
                    truncation=False,
        )
        sentence_dict ={}
        for i, output in enumerate(outputs):
            
            print(f'[pre-slice]: {tokenizer.decode(output)}')
            result = sentence_slice(tokenizer.decode(output), sent_num)
            sentence_dict[i] = result
            print(f'[after-slice] {result}')
        
    return sentence_dict
