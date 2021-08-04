from numpy import reshape
configuration = {}


def init():
    configuration_file = open('configuration/configuration.properties','r')

    for line in configuration_file:
        key, value = line.split('=')
        configuration[key] = value


def get_property(key):
    if len(configuration) == 0:
        init()
    return configuration[key]

def get_matrix(key, shape, function, splitter=','):
    return reshape(list(map(function, get_property(key).split(','))), shape)
