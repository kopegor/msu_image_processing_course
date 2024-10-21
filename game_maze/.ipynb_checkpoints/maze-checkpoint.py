import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt 


cv.startWindowThread()

fontFace = cv.FONT_HERSHEY_DUPLEX
thickness = 2


background = cv.imread('./resource/background.jpg')

maze = cv.imread('./resource/maze.jpg')

print(background.shape, maze.shape)

state = background.copy()
state[71:400, 70:729, :] = maze


background[71:400, 70:729, :] = maze

# state[105, 90, :] = [0, 0, 0]
cur_state = [95, 95]
state[cur_state[0]:cur_state[0]+10, cur_state[1]:cur_state[1]+10] = [255, 0, 0]



# cv.putText(state, 'O', org=tuple(cur_state), color=(255, 0, 0), fontFace=fontFace, fontScale=0.5)
# state[cur_state[0], cur_state[1]] = [255, 255, 255]

# print(cv.waitKey(0))
# print(state[cur_state[0], cur_state[1]])


while True:
    
    cv.imshow( "Window", state)
    print(f"color state: {state[cur_state[0], cur_state[1]]}")
    
    if ((background[cur_state[0], cur_state[1], 0] ==  254) and (background[cur_state[0], cur_state[1], 1] ==  254) and (background[cur_state[0], cur_state[1], 2] ==  254)):
        print(state[cur_state[0], cur_state[1]])
        print(cur_state)
        cv.putText(background, 'Failed!', org=(150, 220), color=(0, 0, 255), fontFace=fontFace, fontScale=5)
        cv.imshow("Window", background)
        cv.waitKey(0)
        break
        
    # if ((background[cur_state[0], cur_state[1], 0] ==  75) and (background[cur_state[0], cur_state[1], 1] ==  177) and (background[cur_state[0], cur_state[1], 2] ==  35)):
    if np.argmax(background[cur_state[0], cur_state[1]]) == 1 and background[cur_state[0], cur_state[1], 1]>=120:
        cv.putText(background, 'You Win!', org=(150, 220), color=(0, 0, 255), fontFace=fontFace, fontScale=3)
        cv.imshow("Window", background)
        cv.waitKey(0)
        break
        
    
    k = cv.waitKey(0)
    
    if k == 100: # 83:# right arrow D
        cur_state[1] += 10
    elif k == 97: # 81:# left arrow A
        cur_state[1] -= 10
    elif k == 119: # upper arrow
        cur_state[0] -= 10
    elif k == 115: # down arrow
        cur_state[0] +=10
    elif k == 113 or k == 27:  # q or esc
        break
    # print(f'k = {k}, org = {org}')
    if k == 100 or k == 97 or k ==119 or k ==115:
        # cv.putText(state, 'O', org=tuple(cur_state), color=(255, 0, 0), fontFace=fontFace, fontScale=0.5)
        
        print(f"color background: {background[cur_state[0], cur_state[1]]}")
        print(f"color state: {state[cur_state[0], cur_state[1]]}")
        print(cur_state)
        state[cur_state[0]:cur_state[0]+10, cur_state[1]:cur_state[1]+10] = [255, 0, 0]


cv.destroyWindow("Window")