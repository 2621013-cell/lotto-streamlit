import random
import streamlit as st

# =====================================================
# 페이지 설정
# =====================================================
st.set_page_config(
    page_title="🎰 Ultimate Lotto Evolution",
    page_icon="🎰",
    layout="centered"
)

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>
.ball{
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

.card{
    padding:15px;
    background:#f5f5f5;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 초기 상태
# =====================================================
if "money" not in st.session_state:
    st.session_state.money = 100000

if "games" not in st.session_state:
    st.session_state.games = 0

if "wins" not in st.session_state:
    st.session_state.wins = 0

if "shop_price" not in st.session_state:
    st.session_state.shop_price = 3000000

if "ticket_discount" not in st.session_state:
    st.session_state.ticket_discount = False

if "number_limit" not in st.session_state:
    st.session_state.number_limit = 45

if "fever_counter" not in st.session_state:
    st.session_state.fever_counter = 0

if "fever_mode" not in st.session_state:
    st.session_state.fever_mode = False

if "fever_left" not in st.session_state:
    st.session_state.fever_left = 0

if "clear_count" not in st.session_state:
    st.session_state.clear_count = 0

if "ending" not in st.session_state:
    st.session_state.ending = False

# =====================================================
# 번호 색상
# =====================================================
def color(n):
    if n <= 10: return "yellow"
    if n <= 20: return "blue"
    if n <= 30: return "red"
    if n <= 40: return "gray"
    return "green"

# =====================================================
# 공 출력
# =====================================================
def draw(nums):
    html = ""
    for n in nums:
        html += f'<div class="ball {color(n)}">{n}</div>'
    st.markdown(html, unsafe_allow_html=True)

# =====================================================
# 로또 생성
# =====================================================
def generate():
    maxn = st.session_state.number_limit
    data = random.sample(range(1, maxn + 1), 7)
    return sorted(data[:6]), data[6]

# =====================================================
# 당첨 계산 (10배 반영)
# =====================================================
def calc(nums, lotto):
    m = len(set(nums) & set(lotto))

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
# 엔딩 체크
# =====================================================
def check_ending():
    return st.session_state.money >= 100000000000  # 1000억

# =====================================================
# 타이틀
# =====================================================
st.title("🎰 Lotto Evolution Game")

st.metric("💰 돈", f"{st.session_state.money:,}원")

st.write(f"게임: {st.session_state.games} | 피버카운트: {st.session_state.fever_counter}")

# =====================================================
# 엔딩 시스템
# =====================================================
if st.session_state.ending:
    st.success("🏁 엔딩 도달!")

    st.write("당신은 로또 제국을 완성했습니다.")

    if st.button("🔁 이어서 하기"):
        st.session_state.ending = False

    if st.button("🔄 처음부터"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.stop()

# =====================================================
# 상점
# =====================================================
if st.button("🛒 상점"):

    st.session_state.show_shop = not st.session_state.get("show_shop", False)

if st.session_state.get("show_shop", False):

    st.subheader("🛒 상점")

    st.write(f"반값 아이템 가격: {st.session_state.shop_price:,}원")

    if st.button("💸 반값 아이템 구매"):

        if st.session_state.money >= st.session_state.shop_price:

            st.session_state.money -= st.session_state.shop_price

            st.session_state.ticket_discount = True

            st.session_state.shop_price = max(
                100,
                int(st.session_state.shop_price * 0.5)
            )

            st.success("구매 완료!")

        else:
            st.error("돈 부족!")

    if st.button("🚪 상점 닫기"):
        st.session_state.show_shop = False

st.divider()

# =====================================================
# 자동 번호
# =====================================================
if st.button("🤖 자동 번호"):
    st.session_state.auto = sorted(
        random.sample(range(1, st.session_state.number_limit + 1), 6)
    )

nums = st.multiselect(
    f"1~{st.session_state.number_limit}",
    list(range(1, st.session_state.number_limit + 1)),
    default=st.session_state.get("auto", []),
    max_selections=6
)

# =====================================================
# 게임 실행
# =====================================================
if st.button("🎲 뽑기"):

    # -----------------------------
    # 피버 시스템
    # -----------------------------
    if st.session_state.fever_mode:
        st.session_state.fever_left -= 1
        ticket_price = 0
    else:
        ticket_price = 10000 if not st.session_state.ticket_discount else 5000

    if st.session_state.money < ticket_price:
        st.error("돈 부족")
        st.stop()

    if len(nums) != 6:
        st.error("6개 선택")
        st.stop()

    # 지불
    st.session_state.money -= ticket_price

    # 피버 증가 (피버 아닐 때만)
    if not st.session_state.fever_mode:
        st.session_state.fever_counter += 1

    # 피버 발동
    if st.session_state.fever_counter >= 100 and not st.session_state.fever_mode:
        st.session_state.fever_mode = True
        st.session_state.fever_left = 50
        st.session_state.fever_counter = 0
        st.success("🔥 피버타임 시작!")

    # 피버 종료
    if st.session_state.fever_mode and st.session_state.fever_left <= 0:
        st.session_state.fever_mode = False

    # 생성
    lotto, bonus = generate()

    m, rank, prize = calc(nums, lotto)

    # 10배 적용
    prize *= 10

    st.session_state.money += prize

    st.session_state.games += 1

    if prize > 0:
        st.session_state.wins += 1

    # 엔딩 체크
    if check_ending():
        st.session_state.ending = True

    # 출력
    st.success("결과")

    draw(lotto)
    draw([bonus])
    draw(sorted(nums))

    st.write(f"{m}개 맞음 | {rank} | {prize:,}원")

    if st.session_state.fever_mode:
        st.warning(f"🔥 피버타임 남은 횟수: {st.session_state.fever_left}")

    if m == 6:
        st.balloons()

# =====================================================
# 리셋
# =====================================================
if st.button("🔄 초기화"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()
