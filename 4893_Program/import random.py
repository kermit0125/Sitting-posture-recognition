import random

def get_user_choice():
    print("请输入你的选择：石头（1）、剪刀（2）、布（3）")
    user_choice = input()
    while user_choice not in ['1', '2', '3']:
        print("输入无效，请重新输入：")
        user_choice = input()
    return int(user_choice)

def get_computer_choice():
    return random.randint(1, 3)

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "平局"
    elif (user_choice == 1 and computer_choice == 2) or \
         (user_choice == 2 and computer_choice == 3) or \
         (user_choice == 3 and computer_choice == 1):
        return "你赢了！"
    else:
        return "计算机赢了。"

def main():
    print("欢迎来到石头剪刀布游戏！")
    
    while True:
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()

        print(f"你的选择: {user_choice}")
        print(f"计算机的选择: {computer_choice}")

        result = determine_winner(user_choice, computer_choice)
        print(result)

        print("是否继续游戏？(y/n)")
        play_again = input()
        if play_again.lower() != 'y':
            break

if __name__ == "__main__":
    main()
