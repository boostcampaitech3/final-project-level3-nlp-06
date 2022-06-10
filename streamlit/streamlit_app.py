import streamlit as st
from streamlit_chat import message

from inference_for_streamlit import load_model, generate_text


model, tokenizer = load_model()
user_results = []

st.title('📚동화 생성기📚')
st.write('프로토타입')
if 'input' not in st.session_state:
    st.session_state['input'] = ''
if 'texts' not in st.session_state:
    st.session_state['messages'] = []

with st.form(key='my_form', clear_on_submit=True):
    col1, col2 = st.columns([8, 1])

    with col1:
        st.text_input('입력 [ex: 맑은 하늘]', key='input')
        max_length = st.slider('생성 길이 조절. 추천 길이는 50~100입니다.', 30, 256, 80)
        temperature = st.slider(
            'Temperature 조절. 생성 길이가 길수록 값을 낮추는게 좋습니다.', 0.1, 1.0, 0.85)
        top_k = st.slider('Top-K', 20, 80, 50)
        top_p = st.slider('Top-P', 0.1, 1.0, 0.95)
        repetition_penalty = st.slider('repetition_penalty', 1.0, 5.0, 1.5)
    with col2:
        st.write('&#9660;&#9660;&#9660;')
        submit = st.form_submit_button(label='Write')

if submit:
    user_result = []
    msg = (st.session_state['input'], True)
    print(msg)
    st.session_state.messages.append(msg)
    for msg in st.session_state.messages:
        message(msg[0], is_user=msg[1])
    with st.spinner('🤖두뇌 풀가동!🤖'):
        result = generate_text(
            msg[0], max_length=max_length,
            model=model, tokenizer=tokenizer,
            top_k=top_k, top_p=top_p, temperature=temperature, repetition_penalty=repetition_penalty
        )
        print(max_length)
        print(result)
    user_result = [msg[0], result, max_length, top_k, top_p, temperature]
    print(user_result)

    # log 기록
    with open('./log/logs.txt', 'a') as f:
        f.write('=' * 30 + '\n')
        f.write(f'[INPUT]: {msg[0]}\n')
        f.write(f'[OUTPUT]: {result}\n')
        f.write(
            f'[MAX_LEN]: {max_length}, [TOP-K]: {top_k}, [TOP-P]: {top_p}, [TEMPER]: {temperature}, [rep]: {repetition_penalty}\n')

    msg = (result, False)
    st.session_state.messages.append(msg)
    message(msg[0], is_user=msg[1])
