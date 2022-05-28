from transformers import (
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    PreTrainedTokenizerFast
)
from util import load_dataset, load_data_collator

# Train
def train(args):
    dir_path = args.dir_path
    model_name = args.model_name
    output_dir = args.output_dir
    overwrite_output_dir = args.overwrite_output_dir
    per_device_train_batch_size = args.per_device_train_batch_size
    num_train_epochs = args.num_train_epochs
    save_steps = args.save_steps

    print(f'Modle is {model_name}')

    # https://github.com/SKT-AI/KoGPT2
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


if __name__ == "__main__":
    train()