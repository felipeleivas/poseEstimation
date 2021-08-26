import glob
import os
import statistics
from math import sqrt, pow

import numpy as np
from scipy import stats
from sklearn.linear_model import RANSACRegressor


def round_number(number, decimal):
    decimal_value = pow(10, decimal)
    number = number * decimal_value
    number = int(number) / decimal_value
    return number


def calculate_distance(point1, point2):
    sum = 0
    for index in range(0, len(point1)):
        sqr = pow(point1[index] - point2[index], 2)
        sum = sum + sqr
    return sqrt(sum)


def calculate_speed(distance, time_elapsed):
    return distance * (3600 / time_elapsed)


## RANSAC
def getRansacAxis(x_axis, y_axis):
    ransac = RANSACRegressor()
    ransac.fit(x_axis, y_axis)
    min = x_axis.min()
    max = x_axis.max()
    line_x = [[min], [max]]
    line_y_ransac = ransac.predict(line_x)
    return line_x, line_y_ransac, ransac


def get_ransac_speed(timestamps, positions, min_dist=None, max_dist=None, precision=2):
    speed, _, _ = get_ransac_speed_complete(timestamps, positions, min_dist, max_dist, precision)
    return speed


def get_ransac_speed_complete(timestamps, positions, min_dist=None, max_dist=None, precision=2):
    p1 = []
    p2 = []
    x_line_ransac = []
    y_line_ransac = []
    filtered_positions_mask = get_filtered_positions_mask(positions, min_dist, max_dist)
    timestamps = np.array(timestamps)[filtered_positions_mask]
    positions = np.array(positions)[filtered_positions_mask]
    positions_per_axis = []
    for position in positions:
        for index in range(0, len(position)):
            if len(positions_per_axis) <= index:
                positions_per_axis.append([])
            positions_per_axis[index].append(position[index])
    min_timestamp, max_timestamp = min(timestamps), max(timestamps)
    for axis_position in positions_per_axis:
        x_line, y_line, axis_ransac = getRansacAxis(np.array(timestamps)[:, None], np.array(axis_position)[:, None])
        p1.append(axis_ransac.predict([[min_timestamp]]))
        p2.append(axis_ransac.predict([[max_timestamp]]))
        x_line_ransac.append(x_line)
        y_line_ransac.append(y_line)
    distance = calculate_distance(p1, p2)
    speed = round_number(calculate_speed(distance, max_timestamp - min_timestamp), precision)
    return speed, x_line_ransac, y_line_ransac


####################
def get_filtered_positions_mask(positions, min_dist=None, max_dist=None):
    included = []
    for position in positions:
        position_distance = calculate_distance(position, [0, 0, 0])
        if min_dist is not None:
            if min_dist < position_distance:
                if max_dist is not None:
                    included.append(max_dist > position_distance)
                else:
                    included.append(True)
            else:
                included.append(False)
        elif max_dist is not None:
            included.append(max_dist > position_distance)

        else:
            included.append(True)
    return included


def get_speeds(timestamps, positions, min_dist=None, max_dist=None):
    speeds = []
    filtered_positions_mask = get_filtered_positions_mask(positions, min_dist, max_dist)
    timestamps = np.array(timestamps)[filtered_positions_mask]
    positions = np.array(positions)[filtered_positions_mask]

    for i in range(0, len(timestamps) - 1):
        distance = calculate_distance(positions[i], positions[i + 1])
        elapsed_time = timestamps[i + 1] - timestamps[i]
        speeds.append(calculate_speed(distance, elapsed_time))

    return speeds


def get_interpolated_speeds(timestamps, positions, interpolation_interval=None, min_dist=None, max_dist=None):
    speeds = []
    filtered_positions_mask = get_filtered_positions_mask(positions, min_dist, max_dist)
    timestamps = np.array(timestamps)[filtered_positions_mask]
    positions = np.array(positions)[filtered_positions_mask]

    for i in range(0, len(timestamps) - 1):
        max_interpolated_element_index = len(timestamps) - 1
        if interpolation_interval is not None:
            max_interpolated_element_index = min(max_interpolated_element_index, i + interpolation_interval)
        for j in range(i + 1, max_interpolated_element_index):
            distance = calculate_distance(positions[i], positions[j])
            elapsed_time = timestamps[j] - timestamps[i]
            speeds.append(calculate_speed(distance, elapsed_time))

    return speeds


#################
def get_average_speed(timestamps, positions, min_dist=None, max_dist=None):
    speeds = get_speeds(timestamps, positions, min_dist, max_dist)
    return statistics.mean(speeds)


def get_median_speed(timestamps, positions, min_dist=None, max_dist=None):
    speeds = get_speeds(timestamps, positions, min_dist, max_dist)
    return statistics.median(speeds)


def get_trim_mean_speed(timestamps, positions, proportion_to_cut=0.1, min_dist=None, max_dist=None):
    speeds = get_speeds(timestamps, positions, min_dist, max_dist)
    return stats.trim_mean(speeds, proportion_to_cut)


def get_interpolated_average_speed(timestamps, positions, min_dist=None, max_dist=None):
    speeds = get_interpolated_speeds(timestamps, positions, None, min_dist, max_dist)
    return statistics.mean(speeds)


