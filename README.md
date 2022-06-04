##  :penguin: 자, 연어 한접시's Final Project :penguin:
### 부스트 캠프 AI Tech 3기 06조의 함께쓰는 동화 프로젝트 :green_book::orange_book::blue_book:

해당 프로젝트는 네이버 커넥트재단의 부스트캠프 AI tech 3기 nlp06조 자,연어 한 접시가 최종 프로젝트로 기획하였습니다.

## 팀원 소개
|<img src="https://avatars.githubusercontent.com/u/86389775?v=4" width = 80>|<img src="https://avatars.githubusercontent.com/u/63946027?v=4" width=80>|<img src="https://avatars.githubusercontent.com/u/56011433?v=4" width=80>|<img src="https://avatars.githubusercontent.com/u/30717355?v=4" width=80>|<img src="https://avatars.githubusercontent.com/u/52444343?v=4" width=80>|
| :--------: | :--------: | :--------: | :--------: | :--------: |
|[T3252] 김선재<br>[@ksj1453](https://github.com/ksj1453)|[T3215] 차경민<br>[@rudals0215](https://github.com/rudals0215)|[T3140] 이도훈<br>[@Sunjii](https://github.com/Sunjii)|[T3065] 김태훈<br>[@thkim107](https://github.com/thkim107)|[T3007] <br> 강진희<br>[@JINHEE-KANG](https://github.com/JINHEE-KANG)|
|데이터 수집 및 전처리|데이터 수집 및 전처리|데이터 수집 및 전처리|데이터 수집 및 전처리|데이터 수집 및 전처리|
|데이터 분석 <br>및 문장 추천 모델 실험|이미지 style-transfer <br>모델 실험 및 학습|문장 생성 모델 실험 <br>및 베이스라인 작성|데이터 분석|키워드 추출 실험<br>및 이미지 검색 API 연계|
|백엔드 구축<br>동화 생성 모델 학습|동화 생성 모델 학습|프로토타입 및 프론트엔드 구축<br>동화 생성 모델 학습|서비스 아키텍쳐 구성<br>및 UI/UX 디자인|동화 생성 모델 학습|


---
# 함께 쓰는 참여형 동화 서비스 GatherBook

GatherBook은 사용자가 동화 문장을 입력하면 다음으로 이어질 문장을 창작하여 사용자와 번갈아가며 동화를 작성하는 참여형 창작 웹서비스 입니다.

> 데모 여기에
<p align="center">
  <img src=src/demo.gif />
</p>

## Installation
```bash
pip install -r requirements.txt
```

## Architecture
**Tale generation model**
![](src/KoGPT-trinity.png)

**Image style-transfer model**
![](src/cyclegan.png)

## Usage
### Train
**Tale generation model**
```bash
python KoGPT/kogpt_trainer.py
python KoGPT2/main.py
```

**Image style-transfer model**
```bash
python cyclegan/main.py
```

### Inference
**Tale generation model**
```bash
python KoGPT/kogpt_inference.py
python KoGPT2/inference.py
```

**Image style-transfer model**
```bash
python cyclegan/inference.py
```


### Web
```bash

```


### Service Outputs
<p align="center">
    <img src= style="display: inline" width=>
    <img src= style="display: inline" width=>
    <img src= style="display: inline" width=>
</p>

### Dataset
- [어린이 전래동화 (청와대)](http://18children.president.pa.go.kr/our_space/fairy_tales.php)
- [국립국어원 모두의 말뭉치 비출판물 데이터](https://corpus.korean.go.kr/)
- [그림형제 동화 번역 데이터](https://m.blog.naver.com/osy2201/221179543994)
- [이솝우화 동화 번역 데이터](https://m.blog.naver.com/osy2201/221183426988)
- [신춘문예 당선작]()
- [픽사베이 무료 이미지](https://pixabay.com/)

### Reference
