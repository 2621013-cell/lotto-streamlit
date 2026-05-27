import random
import streamlit as st

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🎰 Ultimate 로또 게임",
    page_icon="🎰",
    layout="centered"
)

# -----------------------------
# CSS 스타일
# -----------------------------
st.markdown("""
<style>

.ball {
    display:inline-block;
    width:55px;
    height:55px;
    border-radius:50%;
    text-align:center;
    line-height:55px;
    color:white;
    font-size:22px;
    font-weight:bold;
    margin:4px;
}

.yellow {background:#fbc400;}
.blue {background:#69c8f2;}
.red {background:#ff7272;}
.gray {background:#aaaaaa;}
.green {background:#b0d840;}

.result-box {
    padding:15px;
    border-radius:10px;
    background:#f5f5f5;
    margin-top:10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 제목
# -----------------------------
st.title("🎰 Ultimate 로또 게임")
st.write("번호를 선택하고 로또 게임에 도전하세요!")

# -----------------------------
# session_state 초기화
# -----------------------------
if "money" not in st.session_state:
    st.session_state.money = 100000

if "games" not in st.session_state:
    st.session_state.games = 0

if "wins" not in st.session_state:
    st.session_state.wins = 0

# -----------------------------
# 번호 색상 함수
# -----------------------------
def get_color(num):

    if num <= 10:
        return "yellow"

    elif num <= 20:
        return "blue"

    elif num <= 30:
        return "red"

    elif num <= 40:
        return "gray"

    else:
        return "green"

# -----------------------------
# 공 출력 함수
# -----------------------------
def draw_balls(numbers):

    html = ""

    for num in numbers:

        color = get_color(num)

        html += f"""
        <div class="ball {color}">
            {num}
        </div>
        """

    st.markdown(html, unsafe_allow_html=True)

# -----------------------------
# 로또 번호 생성
# -----------------------------
def generate_lotto_numbers():

    selected = random.sample(range(1, 46), 7)

    main_numbers = sorted(selected[:6])
    bonus_number = selected[6]

    return main_numbers, bonus_number

# -----------------------------
# 당첨 확인
# -----------------------------
def check_result(user_numbers, lotto_numbers):

    matched = len(set(user_numbers) & set(lotto_numbers))

    if matched == 6:
        rank = "🎉 1등"
        prize = 2000000000

    elif matched == 5:
        rank = "🥈 2등"
        prize = 100000000

    elif matched == 4:
        rank = "🥉 3등"
        prize = 3000000

    elif matched == 3:
        rank = "🏅 4등"
        prize = 1000000

    elif matched == 2:
        rank = "🎁 5등"
        prize = 200000

    elif matched == 1:
        rank = "🎊 참가상"
        prize = 50000

    else:
        rank = "❌ 낙첨"
        prize = 0

    return matched, rank, prize

# -----------------------------
# 게임 정보
# -----------------------------
st.subheader("🎮 내 게임 정보")

col1, col2, col3 = st.columns(3)

col1.metric("💰 보유 금액", f"{st.session_state.money:,}원")
col2.metric("🎲 플레이 횟수", st.session_state.games)
col3.metric("🏆 당첨 횟수", st.session_state.wins)

st.divider()

# -----------------------------
# 자동 번호 생성
# -----------------------------
if st.button("🤖 자동 번호 선택"):

    st.session_state.auto_numbers = sorted(
        random.sample(range(1, 46), 6)
    )

# -----------------------------
# 번호 선택
# -----------------------------
st.subheader("✍️ 번호 선택")

default_numbers = st.session_state.get("auto_numbers", [])

user_numbers = st.multiselect(
    "1~45 중 6개의 번호를 선택하세요",
    options=list(range(1, 46)),
    default=default_numbers,
    max_selections=6
)

# -----------------------------
# 게임 시작
# -----------------------------
if st.button("🎲 로또 추첨하기"):

    # 게임 비용
    ticket_price = 10000

    if st.session_state.money < ticket_price:
        st.error("💸 돈이 부족합니다!")
        st.stop()

    if len(user_numbers) != 6:
        st.error("반드시 6개의 번호를 선택하세요!")

    else:

        # 티켓 구매
        st.session_state.money -= ticket_price

        # 게임 수 증가
        st.session_state.games += 1

        # 로또 생성
        lotto_numbers, bonus_number = generate_lotto_numbers()

        # 결과 계산
        matched, rank, prize = check_result(
            user_numbers,
            lotto_numbers
        )

        # 당첨금 지급
        st.session_state.money += prize

        if prize > 0:
            st.session_state.wins += 1

        # -----------------------------
        # 결과 출력
        # -----------------------------
        st.success("🎉 추첨 완료!")

        st.subheader("🎯 당첨 번호")
        draw_balls(lotto_numbers)

        st.subheader("⭐ 보너스 번호")
        draw_balls([bonus_number])

        st.subheader("🙋 내 번호")
        draw_balls(sorted(user_numbers))

        st.subheader("📊 게임 결과")

        st.markdown(f"""
        <div class="result-box">

        ✅ 맞춘 번호 개수: <b>{matched}개</b><br><br>

        🏆 등수: <b>{rank}</b><br><br>

        💰 획득 상금: <b>{prize:,}원</b>

        </div>
        """, unsafe_allow_html=True)

        # 랜덤 메시지
        messages = [

            "🍀 다음 판에는 더 좋은 결과가 있을 거예요!",
            "🔥 오늘 운이 좋네요!",
            "🎰 다시 도전해보세요!",
            "😎 로또 고수 인정!",
            "💎 대박의 기운이 느껴집니다!"
        ]

        st.info(random.choice(messages))

        # 이벤트 효과
        if matched == 6:
            st.balloons()
            st.snow()

# -----------------------------
# 게임 리셋
# -----------------------------
st.divider()

if st.button("🔄 게임 초기화"):

    st.session_state.money = 1000000
    st.session_state.games = 0
    st.session_state.wins = 0

    st.success("게임 데이터가 초기화되었습니다!")
