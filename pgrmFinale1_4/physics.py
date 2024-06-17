import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.spatial.transform import Rotation as R

def integrate(df):
    """
    Integrate the velocity values in the given DataFrame to calculate the corresponding position values.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the velocity values.

    Returns:
    None

    Modifies:
    - Adds 'vel_x', 'vel_y', 'vel_z', 'pos_x', 'pos_y', 'pos_z' columns to the DataFrame.

    """
    df['vel_x'] = cumulative_trapezoid(df.iloc[:, 4], initial=0)
    df['vel_y'] = cumulative_trapezoid(df.iloc[:, 5], initial=0)
    df['vel_z'] = cumulative_trapezoid(df.iloc[:, 6], initial=0)
    df['pos_x'] = cumulative_trapezoid(df['vel_x'], initial=0)
    df['pos_y'] = cumulative_trapezoid(df['vel_y'], initial=0)
    df['pos_z'] = cumulative_trapezoid(df['vel_z'], initial=0)

def adjustDrift(df, pos, offset):
    """
    Adjusts the drift of a DataFrame based on the specified position and offset.

    Parameters:
    - df (DataFrame): The DataFrame to adjust.
    - pos (str): The position to adjust ('x', 'y', or 'z').
    - offset (float): The offset value to add to the specified position.

    Returns:
    None
    """
    if pos == 'x':
        df['pos_x'] += offset
    if pos == 'y':
        df['pos_y'] += offset
    if pos == 'z':
        df['pos_z'] += offset

def adjustAngle(df, angle, offset):
    """
    Adjusts the specified angle in the given DataFrame by subtracting the initial value and adding the offset.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the angle values.
    - angle (str): The angle to be adjusted ('x', 'y', or 'z').
    - offset (float): The offset value to be added to the adjusted angle.

    Returns:
    None
    """
    if angle == 'x':
        df['Euler_X'] = df['Euler_X'] - df.iloc[0, 1] + offset
    if angle == 'y':
        df['Euler_Y'] = df['Euler_Y'] - df.iloc[0, 2] + offset
    if angle == 'z':
        df['Euler_Z'] = df['Euler_Z'] - df.iloc[0, 3] + offset

def rotatePositions(df):
    """
    Rotate the positions in the given DataFrame using Euler angles.

    Args:
    - df (pandas.DataFrame): The DataFrame containing the positions.

    Returns:
    tuple: A tuple containing three lists representing the rotated positions along the X, Y, and Z axes respectively.
    """
    trajX = []
    trajY = []
    trajZ = []
    for i in range(df.shape[0]-1):
        r_mat = R.from_euler("xyz", [df.iloc[i+1,1], df.iloc[i+1,2], df.iloc[i+1,3]], degrees=True)
        pos_1 = r_mat.apply([df['pos_x'][i+1],df['pos_y'][i+1],df['pos_z'][i+1]])
        trajX.append(pos_1[0])
        trajY.append(pos_1[1])
        trajZ.append(pos_1[2])
    return trajX, trajY, trajZ

def adjustLength(trajX, trajY, trajZ, length):
    """
    Adjusts the length of trajectory vectors based on a given length.

    Parameters:
    - trajX (float): The x-component of the trajectory vector.
    - trajY (float): The y-component of the trajectory vector.
    - trajZ (float): The z-component of the trajectory vector.
    - length (float): The desired length of the trajectory vector.

    Returns:
    tuple: A tuple containing the adjusted x, y, and z components of the trajectory vector.
    """
    trajX = trajX * 10E-8 * 51 / 7.7 * length / 500
    trajY = trajY * 10E-8 * 51 / 7.7 * length / 500
    trajZ = trajZ * 10E-8 * 51 / 7.7 * length / 500
    return trajX, trajY, trajZ

def calculateOneExtremity(df, trajX, trajY, trajZ, length, orientation, direction):
    """
    Calculate the trajectory of an extremity based on the given parameters.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the orientation data.
    - trajX (list): The X-coordinate trajectory.
    - trajY (list): The Y-coordinate trajectory.
    - trajZ (list): The Z-coordinate trajectory.
    - length (float): The length of the extremity.
    - orientation (str): The orientation of the extremity ("plus" or "minus").
    - direction (str): The direction of the extremity ("x", "y", or "z").

    Returns:
    trajExtremityX (list): The X-coordinate trajectory of the extremity.
    trajExtremityY (list): The Y-coordinate trajectory of the extremity.
    trajExtremityZ (list): The Z-coordinate trajectory of the extremity.
    """
    trajExtremityX = []
    trajExtremityY = []
    trajExtremityZ = []

    if orientation == "plus":
        length = length
    else:
        length = -length

    if direction == "x":
        for i in range(len(trajX)-1):
            r_mat = R.from_euler("xyz", [df.iloc[i+1,1], df.iloc[i+1,2], df.iloc[i+1,3]], degrees=True)
            r_mat_inv = R.from_euler("xyz", [df.iloc[i+1,1], df.iloc[i+1,2], df.iloc[i+1,3]], degrees=True).inv()
            pos_1 = r_mat_inv.apply([trajX[i+1], trajY[i+1], trajZ[i+1]])
            pos_2 = r_mat.apply([pos_1[0]+length, pos_1[1], pos_1[2]])
            trajExtremityX.append(pos_2[0])
            trajExtremityY.append(pos_2[1])
            trajExtremityZ.append(pos_2[2])
    
    if direction == "y":
        for i in range(len(trajX)-1):
            r_mat = R.from_euler("xyz", [df.iloc[i+1,1], df.iloc[i+1,2], df.iloc[i+1,3]], degrees=True)
            r_mat_inv = R.from_euler("xyz", [df.iloc[i+1,1], df.iloc[i+1,2], df.iloc[i+1,3]], degrees=True).inv()
            pos_1 = r_mat_inv.apply([trajX[i+1], trajY[i+1], trajZ[i+1]])
            pos_2 = r_mat.apply([pos_1[0], pos_1[1]+length, pos_1[2]])
            trajExtremityX.append(pos_2[0])
            trajExtremityY.append(pos_2[1])
            trajExtremityZ.append(pos_2[2])

    if direction == "z":
        for i in range(len(trajX)-1):
            r_mat = R.from_euler("xyz", [df.iloc[i+1,1], df.iloc[i+1,2], df.iloc[i+1,3]], degrees=True)
            r_mat_inv = R.from_euler("xyz", [df.iloc[i+1,1], df.iloc[i+1,2], df.iloc[i+1,3]], degrees=True).inv()
            pos_1 = r_mat_inv.apply([trajX[i+1], trajY[i+1], trajZ[i+1]])
            pos_2 = r_mat.apply([pos_1[0], pos_1[1], pos_1[2]+length])
            trajExtremityX.append(pos_2[0])
            trajExtremityY.append(pos_2[1])
            trajExtremityZ.append(pos_2[2])

    return trajExtremityX, trajExtremityY, trajExtremityZ