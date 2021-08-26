import glob

import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import RANSACRegressor

from calculate_speed import calculate_distance, calculate_speed, get_ransac_speed, getRansacAxis, \
    get_ransac_speed_complete

plt.style.use('seaborn-whitegrid')

if __name__ == '__main__':

    # for filepath in glob.glob('points/01_08/hb20_28_2.csv'):
    for filepath in glob.glob('points/01_08/*[!manual].csv'):
        file = open(filepath)
        expected_speed = filepath.split('/')[-1].split('_')[1].split('.')[0]
        print('reading for file ' + filepath)
        content = file.read()
        i = 0
        x_data = []
        y_data = []
        z_data = []
        timestamp_data = []
        timestamp = []
        positions = []
        xRot = 0
        yRot = 0
        for line in content.split('\n'):
            tokens = line.split(',')
            if len(tokens) >= 4:
                timestamp_data.append([float(tokens[0])])
                timestamp.append(float(tokens[0]))
                x_data.append([float(tokens[1])])
                y_data.append([float(tokens[2])])
                z_data.append([float(tokens[3])])
                positions.append(tuple([float(tokens[1]), float(tokens[2]), float(tokens[3])]))
                i += 1
        timestamp_data = np.array(timestamp_data)
        x_data = np.array(x_data)
        y_data = np.array(y_data)
        z_data = np.array(z_data)
        fig = plt.figure()

        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(223)

        ax1.plot(timestamp_data, x_data, 'o', color='green', markersize=1)
        ax1.set_xlabel('Timestamp')
        ax1.set_ylabel('X Position')
        # line_x, line_y_ransac, x_ransac = getRansacAxis(timestamp_data, x_data)
        # ax1.plot(line_x, line_y_ransac, color='black', lw=1)

        ax2.plot(timestamp_data, y_data, 'o', color='red', markersize=1)
        ax2.set_xlabel('Timestamp')
        ax2.set_ylabel('Y Position')
        # line_x, line_y_ransac, y_ransac = getRansacAxis(timestamp_data, y_data)
        # ax2.plot(line_x, line_y_ransac, color='black', lw=1)

        ax3.plot(timestamp_data, z_data, 'o', color='pink', markersize=1)
        ax3.set_xlabel('Timestamp')
        ax3.set_ylabel('Z Position')


        speed, lines_x, lines_y = get_ransac_speed_complete(timestamp, positions, 3, 22)
        printed_string = 'speed: ' + str(speed) + '\nexpected speed: ' + expected_speed
        line_x, line_y_ransac = lines_x[0], lines_y[0]
        ax1.plot(line_x, line_y_ransac, color='black', lw=1)

        line_x, line_y_ransac = lines_x[1], lines_y[1]
        ax2.plot(line_x, line_y_ransac, color='black', lw=1)

        line_x, line_y_ransac = lines_x[2], lines_y[2]
        ax3.plot(line_x, line_y_ransac, color='black', lw=1)

        print('speed: ' + str(speed) )
        # place a text box in upper left in axes coords
        fig.text(0.6, 0.25, printed_string, fontsize=14,
                verticalalignment='center')
        # timestamp_data
        # ransac.predict(line_X
        plt.show()
        cv2.waitKey(0)
