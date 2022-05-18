# KoGPT-Trinity
KoGPT Trinity는 GPT-3 기반의 한국어 모델입니다.
본 프로젝트에서는 `skt/ko-gpt-trinity-1.2B-v0.5`에 전래동화 데이터를 학습시켰습니다. (다른 동화 데이터는 아직 학습시켜보지 않았습니다!)

## ISSUE
- GPT-3 기반의 한국어 모델에는 kakao braind의 KoGPT도 있습니다만.. parameter 숫자가 6B에 달해서 OoM 문제가 있어 학습시키기가 힘들었습니다.
- 같은 GPT-3 기반의 한국어 모델인 skt/ko-gpt-trinity의 경우에는 paramter 숫자가 1.2B로 학습은 가능하여 선택하였습니다.
- 참고로, skt/kogpt2 의 경우에는 parameter 숫자가 125M입니다.
- 모델이 무거운 만큼 inference 속도가 kogpt2에 비하여 상대적으로 느립니다.
  - 모델의 일부를 freezing 하거나
  - half-precision 등을 적용하여 경량화를 해볼 수 있을 것 같습니다.