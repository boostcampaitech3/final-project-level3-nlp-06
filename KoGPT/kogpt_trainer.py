from typing import NoReturn
from transformers import (
    TextDataset,
    DataCollatorForLanguageModeling,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    AutoTokenizer
)
import torch
 

def load_dataset(file_path, tokenizer, block_size = 128):
    dataset = TextDataset(
        tokenizer = tokenizer,
        file_path = file_path,
        block_size = block_size,
    )
    return dataset
 
def load_data_collator(tokenizer, mlm = False):
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, 
        mlm=mlm,
    )
    return data_collator

# Train
def train(
    train_file_path, 
    model_name, 
    output_dir,
    overwrite_output_dir,
    per_device_train_batch_size,
    num_train_epochs,
    save_steps
    ):
    # https://huggingface.co/skt/ko-gpt-trinity-1.2B-v0.5
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    print('load dataset...')
    train_dataset = load_dataset(train_file_path, tokenizer)
    data_collator = load_data_collator(tokenizer)
    print(f'{train_file_path} loaded!')
    
    tokenizer.save_pretrained(output_dir, legacy_format=False)
    print(f'Tokenizer save_pretrained. {output_dir}')
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        pad_token_id=tokenizer.eos_token_id,
        torch_dtype='auto', low_cpu_mem_usage=True
        ).to(device='cuda', non_blocking=True)

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
    trainer.save_model()
    print(f'model saved.')


## Main
def main():
    torch.cuda.empty_cache()
    # 모델명, 데이터 위치, 모델 저장위치, Training arguments를 정의합니다.
    train_file_path = './concate_tale_copy.txt'
    model_name = 'skt/ko-gpt-trinity-1.2B-v0.5'
    output_dir = './output'
    overwrite_output_dir = False
    per_device_train_batch_size = 4 # batch 사이즈 조절 시 oom이 발생할 수 있습니다...
    num_train_epochs = 10
    save_steps = 500
    
    print(f'Modle is {model_name}')
    
    train(
        train_file_path=train_file_path,
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