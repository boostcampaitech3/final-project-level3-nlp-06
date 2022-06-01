from datasets import load_metric, load_dataset

# If you have a problem, execute "pip install --upgrade datasets"
def main():
    perplexity = load_metric('perplexity')
    input_texts = load_dataset("wikitext",
                                        "wikitext-2-raw-v1",
                                        split="test")["text"][:50]
    input_texts = [s for s in input_texts if s!='']
    results = perplexity.compute(model_id='gpt2',
                                input_texts=input_texts)
    print(list(results.keys()))
    print(round(results["mean_perplexity"], 2))
    print(round(results["perplexities"][0], 2))

if __name__ == "__main__":
    main()