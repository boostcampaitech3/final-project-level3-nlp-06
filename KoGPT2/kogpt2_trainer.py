from typing import NoReturn
from transformers import (
    DataCollatorForLanguageModeling,
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    PreTrainedTokenizerFast
)
from util import load_dataset, load_data_collator

# Train
def train(
    directory_path, 
    model_name, 
    output_dir,
    overwrite_output_dir,
    per_device_train_batch_size,
    num_train_epochs,
    save_steps
    ):
    # https://github.com/SKT-AI/KoGPT2
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name,
                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                    pad_token='<pad>', mask_token='<mask>')

    print('load dataset...')
    train_dataset = load_dataset(directory_path, tokenizer)
    data_collator = load_data_collator(tokenizer)
    print(f'{directory_path} loaded!')
    
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
    # 모델명, 데이터 위치, 모델 저장위치, Training arguments를 정의합니다.
    directory_path = 'datasets'
    model_name = 'skt/kogpt2-base-v2'
    output_dir = 'models'
    overwrite_output_dir = False
    per_device_train_batch_size = 16
    num_train_epochs = 10
    save_steps = 500
    
    print(f'Modle is {model_name}')
    
    train(
        directory_path=directory_path,
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