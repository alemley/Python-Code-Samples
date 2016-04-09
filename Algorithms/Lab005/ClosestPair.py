from random import randint
import math
import timeit


class Points(object):
    def __init__(self, _x=None, _y=None):
        self.x = _x
        self.y = _y


def closest_pair(_points, _num_points):
    points = _points
    number_of_points = _num_points
    dist = math.inf
    tuple1 = ()
    tuple2 = ()
    basic_operation_count = 0
    start = timeit.default_timer()
    for i in range(1, number_of_points - 1):
        basic_operation_count += 1
        for j in range(i + 1, number_of_points):
            basic_operation_count += 1
            current_dist = ((points[i].x - points[j].x) ** 2) + ((points[i].y - points[j].y) ** 2)
            if dist > current_dist:
                basic_operation_count += 1
                dist = current_dist
                tuple1 = points[i]
                tuple2 = points[j]
    stop = timeit.default_timer()
    print("Closest pair identified.")
    print("Point 1: ", tuple1.x, ',', tuple1.y)
    print("Point 2: ", tuple2.x, ',', tuple2.y)
    print("Distance between points: ", math.sqrt(dist))
    print("Search runtime: ", (stop - start))
    print("Total number of comparisons: ", basic_operation_count)


def main():
    points = []
    print("Enter total number of points to generate:")
    num_points = int(input())
    print("Number of points: ", num_points)
    for i in range(0, num_points):
        x = randint(-500, 500)
        y = randint(-500, 500)
        points.append(Points(x, y))
    closest_pair(points, num_points)

if __name__ == "__main__":
    main()

#  6) I don't quite recall the projected formula from class, but I do
#  recall that the brute force algorithm is in big theta of (n^3), which could count as a projected worst - case.
#  If this is the case, then the algorithm did much better than expected and operated closer to ((n^2)/2) comparisons