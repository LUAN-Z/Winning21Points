# -*- coding: utf-8 -*-
import random

import pygame

pygame.init()

# set screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
POKER_WIDTH = 125
POKER_HEIGHT = 181
# color (r, g, b)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (186, 238, 110)
GREEN = (11, 238, 7)
LIGHT_RED = (209, 101, 69)
RED = (230, 37, 33)
JUDGEMENT_COLOR = (205, 134, 157)
# start interface widgets position (x, y, w, h)
START_BUTTON_POSITION = (125, 330, 150, 60)
QUIT_BUTTON_POSITION = (515, 330, 150, 60)
# gaming interface widgets position
GET_BUTTON_POSITION = (666, 345, 100, 40)
STOP_BUTTON_POSITION = (666, 415, 100, 40)
SCORE_POSITION = (360, 250, 80, 35)
# gaming continue interface widgets position
CONTINUE_BUTTON_POSITION = (175, 250, 150, 60)
SEC_QUIT_BUTTON_POSITION = (475, 250, 150, 60)
# gaming judging interface widgets position
PC_SCORE_POSITION = (350, 90, 100, 40)
PLAYER_SCORE_POSITION = (350, 370, 100, 40)
JUDGE_RECT_POSITION = (250, 160, 300, 100)
JUDGE_TEXT_POSITION = (280, 120, 250, 200)
JUDGE_BUTTON_POSITION = (350, 250, 100, 50)

