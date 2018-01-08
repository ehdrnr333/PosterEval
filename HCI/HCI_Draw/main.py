import cv2
import numpy as np
import copy

list = ['beer-0','beer-1','beer-2','beer-3','beer-4','beer-5',  'soju-0', 'soju-1', 'soju-2', 'soju-3', 'soju-4', 'soju-5','soju-6','soju-7']

x_val = 500
y_val = 100

def draw_track(f_str, img):
    f = open(f_str, 'r')
    v_str = "EYE PATH"
    cv2.putText(img, v_str, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 4)

    lines = f.readlines()
    interval = 255/len(lines)
    step = 0


    for line in lines:
        step = step+interval
        data = line.split()
        cur_x = int(data[1])
        cur_y = int(data[2])

        cv2.circle(img, (cur_x - x_val, cur_y - y_val), 30, (int(step) + 190, 225, int(255 - step) + 190), -1)
    f.close()

    step = 0
    count = 0

    x = 1
    y = 1
    for line in lines:
        count = count +1
        step = step+interval
        data = line.split()

        if count%30 ==1:
            cv2.putText(img, str(int(count/30)), (int(data[1]) - x_val, int(data[2]) - y_val), cv2.FONT_HERSHEY_SIMPLEX, 1,(int(step) + 90, 120, int(255 - step) + 90), 4)
            cv2.line(img, (x,y), (int(data[1]) - x_val, int(data[2]) - y_val),(int(step) + 90, 120, int(255 - step) + 90), 2)

            x = int(data[1]) - x_val
            y = int(data[2]) - y_val

        cv2.circle(img, (int(step), 160), 40, (int(step) + 90, 120, int(255 - step) + 90), -1)
    f.close()
    return img

def draw_axis(f_str, img, mind, att_med):
    f = open(f_str, 'r')
    board = np.zeros((img.shape[:2][0], img.shape[:2][1], 1), np.uint8)
    board = cv2.addWeighted(board, 1, board, 1, 0.0)
    str = ""
    if mind == 0:
        str = "Eye Track"
    elif att_med == 0:
        str = "Attention"
    else:
        str = "Medtation"

    cv2.putText(board, str, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 4)

    if mind == 0:
        for i in range(0, 255):
            cv2.circle(board, (i, 160), 40, i, -1)

    while True:
        line = f.readline()
        data = line.split()
        if not line: break

        w = 40-mind*(40-int(data[3+att_med]))

        obj = np.zeros((board.shape[:2][0], board.shape[:2][1], 1), np.uint8)

        if mind==0:
            cv2.circle(obj, (int(data[1])-x_val, int(data[2])-y_val), int(w*3/4), 40, -1)
            board = cv2.addWeighted(board, 1, obj, 1, 0.0)
        else:
            if att_med ==0:
                cv2.circle(board, (int(data[1]) - x_val, int(data[2]) - y_val), int(w * 3 / 4),int(w*1.3), -1)
            else:
                cv2.circle(board, (int(data[1]) - x_val, int(data[2]) - y_val), int(w * 3 / 4), 130+int(w * 1.3), -1)


    f.close()

    hsv = np.ones((img.shape[:2][0], img.shape[:2][1], 3), np.uint8)*255
    hsv[:,:,0] = board
    hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    hsv = cv2.blur(hsv, (7,7))

    board = cv2.cvtColor(board, cv2.COLOR_GRAY2BGR)
    mode = cv2.bitwise_and(board, hsv)

    filt = cv2.bitwise_not(mode)
    gray = cv2.cvtColor(filt, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    filt = cv2.bitwise_and(filt, gray)
    filt2 = cv2.bitwise_not(gray)
    return filt, filt2

def draw_mind(f_str, img, flag):
    f = open(f_str, 'r')
    att = 0
    med = 0
    x = 0
    y = 0

    if flag == 0:
        for i in range(100):
            cv2.circle(img, (i, 160), 30, (i*2,255-i*2, 155+i), -1)
        while True:
            line = f.readline()
            data = line.split()
            if not line: break

            i = int(data[3])
            dif = abs(x - int(data[1])) + abs(y - int(data[2]))
            if (att != int(data[3]) or dif > 100) and flag == 0:
                cv2.circle(img, (int(data[1]) - x_val, int(data[2]) - y_val), int(i / 2), (i * 2, 255 - i * 2, 155 + i), -1)
            elif (med != int(data[4]) or dif > 100) and flag == 1:
                cv2.circle(img, (int(data[1]) - x_val, int(data[2]) - y_val), int(i / 2), (i * 2, 255 - i * 2, 155 + i),-1)
            x = int(data[1])
            y = int(data[2])
            att = int(data[3])
            med = int(data[4])

    else:
        for i in range(100):
            cv2.circle(img, (i, 160), 30, (155+i,255-i*2,i*2),  -1)
        while True:
            line = f.readline()
            data = line.split()
            if not line: break

            i = int(data[4])
            dif = abs(x - int(data[1])) + abs(y - int(data[2]))
            if (att != int(data[3]) or dif > 100) and flag == 0:
                cv2.circle(img, (int(data[1]) - x_val, int(data[2]) - y_val), int(i / 2), (155 + i, 255 - i * 2, i * 2), -1)
            elif (med != int(data[4]) or dif > 100) and flag == 1:
                cv2.circle(img, (int(data[1]) - x_val, int(data[2]) - y_val), int(i / 2), (155 + i, 255 - i * 2, i * 2),-1)
            x = int(data[1])
            y = int(data[2])
            att = int(data[3])
            med = int(data[4])

    f.close()

    f = open(f_str, 'r')
    while True:
        line = f.readline()
        data = line.split()
        if not line: break

        dif = abs(x-int(data[1]))+ abs(y-int(data[2]))
        if (att!=int(data[3])or dif >100) and flag==0:
            cv2.putText(img, str(data[3]), (int(data[1])-20-x_val, int(data[2])-y_val), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,105,255),4)
        elif (med !=int(data[4])or dif>100) and flag==1:
            cv2.putText(img, str(data[4]), (int(data[1])+20-x_val, int(data[2])-y_val), cv2.FONT_HERSHEY_SIMPLEX, 1, (105,0,255), 4)
        x = int(data[1])
        y = int(data[2])
        att = int(data[3])
        med = int(data[4])
    f.close()
    return img

def main():

    for i in range(1, 8):
        log_num = '0'+str(i)
        for i in range(len(list)):
            img = cv2.imread(list[i]+'.png')
            filt, filt2 = draw_axis(log_num+"-"+list[i]+".txt",img, 0, 0)
            result = cv2.bitwise_and(img, filt2)
            result = cv2.bitwise_or(result, filt)
            cv2.imwrite('result-'+log_num+'/'+list[i]+'-ax.jpg', result)

            result = copy.copy(img)
            result = draw_mind(log_num+"-" + list[i] + ".txt", result, 0)
            cv2.imwrite('result-'+log_num+'/'+list[i]+'-ma.jpg', result)

            result = copy.copy(img)
            result = draw_mind(log_num+"-" + list[i] + ".txt", result, 1)
            cv2.imwrite('result-'+log_num+'/'+list[i]+'-md.jpg', result)

            result = draw_track(log_num+"-"+list[i]+".txt",img)
            cv2.imwrite('result-'+log_num+'/'+list[i]+'-bt.jpg', result)


if __name__ == '__main__':
    main()