import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="로또 번호 생성기",
    page_icon="🎰",
    layout="centered"
)

# 제목
st.title("🎰 로또 번호 생성기")
st.write("버튼을 누르면 로또 번호를 생성합니다!")

def generate_lotto_numbers():
    """
    로또 번호 생성
    메인 번호 6개 + 보너스 번호 1개
    """

    # 1~45 숫자 생성
    numbers = list(range(1, 46))

    # 랜덤 섞기
    random.shuffle(numbers)

    # 메인 번호 6개
    main_numbers = sorted(numbers[:6])

    # 보너스 번호
    bonus_number = numbers[6]

    return main_numbers, bonus_number


# 버튼 클릭 시 생성
if st.button("번호 생성하기"):

    main_nums, bonus_num = generate_lotto_numbers()

    st.success("로또 번호 생성 완료!")

    st.subheader("🎯 메인 번호")
    st.write(main_nums)

    st.subheader("⭐ 보너스 번호")
    st.write(bonus_num)

    # 풍선 효과
    st.balloons()
