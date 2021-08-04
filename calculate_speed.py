import glob

from math import sqrt, pow
import statistics


def calculate_distance(point1, point2):
    sum = 0
    for index in range(0, len(point1)):
        if index != 1:
            sqr = pow(point1[index] - point2[index], 2)
            sum = sum + sqr
    return sqrt(sum)



def calculate_speed(distance, time_elapsed):
    return distance * (3600 / time_elapsed)


if __name__ == '__main__':
    for filepath in glob.glob('points/01_08/*'):
        file = open(filepath)
        index = 1
        for line in file:
            if line.strip() == 'begin - attempt:':
                positions = []
                timestamps = []
                speeds = []
            elif line.strip() == 'end - attempt:':
                for i in range(0, len(timestamps) - 1):
                    distance = calculate_distance(positions[i], positions[i + 1])
                    time_elapsed = timestamps[i + 1] - timestamps[i]
                    speeds.append(calculate_speed(distance, time_elapsed))
                if len(speeds) > 0:
                    print('print attemp number ' + str(index) + ' for file: ' + filepath)
                    print('distance = ' + str(distance))
                    print('time_elapsed = ' + str(time_elapsed))
                    print('average ' + str(statistics.mean(speeds)))
                    print('median ' + str(statistics.median(speeds)))
                    print('fmean ' + str(statistics.fmean(speeds)))
                    print('size ' + str(len(timestamps)))
                    print('\n\n')
                    index += 1
            else:
                values = line.split(',')
                if len(values) != 4:
                    break
                values = list(map(lambda x: float(x), values))
                timestamp = values[0]
                position = tuple(values[1::])
                positions.append(position)
                timestamps.append(timestamp)
