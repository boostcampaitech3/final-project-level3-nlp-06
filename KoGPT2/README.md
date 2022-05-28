# KoGPT2

- KoGPT2?
    - GPT-2의 부족한 한국어 성능 향상을 위해, 40GB 이상의 한국어 corpus로 학습된 모델!
    - [https://github.com/SKT-AI/KoGPT2](https://github.com/SKT-AI/KoGPT2)
    - 본 프로젝트에서는 `skt/kogpt2-base-v2` 모델 사용

- Tokenizer
    - 허깅페이스 [tokenizers](https://github.com/huggingface/tokenizers) 패키지의 Character BPE tokenizer 사용했다고 합니다.
    - vocab size는 51,200이고, 일부 자주 사용되는 이모지와 이모티콘도 포함되어 있다고 합니다.
    - 그 외에 `unused0` ~ `unused99` 의 미사용 토큰이 존재하는데, 이는 각자 정의하여 task에 맞춰 사용하면 된다고 합니다.
    
    ```python
    > from transformers import PreTrainedTokenizerFast
    > tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
      bos_token='</s>', eos_token='</s>', unk_token='<unk>',
      pad_token='<pad>', mask_token='<mask>')
    > tokenizer.tokenize("안녕하세요. 한국어 GPT-2 입니다.😤:)l^o")
    ['▁안녕', '하', '세', '요.', '▁한국어', '▁G', 'P', 'T', '-2', '▁입', '니다.', '😤', ':)', 'l^o']
    ```

- Data
  - KoGPT2의 경우 `한국어 위키 백과`, 뉴스, `모두의 말뭉치 v1.0`, `청와대 국민청원` 등의 다양한 데이터를 사용
  - 본 프로젝트에서는 여러 `동화 데이터`를 이용해 학습을 시켜 동화 생성에 최적화된 모델을 만드는 것을 목표로 합니다.
    - 어린이 청와대 - 전래동화 100선
    - 그림형제 동화 모음집
    - 국립 국어원 비출판물 데이터
    - 그 외에도 계속 쓸만한 데이터가 있는지 찾아보고 있습니다.

- Usage

```bash
python kogpt2_trainer.py # 모델 학습 및 output 폴더에 저장합니다.
python kogpt2_inference.py # 학습한 모델을 이용해서 테스트 해볼 수 있습니다.
```
> inference시 여러 parameter를 조정하여 결과물을 다양하게 살펴볼 수 있습니다. 주석을 참고해주세요.