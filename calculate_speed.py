import glob
import os
import statistics
from math import sqrt, pow

import numpy as np
from scipy import stats
from sklearn.linear_model import RANSACRegressor

from ransac_3d_fit import Ransac3DFit


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
    if len(positions) <= 1:
        return None, None, None
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
    print(speeds)
    if len(speeds) > 0:
        return statistics.mean(speeds)
    return None;


def get_median_speed(timestamps, positions, min_dist=None, max_dist=None):
    speeds = get_speeds(timestamps, positions, min_dist, max_dist)
    if len(speeds) > 0:
        return statistics.median(speeds)
    return None

def get_ransac_speed_3d_fit(timestamps, positions, min_dist=None, max_dist=None, precision=2):
    speed, _ = get_ransac_speed_3d_complete(timestamps, positions, min_dist, max_dist, precision)
    return speed


def get_ransac_speed_3d_complete(timestamps, positions, min_dist=None, max_dist=None, precision=2):

    filtered_positions_mask = get_filtered_positions_mask(positions, min_dist, max_dist)
    timestamps = np.array(timestamps)[filtered_positions_mask]
    positions = np.array(positions)[filtered_positions_mask]
    if len(positions) <= 1:
        return None, None, None

    ransac = RANSACRegressor(base_estimator=Ransac3DFit(), min_samples=(0.75), max_trials=1000,  residual_threshold=1, stop_probability=.99)
    timestamps_f = []
    for timestamp in timestamps:
        timestamps_f.append([timestamp])
    ransac.fit(timestamps_f, positions)
    min_val = min(timestamps)
    max_val = max(timestamps)
    distance = calculate_distance(ransac.predict([[min_val]])[0], ransac.predict([[max_val]])[0])
    speed = round_number(calculate_speed(distance, max_val - min_val), precision)
    return speed, ransac

def get_first_last_speed(timestamps, positions, min_dist=None, max_dist=None):
    if len(timestamps) > 2:
        distance = calculate_distance(positions[0], positions[-1])
        elapsed_time = timestamps[-1] - timestamps[0]
        return calculate_speed(distance, elapsed_time)
    return None


def get_trim_mean_speed(timestamps, positions, min_dist=None, max_dist=None):
    proportion_to_cut = 0.10
    speeds = get_speeds(timestamps, positions, min_dist, max_dist)
    if len(speeds) > 0:
        return stats.trim_mean(speeds, proportion_to_cut)
    return None


def get_interpolated_average_speed(timestamps, positions, min_dist=None, max_dist=None):
    speeds = get_interpolated_speeds(timestamps, positions, None, min_dist, max_dist)
    print(speeds)
    if len(speeds) > 0:
        return statistics.mean(speeds)
    return None


def get_interpolated_median_speed(timestamps, positions, min_dist=None, max_dist=None):
    speeds = get_interpolated_speeds(timestamps, positions, None, min_dist, max_dist)
    if len(speeds) > 0:
        return statistics.median(speeds)
    return None


def get_interpolated_trim_mean_speed(timestamps, positions, min_dist=None, max_dist=None):
    proportion_to_cut = 0.1
    speeds = get_interpolated_speeds(timestamps, positions, None, min_dist, max_dist)
    if len(speeds) > 0:
        return stats.trim_mean(speeds, proportion_to_cut)
    return None


