from kogpt_inference import generate_text

# validation - perplexity
    test_file_paths = os.listdir(test_dir)

    for i,test_file in enumerate(test_file_paths):
        test_file_path = os.path.join(test_dir,test_file)
        test_dataset = load_dataset(test_file_path, tokenizer)