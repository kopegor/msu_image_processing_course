import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt 
from time import time

def load_resources():
    background = cv.imread('./resource/background.jpg')
    maze = cv.imread('./resource/maze.jpg')
    return background, maze


def init_game(background, maze):
    state = background.copy()
    state[91:659, 120:1125, :] = maze
    cur_state = [140, 160]
    state[cur_state[0]:cur_state[0]+10, cur_state[1]:cur_state[1]+10] = [255, 0, 0]
    
    background[91:659, 120:1125, :] = maze
    
    return state, cur_state, background


def is_failed(cur_state, background, start_time):
    game_time = time() - start_time
    if ((background[cur_state[0]+5, cur_state[1]+5, 0] ==  254) and (background[cur_state[0]+5, cur_state[1]+5, 1] ==  254) and (background[cur_state[0]+5, cur_state[1]+5, 2] ==  254)):
        return True
    elif ((background[cur_state[0]+5, cur_state[1]+5, 0] < 28) and (background[cur_state[0]+5, cur_state[1]+5, 1] < 5) and (background[cur_state[0]+5, cur_state[1]+5, 2] >130)):
        return True
    elif sum(background[cur_state[0]+5, cur_state[1]+5]) < 20:
        return True
    elif    game_time > 60:
        return True 
    return False


def is_win(cur_state, background):
    if background[cur_state[0]+5, cur_state[1]+5, 1]>160 and (background[cur_state[0]+5, cur_state[1]+5, 0] <  90) and (background[cur_state[0]+5, cur_state[1]+5, 2] <  90):
        return True
    return False


def update_state(state, cur_state, direction):
    if direction == 'right':
        cur_state[1] += 10
    elif direction == 'left':
        cur_state[1] -= 10
    elif direction == 'up':
        cur_state[0] -= 10
    elif direction == 'down':
        cur_state[0] +=10

    state[cur_state[0]:cur_state[0]+10, cur_state[1]:cur_state[1]+10] = [255, 0, 0]


def main():
    background, maze = load_resources()
    state, cur_state, background = init_game(background, maze)

    start_time = time()

    # init_background = state.copy()
    while True:
        cv.imshow( "Window", state)
        k = cv.waitKey(1)
        
        if k == 100: # right
            update_state(state, cur_state, 'right')
        elif k == 97: # left
            update_state(state, cur_state, 'left')
        elif k == 119: # up
            update_state(state, cur_state, 'up')
        elif k == 115: # down
            update_state(state, cur_state, 'down')
        elif k == 113 or k == 27:  # q or esc
            break
        if is_failed(cur_state, background, start_time):
            # cv.putText(background, 'Failed!', org=(350, 420), color=(0, 0, 255), fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=5)
            # display gameover image
            failed = cv.imread('./resource/gameover.jpg')
            cv.imshow("Window", failed)

            # cv.imshow("Window", background)
            cv.waitKey(0)
            break
        if is_win(cur_state, background):
            # cv.putText(background, 'You Win!', org=(350, 420), color=(0, 0, 255), fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=3)
            # cv.imshow("Window", background)
            win = cv.imread('./resource/win.jpg')
            cv.imshow("Window", win)
            cv.waitKey(0)
            break

        timer = np.zeros((50, 250, 3))

        game_time = time() - start_time
        cv.putText(timer, f'Time: {int(60-game_time%60):02}', org=(10, 30), color=(0, 0, 255), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1)
        state[0:50, 0:250] = timer

    cv.destroyWindow("Window")


if __name__ == '__main__':
    main()
