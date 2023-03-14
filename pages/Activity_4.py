import math

import streamlit as st
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d import Axes3D

tf.compat.v1.disable_eager_execution()


def rotateOnX(theta, pos):
    return np.array([pos['x'],
                    pos['y'] * math.cos(theta) - pos['z'] * math.sin(theta),
                    pos['y'] * math.sin(theta) + pos['z'] * math.cos(theta)])


def rotateOnY(theta, pos):
    return np.array([pos['z'] * math.sin(theta) + pos['x'] * math.cos(theta),
                     pos['y'],
                     pos['z'] * math.cos(theta) - pos['x'] * math.sin(theta)])


def rotateOnZ(theta, pos):
    return np.array([pos['x'] * math.cos(theta) - pos['y'] * math.sin(theta),
                    pos['x'] * math.sin(theta) + pos['y'] * math.cos(theta),
                    pos['z']])


def shearOnX(shY, shZ, pos):
    return np.array([pos['x'],
                     pos['y'] + pos['x'] * shY,
                     pos['z'] + pos['x'] * shZ])


def shearOnY(shX, shZ, pos):
    return np.array([pos['x'] + pos['y'] * shX,
                     pos['y'],
                     pos['z'] + pos['y'] * shZ])


def shearOnZ(shX, shY, pos):
    return np.array([pos['x'] + pos['z'] * shX,
                     pos['y'] + pos['z'] * shY,
                     pos['z']])


def getShearAm(ax):
    shear_am = st.number_input(
        'Multiplier to ' + ax + ' for shearing?')
    return shear_am


def runSession(points):
    with tf.compat.v1.Session() as session:
        return session.run(points)


class Transform():

    def __init__(self):
        self.points = []
        self.pos = {'x': 0, 'y': 0, 'z': 0}
        self.size = 0

    def translate(self):
        cols = st.columns(3)
        x = cols[0].number_input("Inches to translate X?")
        y = cols[1].number_input("Inches to translate Y?")
        z = cols[2].number_input("Inches to translate Z?")

        trans_am = tf.constant([x, y, z], dtype=tf.float64)  # to move object
        trans_obj = tf.add(self.points, trans_am)
        self.points = runSession(trans_obj)

    def rotate(self):
        rot_ax = st.selectbox("Rotate object in which axis?", [
                              "X-Axis", "Y-Axis", "Z-Axis"])[0].lower()

        theta = math.radians(st.number_input("Angle to rotate object?"))

        for i in range(len(self.points)):
            pos = {'x': self.points[i][0],
                   'y': self.points[i][1],
                   'z': self.points[i][2]}
            if (rot_ax == 'x'):
                self.points[i] = rotateOnX(theta, pos)
            elif (rot_ax == 'y'):
                self.points[i] = rotateOnY(theta, pos)
            elif (rot_ax == 'z'):
                self.points[i] = rotateOnZ(theta, pos)
            else:
                exit()

        rotate_obj = tf.constant(self.points, dtype=tf.float64)
        self.points = runSession(rotate_obj)

    def scale(self):

        cols = st.columns(3)
        x = cols[0].number_input("Multiplier to scale X?")
        y = cols[1].number_input("Multiplier to scale Y?")
        z = cols[2].number_input("Multiplier to scale Z?")

        if x and y and z:
            scale_am = tf.constant([x, y, z], dtype=tf.float64)
            scale_obj = tf.multiply(self.points, scale_am)
            self.points = runSession(scale_obj)

    def shear(self):
        rot_ax = st.selectbox("Shear object in which axis?", [
            "X-Axis", "Y-Axis", "Z-Axis"])[0].lower()

        shr_am_one = 0
        shr_am_two = 0

        if (rot_ax == 'x'):
            shr_am_one = getShearAm('Y')
            shr_am_two = getShearAm('Z')
        elif (rot_ax == 'y'):
            shr_am_one = getShearAm('X')
            shr_am_two = getShearAm('Z')
        elif (rot_ax == 'z'):
            shr_am_one = getShearAm('X')
            shr_am_two = getShearAm('Y')
        else:
            exit()

        for i in range(len(self.points)):
            pos = {'x': self.points[i][0],
                   'y': self.points[i][1],
                   'z': self.points[i][2]}
            if (rot_ax == 'x'):
                self.points[i] = shearOnX(shr_am_one, shr_am_two, pos)
            elif (rot_ax == 'y'):
                self.points[i] = shearOnY(shr_am_one, shr_am_two, pos)
            elif (rot_ax == 'z'):
                self.points[i] = shearOnZ(shr_am_one, shr_am_two, pos)
            else:
                exit()

        shear_obj = tf.constant(self.points, dtype=tf.float64)
        self.points = runSession(shear_obj)

    def getPos(self, points):
        self.pos['x'] = points[:, 0][0]
        self.pos['y'] = points[:, 1][0]
        self.pos['z'] = points[:, 2][0]

    def plot(self):
        self.getPos(self.points)
        tri = Delaunay(self.points).convex_hull

        fig = plt.figure(figsize=(7, 7))  # adjusts window
        ax = fig.add_subplot(111, projection='3d')

        S = ax.plot_trisurf(self.points[:, 0], self.points[:, 1],
                            self.points[:, 2], triangles=tri, shade=True, cmap='Blues', lw=0.5)

        for i in range(len(self.points)):
            pos = {'x': self.points[i][0],
                   'y': self.points[i][1],
                   'z': self.points[i][2]}

            # ax.text(pos['x'], pos['y'], pos['z'], '%s' % (str(i)), size=20, zorder=999,
            # color='k')

        ax.set_xlabel('X [inches]')
        ax.set_ylabel('Y [inches]')
        ax.set_zlabel('Z [inches]')

        # axis of plane for placement of object
        ax.set_xlim3d(-self.size * 2, self.size * 2)
        ax.set_ylim3d(-self.size * 2, self.size * 2)
        ax.set_zlim3d(-self.size * 2, self.size * 2)

        return fig


