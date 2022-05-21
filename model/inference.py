from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st
import torch

@st.cache(allow_output_mutation=True)
def load_model():
    # model, tokenizer load
    model_path = './KoGPT/output'
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)

    return model, tokenizer


# inference
def generate_text(sequence, max_length, model, tokenizer, top_k=50, top_p=0.95, temperature=0.85):
    with torch.no_grad():
        #model_path = "./output"
        #model = AutoModelForCausalLM.from_pretrained(model_path)
        #tokenizer = AutoTokenizer.from_pretrained(model_path)
        print(sequence)

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
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)