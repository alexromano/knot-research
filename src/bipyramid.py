from math import sqrt
import numpy as np 
import transformations as tf 
from math import sqrt, pi, acos, degrees

class Geometry:

    origin, xaxis, yaxis, zaxis = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)

    def __init__(self):
        self.solid, self.plist = [], []

        # CHANGEABLE PARAMETERS
        self.scale = 2
        self.top_height = 1.75 * self.scale
        self.square_tip_out = 1.25 * self.scale
        self.square_tip_up = 1 * self.scale
        self.line_out = 1.5 * self.scale

        # cost function weights
        self.alpha, self.beta, self.gamma = 50, 50, 1.0/3

        # for gradient descent
        self.wiggle_size, self.step_size = 10e-5, 0.5
        self.prev_cost, self.cost_change = None, None

    def buildGeometry(self):
        self.redraw()
        self.solid = np.array(self.plist)

    def redraw(self):
        del self.plist[:]

        # top half top point
        self.plist.append([0, 0, self.top_height])

        # calculations for top and bottom halves
        x_dist = sqrt(3) * self.square_tip_out / 2.0
        y_dist = self.square_tip_out / 2.0

        # top half corner top points
        self.plist.append([0, self.square_tip_out, self.square_tip_up])
        self.plist.append([-x_dist, -y_dist, self.square_tip_up])
        self.plist.append([x_dist, -y_dist, self.square_tip_up])

        # bottom half bottom point
        self.plist.append([0, 0, -self.top_height])

        # bottom half corner bottom points
        self.plist.append([0, self.square_tip_out, -self.square_tip_up])
        self.plist.append([-x_dist, -y_dist, -self.square_tip_up])
        self.plist.append([x_dist, -y_dist, -self.square_tip_up])

        # calculations for connector line points
        x_offset = self.scale / 4.0
        y_offset = self.scale * sqrt(3) / 4.0
        x_coord = self.line_out * sqrt(3) / 2.0
        y_coord = self.line_out / 2.0

        # bottom bar connector line points
        self.plist.append([self.scale/2.0, -self.line_out, 0])
        self.plist.append([-self.scale/2.0, -self.line_out, 0])

        # wing connector line points
        self.plist.append([x_coord + x_offset, y_coord - y_offset, 0])
        self.plist.append([x_coord - x_offset, y_coord + y_offset, 0])
        self.plist.append([-x_coord - x_offset, y_coord - y_offset, 0])
        self.plist.append([-x_coord + x_offset, y_coord + y_offset, 0])

    def take_step(self):

        #handle first two calls to set up comparisons for future
        if self.prev_cost == None:
            self.prev_cost = self.cost()[3]
        elif self.cost_change == None:
            self.gradient_descent()
            cost = self.cost()[3]
            self.cost_change = (self.prev_cost - cost) / self.step_size
            self.prev_cost = cost

        # take most beneficial step
        else:
            values = (self.top_height, self.square_tip_out, self.square_tip_up, self.line_out)
            self.gradient_descent()
            cost = self.cost()[3]
            decrease = (self.prev_cost - cost) / self.step_size

            if abs(self.prev_cost - cost) < 0.5:
                print('Finished optimizing!')

            if decrease < 0:
                self.step_size /= 1.02

            # if step is better than last step
            elif decrease > self.cost_change:
                self.step_size *= 1
                # self.step_size *= 1.01

            # if step is not as good but still beneficial
            else:
                self.step_size /= 1.01
                self.wiggle_size /= 1.001

            self.cost_change, self.prev_cost = decrease, cost

    def gradient_descent(self):
        self.redraw()
        norm_cost = self.cost()[3]

        # figure out contribution to cost function by each parameter
        self.top_height += self.wiggle_size
        self.redraw()
        top_height_cost = self.cost()[3] - norm_cost
        top_height_step = top_height_cost * self.step_size * -1
        self.top_height -= self.wiggle_size

        self.square_tip_out += self.wiggle_size
        self.redraw()
        square_tip_out_cost = self.cost()[3] - norm_cost
        square_tip_out_step = square_tip_out_cost * self.step_size * -1
        self.square_tip_out -= self.wiggle_size

        self.square_tip_up += self.wiggle_size
        self.redraw()
        square_tip_up_cost = self.cost()[3] - norm_cost
        square_tip_up_step = square_tip_up_cost * self.step_size * -1
        self.square_tip_up -= self.wiggle_size

        self.line_out += self.wiggle_size
        self.redraw()
        line_out_cost = self.cost()[3] - norm_cost
        line_out_step = line_out_cost * self.step_size * -1
        self.line_out -= self.wiggle_size

        # take gradient descent step in direction of most decrease
        self.top_height += top_height_step
        self.square_tip_out += square_tip_out_step
        self.square_tip_up += square_tip_up_step
        self.line_out += line_out_step

        self.redraw()

    def cost(self):
        a, b, c = self.length_cost(), self.angle_cost(), self.planarity_cost()
        t = a + b + c
        return (a, b, c, t)

    def length_cost(self):

        def distance(point1, point2):
            diff = 0
            for i in range(len(point1)):
                diff += (point1[i] - point2[i]) ** 2
            return sqrt(diff)

        top_point_line = distance(self.plist[0], self.plist[1])
        diff_tops = abs(top_point_line - self.scale) * 6

        square_line = distance(self.plist[5], self.plist[13])
        diff_squares = abs(square_line - self.scale) * 12

        out_line = distance(self.plist[8], self.plist[9])
        diff_outs = abs(out_line - self.scale) * 4

        diff_total = diff_tops + diff_squares + diff_outs
        return diff_total * self.alpha

    def angle_cost(self):

        def angle(vec1, vec2):

            def magnitude(vec):
                sum = 0
                for i in range(len(vec)):
                    sum += vec[i] ** 2
                return sqrt(sum)

            numer = 0
            for i in range(len(vec1)):
                numer += vec1[i] * vec2[i]

            denom = magnitude(vec1) * magnitude(vec2)

            fraction = numer / denom

            return acos(fraction)

        def vectorize(point1, point2):
            vec = []
            for i in range(len(point1)):
                vec.append(point2[i] - point1[i])
            return vec

        sum_deviations = 0

        # for the pentagons
        s_pentagon = 108 * 2 * pi / 360

        top_edge_1 = vectorize(self.plist[0], self.plist[1])
        top_edge_2 = vectorize(self.plist[0], self.plist[2])
        top_angle = angle(top_edge_1, top_edge_2)

        top_edge = vectorize(self.plist[1], self.plist[0])
        side_edge = vectorize(self.plist[1], self.plist[13])
        side_angle = angle(top_edge, side_edge)

        side_edge_1 = vectorize(self.plist[13], self.plist[1])
        line_out_edge = vectorize(self.plist[13], self.plist[12])
        line_angle = angle(top_edge_1, line_out_edge)

        pentagon_devation = abs(top_angle - s_pentagon) + 2 * abs(side_angle - s_pentagon) \
                            + 2 * abs(line_angle - s_pentagon)
        sum_deviations += 6 * pentagon_devation

        # for the squares
        s_square = 90 * 2 * pi / 360

        left_edge = vectorize(self.plist[1], self.plist[11])
        right_edge = vectorize(self.plist[1], self.plist[13])
        top_angle = angle(left_edge, right_edge)

        top_edge = vectorize(self.plist[11], self.plist[1])
        bottom_edge = vectorize(self.plist[11], self.plist[5])
        edge_angle = angle(top_edge, bottom_edge)

        square_deviation = abs(top_angle - s_square) * 2 + abs(edge_angle - s_square) * 2
        sum_deviations += 3 * square_deviation

        return sum_deviations * self.beta

    def planarity_cost(self):

        def best_fit_plane(plist):
            a, b, c = 0, 0, 0
            p = (0, 0, 0)
            n = len(plist)

            for i in range(n):
                a += (plist[i][1] - plist[(i+1) % n][1]) * (plist[i][2] + plist[(i+1) % n][2])
                b += (plist[i][2] - plist[(i+1) % n][2]) * (plist[i][0] + plist[(i+1) % n][0])
                c += (plist[i][0] - plist[(i+1) % n][0]) * (plist[i][1] + plist[(i+1) % n][1])
                p = tuple(p[x] + plist[i][x] for x in range(len(p)))

            p = tuple(p[x] / n for x in range(len(p)))

            d = -a * p[0] - b * p[1] - c * p[2]

            return (a, b, c, d)

        def distance(point, plane):
            d = abs(plane[0]*point[0] + plane[1]*point[1] + plane[2]*point[2] + plane[3])
            d /= sqrt(plane[0]**2 + plane[1]**2 + plane[2]**2)
            return d

        def cost(plist):
            planarity = 0
            plane = best_fit_plane(plist)
            for point in self.plist:
                planarity += distance(point, plane)
            return planarity

        p_list = [self.plist[0], self.plist[1], self.plist[3], self.plist[11], self.plist[10]]
        pentagon = cost(p_list) * 6
        s_list = [self.plist[2], self.plist[6], self.plist[9], self.plist[12]]
        square = cost(s_list) * 4

        return (pentagon + square) * self.gamma






        






















