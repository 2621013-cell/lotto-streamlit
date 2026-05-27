import random

def generate_lotto_numbers():
    """
    로또 번호 (6개 메인 번호, 1개 보너스 번호)를 생성합니다.
    """
    # 1부터 45까지의 숫자 리스트 생성
    all_numbers = list(range(1, 46))

    # 섞기
    random.shuffle(all_numbers)

    # 메인 번호 6개 선택
    main_numbers = sorted(all_numbers[:6])

    # 보너스 번호 1개 선택 (메인 번호에 없는 숫자)
    bonus_number = all_numbers[6]

    return main_numbers, bonus_number

# 번호 생성 및 출력
main_nums, bonus_num = generate_lotto_numbers()

print(f"로또 메인 번호: {main_nums}")
print(f"보너스 번호: {bonus_num}")
