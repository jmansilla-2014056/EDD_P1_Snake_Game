import curses
import random
import time
from curses import textpad

from Game.Doublylinkedlist import DoublyLinkedList, Node


def create_food(snake, box):
    """Simple function to find coordinates of food which is inside box and not on snake body"""
    food = None
    while food is None:
        food = [random.randint(box[0][0] + 1, box[1][0] - 1),
                random.randint(box[0][1] + 1, box[1][1] - 1)]
        if food in snake:
            food = None
    return food


def create_poison(snake, box):
    """Simple function to find coordinates of food which is inside box and not on snake body"""
    poison = None
    while poison is None:
        poison = [random.randint(box[0][0] + 1, box[1][0] - 1),
                  random.randint(box[0][1] + 1, box[1][1] - 1)]
        if poison in snake:
            poison = None
    return poison


def gamer(stdscr):
    # initial settings
    global new_head
    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # create a game box
    sh = 30
    sw = 90
    box = [[3, 3], [sh - 3, sw - 3]]  # [[ul_y, ul_x], [dr_y, dr_x]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    linked_list = DoublyLinkedList()
    linked_list.insert_in_emptylist([sh // 2, sw // 2 + 1])
    linked_list.insert_at_start([sh // 2, sw // 2])
    linked_list.insert_at_start([sh // 2, sw // 2 - 1])

    # create snake and set initial direction
    snake = [[sh // 2, sw // 2 + 1], [sh // 2, sw // 2], [sh // 2, sw // 2 - 1]]
    direction = curses.KEY_RIGHT

    # draw snake
    for y, x in snake:
        stdscr.addstr(y, x, '#')

    n = linked_list.start_node
    f = 10
    g = 10
    while n is not None:
        stdscr.addstr(n.item[0], n.item[1], str(n.item))
        f = f + 3
        g = g + 3
        n = n.nref

    # create food
    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], '+')
    poison = create_poison(snake, box)
    stdscr.addstr(poison[0], poison[1], '*')

    # print score
    score = 0
    score_text = "Score: {}".format(score)
    stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text)

    while 1:
        # non-blocking input
        key = stdscr.getch()

        # set direction if user pressed any arrow key
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP]:
            direction = key

        # find next position of snake head
        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 1]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]
            time.sleep(0.1)
        elif direction == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]
            time.sleep(0.1)

        # insert and print new head time.sleep(0.5)
        stdscr.addstr(new_head[0], new_head[1], '#')
        snake.insert(0, new_head)

        # remove head in this coordinates

        # if sanke head is on food
        if snake[0] == food:

            # update score
            score += 1
            score_text = "Score: {}".format(score)
            stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text)

            # create new food
            food = create_food(snake, box)
            stdscr.addstr(food[0], food[1], '+')

            # increase speed of game
            stdscr.timeout(100 - (len(snake) // 3) % 90)
        elif snake[0] == poison:
            # update score
            score -= 1
            score_text = "Score: {}".format(score)
            stdscr.addstr(1, sw // 2 - len(score_text) // 2, score_text)

            temp = snake[len(snake) - 1]

            stdscr.addstr(temp[0], temp[1], '/')
            snake.pop(len(snake) - 1)

            # create new poison
            poison = create_poison(snake, box)
            stdscr.addstr(poison[0], poison[1], '*')

            # increase speed of game
            stdscr.timeout(100 - (len(snake) // 3) % 90)
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()
            stdscr.refresh()

        else:
            # shift snake's tail
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        # conditions for game over
        if (snake[0][0] in [box[0][0], box[1][0]] or
                snake[0][1] in [box[0][1], box[1][1]] or
                snake[0] in snake[1:]):
            msg = "Game Over!"

            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)

            while 1:
                key = stdscr.getch()
                if key == curses.KEY_ENTER or key in [10, 13]:
                    break

            stdscr.nodelay(0)
            stdscr.getch()
            break


class Snake:
    pass
