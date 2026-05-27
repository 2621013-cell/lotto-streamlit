import random
import streamlit as st

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="로또 시뮬레이터",
    page_icon="🎰",
    layout="centered"
)

# -----------------------------
# 제목
# -----------------------------
st.title("🎰 로또 시뮬레이터")
st.write("직접 번호를 선택하고 당첨 결과를 확인하세요!")

# -----------------------------
# 로또 번호 생성 함수
# -----------------------------
def generate_lotto_numbers():

    numbers = list(range(1, 46))
    random.shuffle(numbers)

    main_numbers = sorted(numbers[:6])
    bonus_number = numbers[6]

    return main_numbers, bonus_number


# -----------------------------
# 당첨 결과 확인 함수
# -----------------------------
def check_lotto_result(user_numbers, lotto_numbers):

    # 맞춘 번호 개수
    matched = len(set(user_numbers) & set(lotto_numbers))

    # 당첨 기준
    if matched == 6:
        rank = "🎉 1등"
        prize = "200,000,000원"

    elif matched == 5:
        rank = "🥈 2등"
        prize = "10,000,000원"

    elif matched == 4:
        rank = "🥉 3등"
        prize = "300,000원"

    elif matched == 3:
        rank = "🏅 4등"
        prize = "100,000원"

    elif matched == 2:
        rank = "🎁 5등"
        prize = "20,000원"

    elif matched == 1:
        rank = "🎊 참가상"
        prize = "5,000원"

    else:
        rank = "❌ 낙첨"
        prize = "0원"

    return matched, rank, prize


# -----------------------------
# 사용자 번호 선택
# -----------------------------
st.subheader("✍️ 내 번호 선택")

user_numbers = st.multiselect(
    "1~45 중 6개의 번호를 선택하세요",
    options=list(range(1, 46)),
    max_selections=6
)

# -----------------------------
# 추첨 버튼
# -----------------------------
if st.button("🎲 로또 추첨하기"):

    # 번호 6개 선택 확인
    if len(user_numbers) != 6:
        st.error("반드시 6개의 번호를 선택해야 합니다.")

    else:

        # 로또 번호 생성
        lotto_numbers, bonus_number = generate_lotto_numbers()

        # 결과 확인
        matched, rank, prize = check_lotto_result(
            user_numbers,
            lotto_numbers
        )

        # 결과 출력
        st.success("추첨 완료!")

        st.subheader("🎯 당첨 번호")
        st.write(lotto_numbers)

        st.subheader("⭐ 보너스 번호")
        st.write(bonus_number)

        st.subheader("🙋 내 번호")
        st.write(sorted(user_numbers))

        st.subheader("📊 결과")

        st.write(f"일치한 번호 개수: {matched}개")
        st.write(f"등수: {rank}")
        st.write(f"상금: {prize}")

        # 1등이면 풍선 효과
        if matched == 6:
            st.balloons()
