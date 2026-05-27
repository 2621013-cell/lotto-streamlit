import random
import time
import streamlit as st

# =====================================================
# PAGE
# =====================================================
st.set_page_config(
    page_title="🎰 Lotto RPG",
    page_icon="🎰",
    layout="centered"
)

# =====================================================
# UI STYLE (모바일 느낌)
# =====================================================
st.markdown("""
<style>

body {
    background-color: #f4f6f8;
}

.title {
    text-align:center;
    font-size:38px;
    font-weight:bold;
    color:#ffcc00;
}

.card {
    background:white;
    padding:15px;
    border-radius:15px;
    margin:10px 0;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
}

.ball {
    display:inline-block;
    width:50px;
    height:50px;
    border-radius:50%;
    text-align:center;
    line-height:50px;
    color:white;
    font-weight:bold;
    margin:3px;
}

.yellow{background:#fbc400;}
.blue{background:#69c8f2;}
.red{background:#ff7272;}
.gray{background:#aaa;}
.green{background:#7cc576;}

button {
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# INIT STATE
# =====================================================
defaults = {
    "money": 100000,
    "games": 0,
    "wins": 0,
    "ticket_price": 10000,
    "max_number": 45,
    "discount": False,
    "number_reduce": False,
    "fever": False,
    "fever_left": 0,
    "fever_count": 0,
    "ending": False,
    "ending_open": False,
    "auto": []
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =====================================================
# COLOR
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
# LOTTO
# =====================================================
def generate():
    nums = random.sample(range(1, st.session_state.max_number+1), 7)
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
st.markdown('<div class="title">🎰 Lotto RPG</div>', unsafe_allow_html=True)

# =====================================================
# STATUS UI
# =====================================================
st.markdown("### 💰 상태")

col1,col2,col3 = st.columns(3)
col1.metric("돈", f"{st.session_state.money:,}")
col2.metric("게임", st.session_state.games)
col3.metric("당첨", st.session_state.wins)

# =====================================================
# ENDING SYSTEM
# =====================================================
if st.session_state.money >= 100000000000:
    st.session_state.ending = True

if st.session_state.ending:

    st.success("🏁 엔딩 도달!")

    if st.button("🎬 엔딩 보기"):
        st.session_state.ending_open = True

    if st.session_state.ending_open:

        st.markdown("""
        <div class="card">
        👑 당신은 로또 세계의 지배자가 되었습니다.<br>
        모든 확률을 지배했습니다.
        </div>
        """, unsafe_allow_html=True)

        col1,col2 = st.columns(2)

        if col1.button("🔁 이어하기"):
            st.session_state.ending_open = False
            st.session_state.ending = False

        if col2.button("🔄 처음부터"):

            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    st.stop()

# =====================================================
# SHOP
# =====================================================
st.subheader("🛒 상점")

if st.button("💸 반값 아이템 (3M)"):
    if st.session_state.money >= 3000000:
        st.session_state.money -= 3000000
        st.session_state.ticket_price = max(100, int(st.session_state.ticket_price * 0.5))

if st.button("🎯 번호 제한 (30)"):
    if st.session_state.money >= 10000000:
        st.session_state.money -= 10000000
        st.session_state.max_number = 30

st.divider()

# =====================================================
# AUTO
# =====================================================
if st.button("🤖 자동 번호"):
    st.session_state.auto = sorted(
        random.sample(range(1, st.session_state.max_number+1), 6)
    )

user = st.multiselect(
    f"1~{st.session_state.max_number}",
    list(range(1, st.session_state.max_number+1)),
    default=st.session_state.auto,
    max_selections=6
)

# =====================================================
# GAME
# =====================================================
if st.button("🎲 뽑기"):

    price = st.session_state.ticket_price

    # fever
    if st.session_state.fever:
        price = 0
        st.session_state.fever_left -= 1

    if st.session_state.money < price:
        st.error("돈 부족")
        st.stop()

    if len(user) != 6:
        st.error("6개 선택")
        st.stop()

    st.session_state.money -= price
    st.session_state.games += 1

    # fever trigger
    if not st.session_state.fever:
        st.session_state.fever_count += 1

    if st.session_state.fever_count >= 100:
        st.session_state.fever = True
        st.session_state.fever_left = 50
        st.session_state.fever_count = 0
        st.success("🔥 피버타임!")

    if st.session_state.fever and st.session_state.fever_left <= 0:
        st.session_state.fever = False

    lotto, bonus = generate()
    m, rank, prize = calc(user, lotto)

    prize *= 10  # 10배 시스템

    st.session_state.money += prize

    if prize > 0:
        st.session_state.wins += 1

    st.subheader("🎯 결과")

    draw(lotto)
    draw([bonus])
    draw(sorted(user))

    st.write(f"{m}개 | {rank} | {prize:,}원")

    if st.session_state.fever:
        st.warning(f"🔥 피버 남은: {st.session_state.fever_left}")

    if m == 6:
        st.balloons()

# =====================================================
# RESET
# =====================================================
st.divider()

if st.button("🔄 리셋"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()
