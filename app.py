import random
import streamlit as st


def generate_lotto_numbers():
    """로또 번호 (6개 메인 번호, 1개 보너스 번호)를 생성합니다."""
    # random.sample을 사용하면 더 간결하게 추출할 수 있습니다.
    picked_numbers = random.sample(range(1, 46), 7)

    main_numbers = sorted(picked_numbers[:6])
    bonus_number = picked_numbers[6]

    return main_numbers, bonus_number


# --- Streamlit UI 설정 ---
st.set_page_config(page_title="인생역전 로또 번호 생성기", page_icon="🍀")

st.title("🍀 로또 번호 생성기")
st.write("아래 버튼을 누르면 행운의 로또 번호가 생성됩니다!")

# 구분선
st.divider()

# 버튼 생성 및 클릭 이벤트 처리
if st.button("🔮 행운의 번호 뽑기", type="primary"):
    main_nums, bonus_num = generate_lotto_numbers()

    # 메인 번호를 예쁘게 보여주기 위한 텍스트 변환
    main_nums_str = "  ".join([f"[{num}]" for num in main_nums])

    # 결과 출력
    st.subheader("
