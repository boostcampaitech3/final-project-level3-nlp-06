import numpy as np
import torch
import torch.nn.functional as F
from typing import NoReturn
from transformers import (
    DataCollatorForLanguageModeling,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    AutoTokenizer,
    GPT2LMHeadModel,
    PreTrainedTokenizerFast
)

from util import TextDataset, perplexity, load_dataset, load_data_collator

# Train
def train(
    dir_path, 
    model_name, 
    output_dir,
    overwrite_output_dir,
    per_device_train_batch_size,
    num_train_epochs,
    save_steps
    ):
    # https://huggingface.co/skt/ko-gpt-trinity-1.2B-v0.5
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name, 
                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                    pad_token='<pad>', mask_token='<mask>')

    print('load dataset...')
    train_dataset = load_dataset(dir_path, tokenizer)
    data_collator = load_data_collator(tokenizer)
    print(f'{dir_path} loaded!')
    
    tokenizer.save_pretrained(output_dir, legacy_format=False)
    print(f'Tokenizer save_pretrained. {output_dir}')
    
    model = GPT2LMHeadModel.from_pretrained(model_name)
    
    model.save_pretrained(output_dir)
    print(f'Model save_pretrained. {output_dir}')
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=overwrite_output_dir,
        per_device_train_batch_size=per_device_train_batch_size,
        num_train_epochs=num_train_epochs,
        #fp16=True,
    )

    print(training_args)
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )
        
    trainer.train()
    print("Training Done!!")

    trainer.save_model()
    print(f'model saved.')


## Main
def main():
    torch.cuda.empty_cache()
    # 모델명, 데이터 위치, 모델 저장위치, Training arguments를 정의합니다.
    dir_path = 'datasets'
    model_name = 'skt/ko-gpt-trinity-1.2B-v0.5'
    output_dir = 'models'
    overwrite_output_dir = False
    per_device_train_batch_size = 4 # batch 사이즈 조절 시 oom이 발생할 수 있습니다...
    num_train_epochs = 10
    save_steps = 500
    
    print(f'Modle is {model_name}')
    
    train(
        dir_path=dir_path,
        model_name=model_name,
        output_dir=output_dir,
        overwrite_output_dir=overwrite_output_dir,
        per_device_train_batch_size=per_device_train_batch_size,
        num_train_epochs=num_train_epochs,
        save_steps=save_steps
    )

    print("Training Done!!")



if __name__ == "__main__":
    main()