class Cube(Transform):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        pre_val = 1.00
        if pre_val:
            side_len = st.number_input(
                "Area of cube in inches?", value=pre_val)
            self.size = side_len
            bottom_lower = np.array((0, 0, 0))
            points = np.vstack([
                bottom_lower,  # 0 || 8
                bottom_lower + [0, side_len, 0],  # 1
                bottom_lower + [side_len, side_len, 0],  # 2
                bottom_lower + [side_len, 0, 0],  # 3
                bottom_lower + [0, 0, side_len],  # 4
                bottom_lower + [0, side_len, side_len],  # 5
                bottom_lower + [side_len, side_len, side_len],  # 6
                bottom_lower + [side_len, 0, side_len],  # 7
                bottom_lower  # 8 || 0
            ])
            self.points = points


class Cuboid(Transform):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        pre_val = 1.00
        if pre_val:
            side_len = st.number_input(
                "Area of cuboid in inches?", value=pre_val)
            self.size = side_len
            bottom_lower = np.array((0, 0, 0))
            points = np.vstack([
                bottom_lower,  # No
                bottom_lower + [0, side_len * 2.0, 0],  # Yes
                bottom_lower + [side_len, side_len * 2.0, 0],  # Yes
                bottom_lower + [side_len, 0, 0],  # No
                bottom_lower + [0, 0, side_len],  # No
                bottom_lower + [0, side_len * 2.0, side_len],  # Yes
                bottom_lower + [side_len, side_len * 2.0, side_len],  # Yes
                bottom_lower + [side_len, 0, side_len],  # No
                bottom_lower  # No
            ])
            self.points = points


class Trapezoid(Transform):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        pre_val = 1.00
        if pre_val:
            side_len = st.number_input(
                "Area of trapezoid in inches?", value=pre_val)
            self.size = side_len
            bottom_lower = np.array((0, 0, 0))
            points = np.vstack([
                bottom_lower,  # No
                bottom_lower + [side_len * -0.5, side_len, 0],  # Yes
                bottom_lower + [side_len * 1.5, side_len, 0],  # Yes
                bottom_lower + [side_len * 1.5, 0, 0],  # Yes
                bottom_lower + [0, 0, side_len],  # No
                bottom_lower + [0, side_len, side_len],  # No
                bottom_lower + [side_len, side_len, side_len],  # No
                bottom_lower + [side_len, 0, side_len],  # No
                bottom_lower + [side_len * -0.5, 0, 0]  # Yes
            ])
            self.points = points


class RightTri(Transform):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        pre_val = 1.00
        if pre_val:
            side_len = st.number_input(
                "Area of right triangle in inches?", value=pre_val)
            self.size = side_len
            bottom_lower = np.array((0, 0, 0))
            points = np.vstack([
                bottom_lower,  # No
                bottom_lower + [0, side_len, 0],  # No
                bottom_lower + [side_len, side_len, 0],  # No
                bottom_lower + [side_len, 0, 0],  # No
                bottom_lower + [0, 0, side_len],  # No
                bottom_lower + [0, side_len, side_len],  # No
                bottom_lower + [0, side_len, 0],  # yes
                bottom_lower + [0, 0, 0],  # Yes
                bottom_lower + [0, 0, 0]  # No
            ])
            self.points = points


class SqPyramid(Transform):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        pre_val = 1.00
        if pre_val:
            side_len = st.number_input(
                "Area of square pyramid in inches?", value=pre_val)
            self.size = side_len
            bottom_lower = np.array((0, 0, 0))
            points = np.vstack([
                bottom_lower,
                bottom_lower + [0, side_len, 0],
                bottom_lower + [side_len, 0, 0],  # Yes
                bottom_lower + [side_len, 0, 0],
                bottom_lower + [side_len * 0.5,
                                side_len * 0.5, side_len],  # Yes
                bottom_lower + [0, 0, 0],  # Yes
                bottom_lower + [side_len, side_len, 0],  # Yes
                bottom_lower + [0, 0, 0],  # Yes
                bottom_lower
            ])
            self.points = points


def main():
    st.write("# Activity 4: 3D Objects and Transformation")

    obj_to_plt = st.selectbox("Object to plot?", [
        "Cube", "Cuboid", "Trapezoid", "Right Triangle", "Square Pyramid"])
    obj = None

    if obj_to_plt == "Cube":
        obj = Cube()
    elif obj_to_plt == "Cuboid":
        obj = Cuboid()
    elif obj_to_plt == "Cuboid":
        obj = Trapezoid()
    elif obj_to_plt == "Cuboid":
        obj = RightTri()
    else:
        obj = SqPyramid()

    col1, col2 = st.columns(2)
    col1.markdown("**Original**")
    col1.pyplot(obj.plot())

    trnsf_func = st.selectbox("Transform object with?", [
        "Translate", "Rotate", "Scale", "Shear"])

    if trnsf_func == "Translate":
        obj.translate()
    elif trnsf_func == "Rotate":
        obj.rotate()
    elif trnsf_func == "Scale":
        obj.scale()
    else:
        obj.shear()

    col2.markdown("**Transformed**")
    col2.pyplot(obj.plot())


if __name__ == '__main__':
    main()