# poker cards
CARDS = {
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
ACE_LIST = ["黑桃A", "红桃A", "方块A", "梅花A"]
# font style
LARGE_TEXT_STYLE = pygame.font.SysFont("Vineta BT", 100)
CORBEL = pygame.font.SysFont("Corbel", 40)
SMALL_TEXT_STYLE = pygame.font.SysFont("Yahei", 40, True)
SCORE_STYLE = pygame.font.SysFont("Menlo", 40)
JUDGE_STYLE = pygame.font.SysFont("Corbel", 110, True)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# set screen title
pygame.display.set_caption(u'Winning 21 Points')
# gaming timer
clock = pygame.time.Clock()
# background image
background = pygame.image.load('./card/table.jpg')
poker = pygame.image.load('./card/4ace.png')
icon = pygame.image.load('./card/icon.png')
pygame.display.set_icon(icon)
screen.blit(background, (0, 0))
pygame.display.update()

poker_list = list(CARDS.keys())
isClickSure = True
isGameOver = False
isStopAsking = False


def shuffle_cards():
    """
    Shuffling cards

    [Disordering the order of `poker_list`]
    """
    global poker_list
    poker_list = list(CARDS.keys())
    random.shuffle(poker_list)


def divide_two_cards(current_poker_list: list):
    """
    Initializing the hand

    [Divide two cards to player or pc]

    Arguments:

        current_poker_list {list} -- [Remaining poker cards]
    """
    return [
        current_poker_list.pop(random.randint(0, len(current_poker_list) - 1)),
        current_poker_list.pop(random.randint(0, len(current_poker_list) - 1))
    ]


def get_new_card(hand: list):
    """
    Add a new poker card into your hand

    [when you get a new card the `poker_list` list will remove the it.]
    """
    card = poker_list.pop(random.randint(0, len(poker_list) - 1))
    hand.append(card)


def calculate_score(hand: list):
    """
    calculating the total score of the cards in your hand

    Arguments:

        hand {list} -- [the cards you have]
    """
    score = 0
    hasAce = False
    for card in hand:
        score += CARDS[card]

    for card in hand:
        if card in ACE_LIST:
            hasAce = True
            break

    if hasAce and score <= 21 and score + 10 <= 21:
        score += 10

    return score


def refresh():
    """
    update the gaming interface images
    """
    pygame.display.update()
    clock.tick(30)


def quit_game():
    """
    quitting the game and closing the window
    """
    pygame.quit()
    quit()


def text_render(text: str, font: pygame.font.SysFont, color: tuple):
    """
    rerendering the text with new font and color

    Arguments:

        text {str} -- [text]
        font {pygame.font.SysFont} -- [pygame.font.SysFont font]
        color {tuple} -- [(r, g, b)]

    Returns:
        [type] -- [surface and rectangle]
    """
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def button(text: str, position: tuple, color: tuple, hover_color: tuple,
           callback=None, *args):
    """
    Drawing a button on screen

    Arguments:

        text {str} -- [the text display on the button]
        position {tuple} -- [the button size (x, y, w, h)]
        color {tuple} -- [the button inactive color]
        hover_color {tuple} -- [button active color]

    Keyword Arguments:

        callback {function} -- [callback function] (default: {None})
        *args {} [callback function parameter]
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    left = position[0]
    right = position[0] + position[2]
    top = position[1]
    bottom = position[1] + position[3]
    if left <= mouse[0] <= right and top <= mouse[1] <= bottom:
        pygame.draw.rect(screen, hover_color, position)
        if click[0] == 1 and callback is not None:
            pygame.time.delay(500)
            if callback.__name__ in ['quit_game',
                                     'game_main_interface',
                                     'continue_next_round']:
                callback()
            elif callback.__name__ == 'get_new_card':
                callback(args[0])
            elif callback.__name__ == 'settlement':
                callback(args[0], args[1])
            else:
                callback()
    else:
        pygame.draw.rect(screen, color, position)
    button_surface, button_rect = text_render(text, SMALL_TEXT_STYLE, WHITE)
    button_rect.center = ((left + right) / 2, (top + bottom) / 2)
    screen.blit(button_surface, button_rect)


def display_text(text: str, font_style: pygame.font.SysFont, position: tuple,
                 text_color: tuple, withBackground=False, *args):
    """
    display text on the screen

    Arguments:

        text {str} -- [text]
        font_style {pygame.font.SysFont} -- [font]
        position {tuple} -- [text rectangle position (x, y, w, h)]
        text_color {tuple} -- [text color (r, g, b)]
        background_color {tuple} -- [rectangle color (r, g, b)]
    """
    if withBackground:
        pygame.draw.rect(screen, args[0], position)
    button_surface, button_rect = text_render(text, font_style, text_color)
    button_rect.center = (position[0] + position[2] / 2,
                          position[1] + position[3] / 2)
    screen.blit(button_surface, button_rect)


def display_single_card(poker_name: str, x: int, y: int):
    """
    Displaying a poker image on the screen at specific position

    [Loading an image from `./card` with specific image name `poker_name.png`\
    and display it on screen]

    Arguments:

        poker_name {str} -- [poker card name]
        x {int} -- [the x axis value of lefttop position]
        y {int} -- [the y axis value of lefttop position]
    """
    poker = pygame.image.load('./card/' + poker_name + '.png')
    screen.blit(poker, (x, y))


def display_multiple_cards(hand: list, role: int):
    """
    displaying poker card image in the screen

    [displaying the relative images of the cards
        on the top or bottom of the screen]

    Arguments:

        hand {list} -- [the cards you have]\n
        role {int} -- [player: 1 or pc: 0,
                       if role == 1, displaying images on the top of the seceen
                       if role == 0, displaying images on the bottom
   """
    if role == 1:  # player
        img_y = 300
    else:  # pc
        img_y = 20
    cards_amount = len(hand)
    half_stack_cards_width = POKER_WIDTH * (cards_amount + 1) / 4
    stack_cards_x = SCREEN_WIDTH / 2 - half_stack_cards_width
    for i in range(cards_amount):
        display_single_card(hand[i],
                            stack_cards_x + int(POKER_WIDTH / 2) * i, img_y)


def settlement(player_hand: list, pc_hand: list):
    """
    The pc judges whether to get cards according to your points and
    makes a score decision.

    Arguments:

    """
    global isStopAsking
    isStopAsking = True
    while isStopAsking:
        screen.blit(background, (0, 0))
        display_multiple_cards(player_hand, 1)
        display_multiple_cards(pc_hand, 0)
        refresh()
        player_hand_point = calculate_score(player_hand)
        if player_hand_point == 21:
            display_text(str(player_hand_point), SCORE_STYLE,
                         PLAYER_SCORE_POSITION, WHITE, True, GREEN)
        pc_hand_point = calculate_score(pc_hand)
        while pc_hand_point < player_hand_point:
            get_new_card(pc_hand)
            display_multiple_cards(pc_hand, 0)
            pc_hand_point = calculate_score(pc_hand)
            refresh()
            pygame.time.delay(500)
        if player_hand_point > 21 and pc_hand_point > 21:
            judgement = 'DRAW'

        elif player_hand_point <= 21 and pc_hand_point > 21:
            judgement = "YOU WIN"

        elif player_hand_point > 21 and pc_hand_point <= 21:
            judgement = "YOU LOSE"
        elif player_hand_point <= 21 and pc_hand_point <= 21:
            if player_hand_point < pc_hand_point:
                judgement = "YOU LOSE"

            elif player_hand_point == pc_hand_point:
                judgement = 'DRAW'

            else:
                judgement = "YOU WIN"
        isStopAsking = False
        pygame.time.delay(1000)
        game_confirm_interface(player_hand, pc_hand, judgement)


def continue_next_round():
    global isSettle, isClickSure
    isClickSure = False
    isContinue = True
    screen.blit(background, (0, 0))
    while isContinue:
        screen.blit(poker, (SCREEN_WIDTH / 9 * 2, SCREEN_HEIGHT / 4))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isContinue = False
                quit_game()
        button("Again", CONTINUE_BUTTON_POSITION, LIGHT_GREEN,
               GREEN, game_main_interface)
        button("Quit", SEC_QUIT_BUTTON_POSITION, LIGHT_RED, RED,
               quit_game)
        refresh()
    isSettle = False


def game_initial_interface():
    """
    Gaming initial interface
    """
    atInitInterface = True
    while atInitInterface:
        screen.blit(poker, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 14 * 5))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                atInitInterface = False
                quit_game()
        text_surface, text_rect = text_render(u"Winning 21 Points",
                                              LARGE_TEXT_STYLE, WHITE)
        text_rect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 3))
        shadow_text_surface, shadow_text_rect = text_render(
            u"Winning 21 Points", LARGE_TEXT_STYLE, GRAY)
        shadow_text_rect.center = ((SCREEN_WIDTH / 2 + 10),
                                   (SCREEN_HEIGHT / 3))
        screen.blit(shadow_text_surface, shadow_text_rect)
        screen.blit(text_surface, text_rect)
        button(u"Start", START_BUTTON_POSITION, LIGHT_GREEN,
               GREEN, game_main_interface)
        button("Quit", QUIT_BUTTON_POSITION, LIGHT_RED,
               RED, quit_game)
        refresh()


def game_confirm_interface(player_hand: list, pc_hand: list, judgement: str):
    """
    displaying the final score and who wins
    """
    isClickSure = True
    player_score = calculate_score(player_hand)
    pc_score = calculate_score(pc_hand)
    if judgement == 'YOU WIN':
        player_score_color = GREEN
        pc_score_color = RED
        judgement_color = (238, 43, 82)
    elif judgement == 'YOU LOSE':
        player_score_color = RED
        pc_score_color = GREEN
        judgement_color = (64, 64, 64)
    else:
        player_score_color = pc_score_color = YELLOW
        judgement_color = (110, 196, 145)

    screen.blit(background, (0, 0))
    display_multiple_cards(player_hand, 1)
    display_multiple_cards(pc_hand, 0)
    display_text(str(player_score), SCORE_STYLE, PLAYER_SCORE_POSITION,
                 WHITE, True, player_score_color)
    display_text(str(pc_score), SCORE_STYLE, PC_SCORE_POSITION,
                 WHITE, True, pc_score_color)
    pygame.time.delay(1000)
    refresh()
    pygame.time.delay(1000)
    display_text(judgement, JUDGE_STYLE, JUDGE_TEXT_POSITION, judgement_color)
    while isClickSure:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isClickSure = False
                quit_game()
        button("OK", JUDGE_BUTTON_POSITION, LIGHT_GREEN, GREEN,
               continue_next_round)
        refresh()


def game_main_interface():
    """
    Gaming loop interface
    """
    screen.blit(background, (0, 0))
    shuffle_cards()
    isGameOver = False
    player_hand = []
    pc_hand = []
    player_init_hand = divide_two_cards(poker_list)
    player_hand.extend(player_init_hand)
    player_init_hand_score = calculate_score(player_init_hand)
    display_text(str(player_init_hand_score), CORBEL, SCORE_POSITION,
                 WHITE, True, BLACK)
    pc_init_hand = divide_two_cards(poker_list)
    pc_hand.extend(pc_init_hand)
    while not isGameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGameOver = True
                quit_game()
        player_hand_point = calculate_score(player_hand)
        display_text(str(player_hand_point), CORBEL, SCORE_POSITION,
                     WHITE, True, BLACK)
        if calculate_score(player_hand) == 21:
            settlement(player_hand, pc_hand)

        button("Get", GET_BUTTON_POSITION, LIGHT_GREEN,
               GREEN, get_new_card, player_hand)
        if calculate_score(player_hand) > 21:
            game_confirm_interface(player_hand, pc_hand, "YOU LOSE")
        button("Stop", STOP_BUTTON_POSITION, LIGHT_RED,
               RED, settlement, player_hand, pc_hand)

        display_multiple_cards(player_hand, 1)
        display_single_card('back', 307, 20)
        display_single_card(pc_hand[0], 371, 20)
        refresh()


if __name__ == '__main__':
    game_initial_interface()
    quit_game()
