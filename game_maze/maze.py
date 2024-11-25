import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt 
from time import time


def load_resources():
    background = cv.imread('./resource/background.jpg')
    maze = cv.imread('./resource/maze.jpg')
    player = cv.imread('./resource/player.jpg')
    return background, maze, player


def init_game(background, maze, player):
    state = background.copy()
    state[100:846, 150:1406, :] = maze
    cur_state = [170, 220]
    
    background[100:846, 150:1406, :] = maze

    return state, cur_state, background


BACKGROUND, MAZE, PLAYER = load_resources()
STATE, CUR_STATE, BACKGROUND = init_game(BACKGROUND, MAZE, PLAYER)


def draw_player():
    for i in range(PLAYER.shape[0]):
        for j in range(PLAYER.shape[1]):
            if PLAYER[i, j][0] < 200 or PLAYER[i, j][1] < 200 or PLAYER[i, j][2] < 200:
            # if sum(PLAYER[i, j]) < 600:
                STATE[CUR_STATE[0] - 25 + i, CUR_STATE[1] - 25 + j] = PLAYER[i, j]

draw_player()

def is_failed(
        cur_state,
        background, 
        start_time
):
    game_time = time() - start_time
    failed_area = 15
    for i in range(failed_area):
        if ((background[cur_state[0]+i, cur_state[1], 0] < 28) and (background[cur_state[0]+i, cur_state[1], 1] < 5) and (background[cur_state[0]+i, cur_state[1], 2] >130)):
            print(background[cur_state[0]+i, cur_state[1], :])
            return True
        elif ((background[cur_state[0], cur_state[1]+i, 0] < 28) and (background[cur_state[0], cur_state[1]+i, 1] < 5) and (background[cur_state[0], cur_state[1]+i, 2] >130)):
            print(background[cur_state[0], cur_state[1]+i, :])
            return True
        elif ((background[cur_state[0]-i, cur_state[1], 0] < 28) and (background[cur_state[0]-i, cur_state[1], 1] < 5) and (background[cur_state[0]-i, cur_state[1], 2] >130)):
            print(background[cur_state[0]-i, cur_state[1], :])
            return True
        elif ((background[cur_state[0], cur_state[1]-i, 0] < 28) and (background[cur_state[0], cur_state[1]-i, 1] < 5) and (background[cur_state[0], cur_state[1]-i, 2] >130)):
            print(background[cur_state[0], cur_state[1]-i, :])
            return True

        if sum(background[cur_state[0]+i, cur_state[1]]) < 20:
            print(background[cur_state[0]+i, cur_state[1]])
            return True
        elif sum(background[cur_state[0], cur_state[1]+i]) < 20:
            print(background[cur_state[0], cur_state[1]+i])
            return True
        elif sum(background[cur_state[0]-i, cur_state[1]]) < 20:
            print(background[cur_state[0]-i, cur_state[1]])
            return True
        elif sum(background[cur_state[0], cur_state[1]-i]) < 20:
            print(background[cur_state[0], cur_state[1]-i])
            return True

        
    if game_time > 60:
        return True 
        
    return False

def is_win(
        cur_state, 
        background
        ):
    win_area = 15
    for i in range(win_area):
        if background[cur_state[0]+i, cur_state[1], 1]>160 and (background[cur_state[0]+i, cur_state[1], 0] <  90) and (background[cur_state[0]+i, cur_state[1], 2] <  90):
            print(background[cur_state[0]+i, cur_state[1], :])
            return True
        elif background[cur_state[0], cur_state[1]+i, 1]>160 and (background[cur_state[0], cur_state[1]+i, 0] <  90) and (background[cur_state[0], cur_state[1]+i, 2] <  90):
            print(background[cur_state[0], cur_state[1]+i, :])
            return True
        elif background[cur_state[0]-i, cur_state[1], 1]>160 and (background[cur_state[0]-i, cur_state[1], 0] <  90) and (background[cur_state[0]-i, cur_state[1], 2] <  90):
            print(background[cur_state[0]-i, cur_state[1], :])
            return True
        elif background[cur_state[0], cur_state[1]-i, 1]>160 and (background[cur_state[0], cur_state[1]-i, 0] <  90) and (background[cur_state[0], cur_state[1]-i, 2] <  90):
            print(background[cur_state[0], cur_state[1]-i, :])
            return True
    
    return False



def update_state(
        direction, 
    ):
    step = 15
    if direction == 'right':
        CUR_STATE[1] += step
    elif direction == 'left':
        CUR_STATE[1] -= step
    elif direction == 'up':
        CUR_STATE[0] -= step
    elif direction == 'down':
        CUR_STATE[0] += step

    draw_player()


# def main():
start_time = time()

while True:
    cv.imshow( "Window", STATE)
    k = cv.waitKey(100)
    
    if k == 100: # right
        update_state('right')
    elif k == 97: # left
        update_state('left')
    elif k == 119: # up
        update_state('up')
    elif k == 115: # down
        update_state('down')
    elif k == 113 or k == 27:  # q or esc
        break

    if is_failed(CUR_STATE, BACKGROUND, start_time):
        print("Failed")
        failed = cv.imread('./resource/gameover_2.jpg')
        print(STATE.shape, failed.shape)
        STATE = failed
        cv.imshow("Window", STATE)

        cv.waitKey(0)
        break
        

    if is_win(CUR_STATE, BACKGROUND):
        print("You Win")
        win = cv.imread('./resource/win_2.jpg')
        STATE = win
        cv.imshow("Window", STATE)
        cv.waitKey(0)
        break
        

    timer = np.zeros((50, 250, 3))

    game_time = time() - start_time
    cv.putText(timer, f'Time: {int(60-game_time%60):02}', org=(10, 30), color=(0, 0, 255), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1)
    STATE[0:50, 0:250] = timer

cv.destroyWindow("Window")


# if __name__ == '__main__':
#     main()
