import random
import streamlit as st

# =====================================================
# PAGE
# =====================================================
st.set_page_config(
    page_title="🎰 로또 클리커",
    page_icon="🎰",
    layout="centered"
)

# =====================================================
# STYLE
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
.yellow{background:#fbc400;}
.blue{background:#69c8f2;}
.red{background:#ff7272;}
.gray{background:#aaa;}
.green{background:#7cc576;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# STATE
# =====================================================
defaults = {
    "money": 1000000,
    "games": 0,
    "wins": 0,
    "ticket_price": 10000,
    "max_number": 45,
    "auto": [],
    "double_money": False,

    # FEVER
    "fever": False,
    "fever_left": 0,
    "fever_count": 0,

    # ENDING
    "ending_unlocked": False,
    "ending_open": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =====================================================
# UTIL
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

def generate():
    nums = random.sample(range(1, st.session_state.max_number + 1), 7)
    return sorted(nums[:6]), nums[6]

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
# TITLE
# =====================================================
st.title("🎰 로또 클리커")

st.metric("💰 돈", f"{st.session_state.money:,}")
st.write(f"🎲 게임: {st.session_state.games} | 🏆 당첨: {st.session_state.wins}")

st.divider()

# =====================================================
# 🛒 SHOP (그대로 유지)
# =====================================================
st.subheader("🛒 상점")

if st.button("💸 반값 아이템 (3M)"):
    if st.session_state.money >= 3000000:
        st.session_state.money -= 3000000
        st.session_state.ticket_price = max(100, st.session_state.ticket_price // 2)

if st.button("🎯 1~30 제한 (10M)"):
    if st.session_state.money >= 10000000:
        st.session_state.money -= 10000000
        st.session_state.max_number = 30

if not st.session_state.double_money:
    if st.button("💰 2배 포션 (20M)"):
        if st.session_state.money >= 20000000:
            st.session_state.money -= 20000000
            st.session_state.double_money = True

st.divider()

# =====================================================
# AUTO
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
# 🎲 MULTI DRAW SYSTEM (핵심 추가)
# =====================================================
st.subheader("🎲 뽑기 배수 선택")

draw_mode = st.selectbox(
    "뽑기 개수 선택",
    ["1회", "100회", "300회"]
)

draw_count = {
    "1회": 1,
    "100회": 100,
    "300회": 300
}[draw_mode]

# =====================================================
# GAME
# =====================================================
if st.button("🎰 실행"):

    total_gain = 0

    for _ in range(draw_count):

        # ================= FEVER =================
        if st.session_state.fever:
            price = 0
            st.session_state.fever_left -= 1
        else:
            price = st.session_state.ticket_price

        if st.session_state.money < price:
            break

        st.session_state.money -= price
        st.session_state.games += 1

        # fever count
        if not st.session_state.fever:
            st.session_state.fever_count += 1

        if st.session_state.fever_count >= 100:
            st.session_state.fever = True
            st.session_state.fever_left = 50
            st.session_state.fever_count = 0

        if st.session_state.fever and st.session_state.fever_left <= 0:
            st.session_state.fever = False

        lotto, bonus = generate()
        m, rank, prize = calc(user, lotto)

        if st.session_state.double_money:
            prize *= 2

        st.session_state.money += prize
        total_gain += prize

        if prize > 0:
            st.session_state.wins += 1

    st.success(f"🎰 {draw_count}회 완료!")

    st.write(f"💰 총 획득: {total_gain:,}원")

    draw(lotto)
    draw([bonus])

# =====================================================
# 🏁 ENDING
# =====================================================
st.divider()

if st.session_state.money >= 100000000000:
    st.session_state.ending_unlocked = True

st.subheader("🏁 엔딩")

if st.session_state.ending_unlocked:

    if st.button("🎬 엔딩 보기"):
        st.session_state.ending_open = True

if st.session_state.ending_open:

    st.success("🏆 엔딩 도달!")

    col1, col2 = st.columns(2)

    if col1.button("🔁 이어하기"):
        st.session_state.ending_open = False

    if col2.button("🔄 처음부터"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# =====================================================
# RESET + COUNT 유지 초기화
# =====================================================
st.divider()

if st.button("🔄 초기화"):

    keep_keys = ["double_money"]  # 유지하고 싶은 것만 남김

    for k in list(st.session_state.keys()):
        if k not in keep_keys:
            del st.session_state[k]

    st.rerun()