def get_interpolated_median_speed(timestamps, positions, min_dist=None, max_dist=None):
    speeds = get_interpolated_speeds(timestamps, positions, None, min_dist, max_dist)
    return statistics.median(speeds)


def get_interpolated_trim_mean_speed(timestamps, positions, proportion_to_cut=0.1, min_dist=None, max_dist=None):
    speeds = get_interpolated_speeds(timestamps, positions, None, min_dist, max_dist)
    return stats.trim_mean(speeds, proportion_to_cut)


def print_speed(timestamps, positions, output_file):
    min_distance = 0
    max_distance = 25.0
    average_speed = get_average_speed(timestamps, positions)
    median_speed = get_median_speed(timestamps, positions)
    trim_mean_speed = get_trim_mean_speed(timestamps, positions)
    interpolated_average_speed = get_interpolated_average_speed(timestamps, positions)
    interpolated_median_speed = get_interpolated_median_speed(timestamps, positions)
    interpolated_trim_mean_speed = get_interpolated_trim_mean_speed(timestamps, positions)
    ransac_speed = get_ransac_speed(timestamps, positions)
    distance_interval_average_speed = get_average_speed(timestamps, positions, min_distance, max_distance)
    distance_interval_median_speed = get_median_speed(timestamps, positions, min_distance, max_distance)
    distance_interval_trim_mean_speed = get_trim_mean_speed(timestamps, positions, min_distance, max_distance)
    distance_interval_interpolated_average_speed = get_interpolated_average_speed(timestamps, positions, min_distance,
                                                                                  max_distance)
    distance_interval_interpolated_median_speed = get_interpolated_median_speed(timestamps, positions, min_distance,
                                                                                max_distance)
    distance_interval_interpolated_trim_mean_speed = get_interpolated_trim_mean_speed(timestamps, positions,
                                                                                      min_distance, max_distance)
    distance_interval_ransac_speed = get_ransac_speed(timestamps, positions, min_distance, max_distance)

    # print('average                                                                                      ' + str(
    #     average_speed))
    # print('median                                                                                       ' + str(
    #     median_speed))
    # print('trim_mean                                                                                    ' + str(
    #     trim_mean_speed))
    # print('interpolated average                                                                         ' + str(
    #     interpolated_average_speed))
    # print('interpolated median                                                                          ' + str(
    #     interpolated_median_speed))
    # print('interpolated trim_mean                                                                       ' + str(
    #     interpolated_trim_mean_speed))
    print('ransac ' + str(ransac_speed))
    # print('average                  min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(
    #     distance_interval_average_speed))
    # print('median                   min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(
    #     distance_interval_median_speed))
    # print('trim_mean                min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(
    #     distance_interval_trim_mean_speed))
    # print('interpolated average     min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(
    #     distance_interval_interpolated_average_speed))
    # print('interpolated median      min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(
    #     distance_interval_interpolated_median_speed))
    # print('interpolated trim_mean   min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(
    #     distance_interval_interpolated_trim_mean_speed))

    print(
        'ransac min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(
            distance_interval_ransac_speed))
    output_file.write(';' + str(average_speed) + ';' + str(median_speed) + ';' + str(trim_mean_speed) + ';' + str(
        interpolated_average_speed) + ';' + str(interpolated_median_speed) + ';' + str(
        interpolated_trim_mean_speed) + ';' + str(ransac_speed) + ';' + str(
        distance_interval_average_speed) + ';' + str(distance_interval_median_speed) + ';' + str(
        distance_interval_trim_mean_speed) + ';' + str(distance_interval_interpolated_average_speed) + ';' + str(
        distance_interval_interpolated_median_speed) + ';' + str(
        distance_interval_interpolated_trim_mean_speed) + ';' + str(distance_interval_ransac_speed) + '\n')
    print('')


def get_speed_from_content(file_content, output_file):
    positions = []
    timestamps = []
    for line in file_content.split('\n'):
        line = line.strip()
        if len(line) > 0 and not line == 'begin - attempt:' and not line == 'end - attempt:':
            values = line.split(',')
            if len(values) != 4:
                break
            values = list(map(lambda x: float(x), values))
            timestamp = values[0]
            position = tuple(values[1::])
            positions.append(position)
            timestamps.append(timestamp)
    # if print:
    return print_speed(np.array(timestamps), np.array(positions), output_file)
    # else:
    #     return get_speed(timestamps, positions)


if __name__ == '__main__':
    i = 1
    csv_filename = "csv/fileName"
    while os.path.exists(csv_filename + '.csv'):
        csv_filename = "csv/fileName" + str(i)
        i += 1
    csv = open(csv_filename + '.csv', 'w')

    for filepath in glob.glob('points/01_08/*[!manual].csv'):
        file = open(filepath)
        expected_speed = filepath.split('/')[-1].split('_')[1].split('.')[0]
        csv.write(filepath + ';' + expected_speed)
        print('reading for file ' + filepath + '\nexpected speed: ' + expected_speed)
        get_speed_from_content(file.read(), csv)
        # average, median, fmean, trim_mean, _ = get_speed_from_content(file.read(), False)
        # csv.write(filepath + "," + str(average) + "," + str(median) + "," + str(trim_mean) + ",\n")
