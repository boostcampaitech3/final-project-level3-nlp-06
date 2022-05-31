from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st
import torch
import time

@st.cache(allow_output_mutation=True)
def load_model():
    # model, tokenizer load
    model_path = './KoGPT/output'
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    
    print(model.config)
    return model, tokenizer

def sentence_slice(input_str:str):
    sent_token_rindx = input_str.rfind('</s>')
    sliced = input_str[0:sent_token_rindx]
    sliced = sliced.replace('</s>', '')
    sliced = sliced.replace('<unk>', '')

    return sliced


# inference
def generate_text(sequence, max_length, model, tokenizer, top_k=50, top_p=0.95, temperature=0.85, repetition_penalty=1.5):
    with torch.no_grad():
        print(sequence)

        s_t = time.time()
        ids = tokenizer.encode(f'{sequence}', return_tensors='pt')
        outputs = model.generate(
            ids,
            do_sample=True,
            max_length=max_length,
            pad_token_id=model.config.pad_token_id,
            bos_token_id=model.config.bos_token_id,
            eos_token_id=model.config.eos_token_id,
            top_k=top_k, # Top-K 샘플링
            top_p=top_p, # Top-P 샘플링
            temperature=temperature, # 높을수록 다양한 결과를 내도록 함
            repetition_penalty=repetition_penalty,
            use_cache=True,
        )
        cost_time = time.time() - s_t

    return sentence_slice(tokenizer.decode(outputs[0]))