def print_speed(timestamps, positions, output_file):
    should_restrict_distance = False
    min_distance = 0
    max_distance = 25.0
    average_speed = get_average_speed(timestamps, positions)
    median_speed = get_median_speed(timestamps, positions)
    trim_mean_speed = get_trim_mean_speed(timestamps, positions)
    interpolated_average_speed = get_interpolated_average_speed(timestamps, positions)
    interpolated_median_speed = get_interpolated_median_speed(timestamps, positions)
    interpolated_trim_mean_speed = get_interpolated_trim_mean_speed(timestamps, positions)
    ransac_speed = get_ransac_speed(timestamps, positions)
    first_last_speed = get_first_last_speed(timestamps, positions)
    ransac_speed3d = get_ransac_speed_3d_fit(timestamps, positions)
    if should_restrict_distance:
        distance_interval_average_speed = get_average_speed(timestamps, positions, min_distance, max_distance)
        distance_interval_median_speed = get_median_speed(timestamps, positions, min_distance, max_distance)
        distance_interval_trim_mean_speed = get_trim_mean_speed(timestamps, positions, min_distance, max_distance)
        distance_interval_interpolated_average_speed = get_interpolated_average_speed(timestamps, positions, min_distance, max_distance)
        distance_interval_interpolated_median_speed = get_interpolated_median_speed(timestamps, positions, min_distance, max_distance)
        distance_interval_interpolated_trim_mean_speed = get_interpolated_trim_mean_speed(timestamps, positions, min_distance, max_distance)
        distance_interval_ransac_speed = get_ransac_speed(timestamps, positions, min_distance, max_distance)

    print('average                                                                                      ' + str(average_speed))
    print('median                                                                                       ' + str(median_speed))
    print('trim_mean                                                                                    ' + str(trim_mean_speed))
    print('interpolated average                                                                         ' + str(interpolated_average_speed))
    print('interpolated median                                                                          ' + str(interpolated_median_speed))
    print('interpolated trim_mean                                                                       ' + str(interpolated_trim_mean_speed))
    print('ransac ' + str(ransac_speed))
    print('first_last_speed ' + str(first_last_speed))
    print('ransac_speed3d ' + str(ransac_speed3d))
    if should_restrict_distance:
        print('average                  min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(distance_interval_average_speed))
        print('median                   min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(distance_interval_median_speed))
        print('trim_mean                min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(distance_interval_trim_mean_speed))
        print('interpolated average     min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(distance_interval_interpolated_average_speed))
        print('interpolated median      min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(distance_interval_interpolated_median_speed))
        print('interpolated trim_mean   min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(distance_interval_interpolated_trim_mean_speed))

        print('ransac min_dis ' + str(min_distance) + ' max dist ' + str(max_distance) + ' ' + str(distance_interval_ransac_speed))
    output_file.write(
        ';' + str(average_speed) + ';' + str(median_speed) + ';' + str(trim_mean_speed) + ';' + str(interpolated_average_speed) + ';' + str(interpolated_median_speed) + ';' + str(interpolated_trim_mean_speed) + ';' + str(ransac_speed) + ';' + str(
            first_last_speed) + ';' + str(ransac_speed3d))
    if should_restrict_distance:
        output_file.write(str(distance_interval_average_speed) + ';' + str(distance_interval_median_speed) + ';' + str(distance_interval_trim_mean_speed) + ';' + str(distance_interval_interpolated_average_speed) + ';' + str(
            distance_interval_interpolated_median_speed) + ';' + str(distance_interval_interpolated_trim_mean_speed) + ';' + str(distance_interval_ransac_speed) + ';' + str(ransac_speed3d))
    output_file.write('\n')
    print('')


def get_speed_from_content(file_content, output_file):
    positions = []
    timestamps = []
    lines = []
    for line in file_content.split('\n'):
        line = line.strip()
        if len(line) > 0 and not line == 'begin - attempt:' and not line == 'end - attempt:':
            values = line.split(',')
            if len(values) != 4:
                break
            lines.append(line)
    lines = sorted(lines, key=lambda x: float(x.split(',')[0]))
    for line in lines:
        if len(line) > 0 and not line == 'begin - attempt:' and not line == 'end - attempt:':
            values = line.split(',')
            if len(values) != 4:
                break
            values = list(map(lambda x: float(x), values))
            timestamp = values[0]
            position = tuple(values[1::])
            positions.append(position)
            timestamps.append(timestamp)
    if len(positions) == 0:
        output_file.write('\n')
        return None
    return print_speed(np.array(timestamps), np.array(positions), output_file)  # else:  #     return get_speed(timestamps, positions)


if __name__ == '__main__':
    i = 1
    csv_filename = "csv/fileName"
    while os.path.exists(csv_filename + '.csv'):
        csv_filename = "csv/fileName" + str(i)
        i += 1
    csv = open(csv_filename + '.csv', 'w')

    # for filepath in glob.glob('points/29_08/*[!_manual].csv'):
    for filepath in glob.glob('points/points/*.csv'):
        file = open(filepath)
        expected_speed = filepath.split('/')[-1].split('_')[-1].split('.')[0]
        csv.write(filepath + ';' + expected_speed)
        print('reading for file ' + filepath + '\nexpected speed: ' + expected_speed)
        get_speed_from_content(file.read(), csv)
