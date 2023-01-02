import random
# TODO STEP1
MAX_INPUT_TITLE_LEN = 28
msg = f"게임 제목을 최대 {MAX_INPUT_TITLE_LEN}자 이내로 영문, 숫자 조합으로 입력하세요(한글검사x):\n"
while True:
  player_input_title = input(msg).strip()

  if not player_input_title:
    print('정상적으로 입력하세요')
    continue
  elif len(player_input_title) > MAX_INPUT_TITLE_LEN:
    print(f'입력하신 제목은 {len(player_input_title)-MAX_INPUT_TITLE_LEN}자 초과하였습니다.')
    continue
  else:
    break

# TODO STEP 2
MAX_INPUT_PLAYER_NAME_LEN = MAX_INPUT_TITLE_LEN
msg = f"플레이어의 이름을 최대 {MAX_INPUT_PLAYER_NAME_LEN}자 이내로 영문, 숫자 조합으로 입력하세요(한글검사x):\n"
while True:
  player_input_name = input(msg).strip()

  if not player_input_name:
    print('정상적으로 입력하세요')
  elif len(player_input_name) > MAX_INPUT_PLAYER_NAME_LEN:
    print(
        f'입력하신 이름은 {len(player_input_name)-MAX_INPUT_PLAYER_NAME_LEN}자 초과하였습니다.')
  else:
    break

# TODO STEP 3
# 더미 데이터
player_input_title = 'Number Match Game'
player_input_name = 'Guest Pro'
tmp = 'VER 1.0.0'

# 한번에 출력하기
input_text = f'''

------------------------------
-{player_input_title:^28}-
-{player_input_name:^28}-
-         VER 1.0.0          -
------------------------------

'''

print(input_text)

# 밑에 while은 맨 밑에서 진행여부때문에 다시 만들어준거
# 게임 진행 여부를 블린형 변수로 관리한다.
is_game_play = True
while is_game_play:
    # TODO STEP 4
    # 모듈 가져오기
    ai_number = random.randint(1, 100)
    print(f'ai답은 {ai_number}이다.')
    # 사용자 시도 횟수 변수 초기화
    player_try_count = 0  # 초기화

    # 사용자가 입력한 값과 ai값과 비교한다.(작다,크다,같다)
    '''
    ai값과 비교한다ㅇㄻ
    ai값보다 입력값이 작으면 작다, 크면 크다 출력
    값이 동일하면, 몇번만에 맞췄다고 표시하고
    플레이어가 숫자를 입력한 횟수를 기억해야 한다.
    맞추면
    점수 출력 (10-시도횟수)*10

    '''

    while True:
        while True:

            msg = '1~100사이 값을 넣으시오\n'
            player_number = input(msg).strip()

            if not player_number:
                print('정확하게 입력하세요')
            elif not player_number.isnumeric():
                print('숫자만 입력하세요')
            else:
                player_number = int(player_number)
                if (player_number < 1) or (player_number > 100):
                # print(msg) --> 입력 프럼프트와 동일한 메시지 므로 생략
                    continue

                break

        # 사용자 입력 카운트 증가(+1)

        player_try_count += 1

        if player_number > ai_number:
            print('선택하는 숫자가 정답보다 큽니다. 숫자를 줄여주세요.')
        elif player_number < ai_number:
            print('선택하신 숫자가 정답보다 작습니다. 숫자를 키워주세요.')
        else:
            print('정답입니다. 축하드립니다.')
            break #맨앞 While로 감 71번줄은 나랑 서열 같은거다

        # 점수 출력 : (10-시도횟수)*10
        # 10회 이상 시도 횟수가 초과되면 게임 오버 출력
    if player_try_count >= 10: print('게임오버')
    else: print(f'게임 클리어\n{player_input_name}님의 점수는 {(10-player_try_count)*10}입니다.')

    # TODO STEP 6

    # 다시 게임할것인지 물어보고 다시하면(y) step 4부터 진행
    # 끝낸다고 하면(n) 다음 메시지 출력하고 종료
    # 엉뚱한 답을 하거나, 빈값이거나 동등이면 메시지 하나로 통일(정확하게 입력하세요)
    while True:
        msg = "다시 도전하시겠습니까?"
        player_answer = input(msg).strip().lower()
        if player_answer == 'y':
            break
        elif player_answer == 'n':
            is_game_play = False
            break
        else: #모든 오류사항
            print('정확하게 입력하세요.')

print('bye~ bye~')