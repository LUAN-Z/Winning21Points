import random
from sys import exit

import numpy as np

cards = {
    "黑桃A": 1, "黑桃2": 2, "黑桃3": 3, "黑桃4": 4, "黑桃5": 5, "黑桃6": 6,
    "黑桃7": 7, "黑桃8": 8, "黑桃9": 9, "黑桃10": 10, "黑桃J": 10,
    "黑桃Q": 10, "黑桃K": 10,
    "红桃A": 1, "红桃2": 2, "红桃3": 3, "红桃4": 4, "红桃5": 5, "红桃6": 6,
    "红桃7": 7, "红桃8": 8, "红桃9": 9, "红桃10": 10, "红桃J": 10,
    "红桃Q": 10, "红桃K": 10,
    "方块A": 1, "方块2": 2, "方块3": 3, "方块4": 4, "方块5": 5, "方块6": 6,
    "方块7": 7, "方块8": 8, "方块9": 9, "方块10": 10, "方块J": 10,
    "方块Q": 10, "方块K": 10,
    "梅花A": 1, "梅花2": 2, "梅花3": 3, "梅花4": 4, "梅花5": 5, "梅花6": 6,
    "梅花7": 7, "梅花8": 8, "梅花9": 9, "梅花10": 10, "梅花J": 10,
    "梅花Q": 10, "梅花K": 10
}

poker = list(cards.keys())  # 1 deck of poker has 52 cards
poker_count = 1  # 1 deck
poker_list = poker * poker_count
ace_list = {"黑桃A", "红桃A", "方块A", "梅花A"}
total_score = np.array([0, 0])  # the score between player and pc, default 0:0.
game_round = 1  # the round of the game, default 1


def shuffle_cards(poker_list: list):
    """
    shuffling the poker cards

    Arguments:
        poker {list}
    """
    random.shuffle(poker_list)


def calculating_score(hand: list):
    """
    calculating the total score of the cards in your hand

    Arguments:
        hand {list} -- [the cards you have]
    """
    score = 0
    hasAce = False
    for card in hand:
        score += cards[card]

    for card in hand:
        if card in ace_list:
            hasAce = True
            break

    if hasAce and score <= 21 and score + 10 <= 21:
        score += 10

    return score


def who_win(player_score: int, pc_score: int):
    """
    Judging who wins the game, the side will get one point if wins.

    Arguments:
        player_score {int} -- [scores of your hand]
        pc_score {int} -- [score of pc's hand]

    Returns:
        [return the score between player and pc]
    """
    if player_score > 21 and pc_score > 21:
        print("{}:{} 平局".format(player_score, pc_score))
        return np.array([0, 0])

    elif player_score <= 21 and pc_score > 21:
        print("{}:{} 恭喜你，你赢了！".format(player_score, pc_score))
        return np.array([1, 0])

    elif player_score > 21 and pc_score <= 21:
        print("{}:{} 对不起, 你输了！".format(player_score, pc_score))
        return np.array([0, 1])

    elif player_score <= 21 and pc_score <= 21:
        if player_score < pc_score:
            print("{}:{} 对不起, 你输了！".format(player_score, pc_score))
            return np.array([0, 1])
        elif player_score == pc_score:
            print("{}:{} 平局".format(player_score, pc_score))
            return np.array([0, 0])
        else:
            print("{}:{} 恭喜你，你赢了！".format(player_score, pc_score))
            return np.array([1, 0])


def whether_ask_for_a_card():
    """
    whether add a new poker card to you hand
    """
    isAsking = input('是否加牌？(Y/N) >>->>->>->>-->:')
    if isAsking.upper() == "Y":
        return get_new_card()

    elif isAsking.upper() == "N":
        print("玩家停止叫牌")
        return False
    else:
        print("输入错误,请重新输入")
        whether_ask_for_a_card()


def get_new_card():
    """
    Add a new poker card into your hand
    when you get a new card the `poker_list` list will remove the card.
    """
    card = poker_list.pop(random.randint(0, len(poker_list) - 1))
    # print(card)
    return card


def continue_or_quit():
    """
    whether to start a new game

    Returns:
        bool -- [True]
    """
    isContinue = input('是否进行下一局游戏？(Y/N) >>->>->>->>-->:')
    if isContinue.upper() == "Y":
        if len(poker_list) < 45:
            print("现在有 {} 张牌, 剩余牌数太少, 游戏结束".format(len(poker_list)))
            exit(1)
        else:
            return True
    elif isContinue.upper() == "N":
        print("玩家结束游戏")
        exit(1)
    else:
        print("输入错误,请重新输入")
        continue_or_quit()


def initialize_the_game(current_poker_list: list):
    """
    Initializing the game

    [Divide two cards to player or pc]

    Arguments:
        current_poker_list {list} -- [Remaining poker cards]
    """
    return [
        current_poker_list.pop(random.randint(0, len(current_poker_list) - 1)),
        current_poker_list.pop(random.randint(0, len(current_poker_list) - 1))
    ]


def game_process(poker_list: list):
    """
    Define the game process

    Arguments:
        poker_list {np.array} -- [remaining poker cards list]
    """
    player_hand = []
    pc_hand = []
    player_init_hand = initialize_the_game(poker_list)
    player_init_hand_score = calculating_score(player_init_hand)
    pc_init_hand = initialize_the_game(poker_list)

    player_hand.extend(player_init_hand)
    print('你的初始手牌 {} {}'.format(player_init_hand, player_init_hand_score))

    pc_hand.extend(pc_init_hand)
    print('电脑的初始手牌 {} {}'.format('覆盖', pc_init_hand[0]))

    point = [calculating_score(player_hand), calculating_score(pc_hand)]
    # print('点数 {}'.format(point))

    if point[0] == 21 or point[1] == 21:
        return who_win(point[0], point[1])
    else:
        is21Point = False
        while point[0] <= 21:
            new_card = whether_ask_for_a_card()
            if is21Point is True:
                new_card = False
            if new_card is not False:
                player_hand.append(new_card)
                point[0] = calculating_score(player_hand)
                print('你的手牌为 {} {}'.format(player_hand, point[0]))
                if point[0] > 21:
                    print("爆点")
                    print('电脑的手牌为 {}'.format(pc_hand))
                    return who_win(point[0], point[1])
                elif point[0] == 21:
                    print("21点！")
                    is21Point = True
                    continue
                else:
                    continue
            elif new_card is False:
                while point[1] < point[0]:
                    new_card = get_new_card()
                    pc_hand.append(new_card)
                    pc_point = calculating_score(pc_hand)
                    point[1] = pc_point
                print('电脑的手牌为 {}'.format(pc_hand))
                return who_win(point[0], point[1])
            else:
                continue


while True:
    input("游戏开始，按‘回车’进入")
    print('现在是第 {} 轮, 剩余 {} 张牌'.format(game_round, len(poker_list)))
    shuffle_cards(poker_list)
    score = game_process(poker_list)
    total_score = np.add(total_score, score)
    print("本轮游戏结束，总比分为 玩家:电脑 {} : {}".format(
        total_score[0], total_score[1]))
    game_round += 1
    continue_or_quit()
