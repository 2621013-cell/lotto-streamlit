import random
import streamlit as st

# =====================================================
# 페이지 설정
# =====================================================
st.set_page_config(
    page_title="🎰 Ultimate Lotto RPG",
    page_icon="🎰",
    layout="centered"
)

# =====================================================
# CSS
# =====================================================
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
    font-weight:bold;
    margin:3px;
}

.yellow {background:#fbc400;}
.blue {background:#69c8f2;}
.red {background:#ff7272;}
.gray {background:#aaa;}
.green {background:#7cc576;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 초기값 (수정됨: 100만원 시작)
# =====================================================
defaults = {
    "money": 1000000,   # ✅ 변경
    "games": 0,
    "wins": 0,
    "ticket_price": 10000,
    "max_number": 45,
    "discount": False,
    "number_reduce": False,
    "fever": False,
    "fever_left": 0,
    "fever_count": 0,
    "auto": [],
    "show_shop": False,

    # ✅ 추가
    "double_money": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =====================================================
# 유틸
# =====================================================
def color(n):
    if n <= 10: return "yellow"
    if n <= 20: return "blue"
    if n <= 30: return "red"
    if n <= 40: return "gray"
    return "green"

def draw(nums):
    html = ""
    for n in nums:
        html += f'<div class="ball {color(n)}">{n}</div>'
    st.markdown(html, unsafe_allow_html=True)

# =====================================================
# 로또 생성
# =====================================================
def generate():
    nums = random.sample(range(1, st.session_state.max_number + 1), 7)
    return sorted(nums[:6]), nums[6]

# =====================================================
# 점수 계산
# =====================================================
def calc(user, lotto):
    m = len(set(user) & set(lotto))

    table = {
        6: ("1등", 2000000000),
        5: ("2등", 100000000),
        4: ("3등", 3000000),
        3: ("4등", 1000000),
        2: ("5등", 500000),
        1: ("참가", 50000),
        0: ("꽝", 0)
    }

    return m, *table[m]

# =====================================================
# 타이틀
# =====================================================
st.title("🎰 Lotto RPG")

st.metric("💰 돈", f"{st.session_state.money:,}")

st.divider()

# =====================================================
# 🛒 상점
# =====================================================
st.subheader("🛒 상점")

# 끝번호 아이템
if st.button("🎯 번호 1~30 제한 (10,000,000원)"):

    if st.session_state.money >= 10000000:
        st.session_state.money -= 10000000
        st.session_state.max_number = 30

# 반값 아이템
if st.button("💸 반값 아이템 (3,000,000원)"):

    if st.session_state.money >= 3000000:
        st.session_state.money -= 3000000
        st.session_state.ticket_price = max(
            100,
            st.session_state.ticket_price // 2
        )

# ⭐ 추가: 돈 2배 포션 (영구)
if not st.session_state.double_money:

    if st.button("💰 돈 2배 포션 (20,000,000원)"):

        if st.session_state.money >= 20000000:
            st.session_state.money -= 20000000
            st.session_state.double_money = True
            st.success("💰 모든 보상이 2배 됩니다!")

st.divider()

# =====================================================
# 자동 번호
# =====================================================
if st.button("🤖 자동 번호"):
    st.session_state.auto = sorted(
        random.sample(range(1, st.session_state.max_number + 1), 6)
    )

user = st.multiselect(
    f"1~{st.session_state.max_number}",
    list(range(1, st.session_state.max_number + 1)),
    default=st.session_state.auto,
    max_selections=6
)

# =====================================================
# 게임
# =====================================================
if st.button("🎲 뽑기"):

    price = st.session_state.ticket_price

    if st.session_state.money < price:
        st.error("돈 부족")
        st.stop()

    if len(user) != 6:
        st.error("6개 선택")
        st.stop()

    st.session_state.money -= price
    st.session_state.games += 1

    lotto, bonus = generate()

    m, rank, prize = calc(user, lotto)

    # ⭐ 핵심 추가: 2배 포션 적용
    if st.session_state.double_money:
        prize *= 2

    st.session_state.money += prize

    if prize > 0:
        st.session_state.wins += 1

    st.subheader("🎯 결과")

    draw(lotto)
    draw([bonus])
    draw(sorted(user))

    st.write(f"{m}개 | {rank} | {prize:,}원")

    if m == 6:
        st.balloons()

# =====================================================
# 리셋
# =====================================================
if st.button("🔄 초기화"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()
