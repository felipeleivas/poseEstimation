from operator import itemgetter

def get_pixels_right_order(pixels):
    sorted_pixels =  sorted(pixels, key=itemgetter(0))
    left_points = sorted_pixels[0:2]
    right_points = sorted_pixels[2:4]
    p1,p4 = sorted(left_points, key=itemgetter(1))
    p2,p3 = sorted(right_points, key=itemgetter(1))
    return [p1,p2,p3,p4]
