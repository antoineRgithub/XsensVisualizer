import numpy as np
import pandas as pd
import os
import physics as phy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class Trajectory:
    """
    A class representing all trajectories.
    """

    def __init__(self, fileNames):
        """
        Initializes an instance of the class.

        Parameters:
        - fileNames (list): A list of file names.

        Attributes:
        - __dfs (dict): A dictionary to store DataFrames.
        - trajectories (dict): A dictionary to store trajectories.
        - fileNames (list): A list of file names.
        """
        self.__dfs = dict()
        self.trajectories = dict()
        self.fileNames = fileNames

    def convertFile(self, fileName, separator):
        """
        Converts a file to a pandas DataFrame and stores it in the object's dictionary.

        Parameters:
        - fileName (str): The name of the file to be converted.
        - separator (str): The separator used in the file.

        Returns:
        None
        """
        csvName = fileName + '.csv'
        df = pd.read_csv(os.path.abspath(csvName), index_col=0, sep=separator)
        df = df.dropna()
        self.__dfs[fileName] = df

    def convertFiles(self, separator):
        """
        Converts multiple files using the specified separator.

        Parameters:
        - separator (str): The separator to be used for file conversion.

        Returns:
        None
        """
        for fileName in self.fileNames:
            self.convertFile(fileName, separator)
    
    def integrate(self, fileName):
        """
        Integrate the data in the specified file.

        Parameters:
        - fileName (str): The name of the file containing the data.

        Returns:
        None
        """
        df = self.__dfs[fileName]
        phy.integrate(df)

    def adjustDrift(self, fileName):
        """
        Adjusts the Drift of the given DataFrame by subtracting the offset value from the 'x' column.

        Parameters:
        - fileName (str): The name of the file to adjust the Drift for.

        Returns:
        None
        """
        offset_x = 1.596121e+09 / 2
        df = self.__dfs[fileName]
        phy.adjustDrift(df, 'x', offset_x)
    
    def adjustAngle(self, fileName):
        """
        Adjusts the angles in the DataFrame for the given file.

        Parameters:
        - fileName (str): The name of the file to adjust the angles for.

        Returns:
        None
        """
        df = self.__dfs[fileName]
        phy.adjustAngle(df, 'x', 0)
        phy.adjustAngle(df, 'y', 0)
        phy.adjustAngle(df, 'z', 0)

    def rotatePositions(self, fileName):
        """
        Rotate the positions in the DataFrame for the given file.

        Parameters:
        - fileName (str): The name of the file to rotate positions for.

        Returns:
        None
        """
        df = self.__dfs[fileName]
        trajX, trajY, trajZ = phy.rotatePositions(df)
        self.trajectories[fileName] = [trajX, trajY, trajZ]

    def rotateAll(self):
        """
        Rotates all the positions in the given file names.

        This method iterates through each file name in the `fileNames` list and calls the `rotatePositions` method
        to rotate the positions in each file.

        Parameters:
        - None

        Returns:
        None
        """
        for fileName in self.fileNames:
            self.rotatePositions(fileName)

    def testRowsNumber(self, fileName, rowsNb):
        """
        Test the number of rows to drop in a DataFrame.

        Parameters:
        - fileName (str): The name of the file containing the DataFrame.
        - rowsNb (int): The number of rows to drop.

        Returns:
        bool: True if the number of rows is valid and can be dropped, False otherwise.
        """
        df = self.__dfs[fileName]
        try:
            df_res = df.copy()
            df_res = df_res.drop(int(rowsNb)).copy()
        except ValueError:
            print("\nError: Invalid number of rows to drop.")
            return False
        
    def testAll(self, rowsNb):
        """
        Test all files in the fileNames list to check if they have the specified number of rows.

        Parameters:
        - rowsNb (int): The expected number of rows in each file.

        Returns:
        bool: True if all files have the expected number of rows, False otherwise.
        """
        for fileName in self.fileNames:
            self.testRowsNumber(fileName, rowsNb)
        return True
    
    def adjustLength(self, fileName, length):
        """
        Adjusts the length of the trajectory data for a given file.

        Parameters:
        - fileName (str): The name of the file containing the trajectory data.
        - length (int): The desired length of the trajectory data.

        Returns:
        None

        Modifies the trajectory data for the given file by adjusting its length to the specified value.
        """
        trajX, trajY, trajZ = self.trajectories[fileName]
        trajX = np.array(trajX)
        trajY = np.array(trajY)
        trajZ = np.array(trajZ)
        trajX, trajY, trajZ = phy.adjustLength(trajX, trajY, trajZ, length)
        self.trajectories[fileName] = [trajX, trajY, trajZ]

    def calculateExtremitiesTrajectories(self, fileName, plusLength, minusLength):
        """
        Calculates the extremities trajectories for a given file.

        Parameters:
        - fileName (str): The name of the file.
        - plusLength (int): The length for calculating the plus extremity.
        - minusLength (int): The length for calculating the minus extremity.

        Returns:
        None
        """
        trajX, trajY, trajZ = self.trajectories[fileName]
        trajXPlus, trajYPlus, trajZPlus = phy.calculateOneExtremity(self.__dfs[fileName], trajX, trajY, trajZ, plusLength, "plus", "x")
        trajXMinus, trajYMinus, trajZMinus = phy.calculateOneExtremity(self.__dfs[fileName], trajX, trajY, trajZ, minusLength, "minus", "x")
        self.trajectories[fileName + "Plus"] = [trajXPlus, trajYPlus, trajZPlus]
        self.trajectories[fileName + "Minus"] = [trajXMinus, trajYMinus, trajZMinus]
        trajX = trajX[:len(trajX)-1]
        trajY = trajY[:len(trajY)-1]
        trajZ = trajZ[:len(trajZ)-1]
        self.trajectories[fileName] = [trajX, trajY, trajZ]

    def defineJoint(self, fixedFileName, mobileFileName):
        """
        Adjusts the trajectories of the mobile extremity, mobile centre, and mobile other extremity
        based on the difference between the fixed extremity and mobile extremity.

        Parameters:
        - fixedFileName (str): The name of the fixed extremity file.
        - mobileFileName (str): The name of the mobile extremity file.

        Returns:
        None
        """
        fixedExtremity = fixedFileName + "Plus"
        mobileExtremity = mobileFileName + "Minus"
        mobileCentre = mobileFileName
        mobileOtherExtremity = mobileFileName + "Plus"

        for i in range(len(self.trajectories[fixedExtremity][0])):
            deltaX = self.trajectories[fixedExtremity][0][i] - self.trajectories[mobileExtremity][0][i]
            deltaY = self.trajectories[fixedExtremity][1][i] - self.trajectories[mobileExtremity][1][i]
            deltaZ = self.trajectories[fixedExtremity][2][i] - self.trajectories[mobileExtremity][2][i]
            self.trajectories[mobileExtremity][0][i] = self.trajectories[mobileExtremity][0][i] + deltaX
            self.trajectories[mobileExtremity][1][i] = self.trajectories[mobileExtremity][1][i] + deltaY
            self.trajectories[mobileExtremity][2][i] = self.trajectories[mobileExtremity][2][i] + deltaZ
            self.trajectories[mobileCentre][0][i] = self.trajectories[mobileCentre][0][i] + deltaX
            self.trajectories[mobileCentre][1][i] = self.trajectories[mobileCentre][1][i] + deltaY
            self.trajectories[mobileCentre][2][i] = self.trajectories[mobileCentre][2][i] + deltaZ
            self.trajectories[mobileOtherExtremity][0][i] = self.trajectories[mobileOtherExtremity][0][i] + deltaX
            self.trajectories[mobileOtherExtremity][1][i] = self.trajectories[mobileOtherExtremity][1][i] + deltaY
            self.trajectories[mobileOtherExtremity][2][i] = self.trajectories[mobileOtherExtremity][2][i] + deltaZ

    def calculateTrajectory(self, fileName, plusLength, minusLength):
        """
        Calculates the trajectory of the object based on the given file name and length adjustments.

        Parameters:
        - fileName (str): The name of the file containing the data.
        - plusLength (float): The length to be added to the trajectory.
        - minusLength (float): The length to be subtracted from the trajectory.

        Returns:
        None
        """
        self.integrate(fileName)
        self.adjustDrift(fileName)
        self.adjustAngle(fileName)
        self.rotatePositions(fileName)
        self.adjustLength(fileName, minusLength+plusLength)
          
    def retrieveTrajectory(self, fileName):
        """
        Retrieve the trajectory associated with the given file name.

        Parameters:
        - fileName (str): The name of the file containing the trajectory.

        Returns:
        list: The trajectory associated with the given file name.
        """
        return self.trajectories[fileName]
    
    def retrievePlusTrajectory(self, fileName):
        """
        Retrieve the 'plus' extremity trajectory for a given file name.

        Parameters:
        - fileName (str): The name of the file.

        Returns:
        list: The 'plus' trajectory for the given file name.
        """
        return self.trajectories[fileName + "Plus"]
    
    def retrieveMinusTrajectory(self, fileName):
        """
        Retrieve the 'minus' extremity trajectory for a given file name.

        Parameters:
        - fileName (str): The name of the file.

        Returns:
        list: The minus trajectory associated with the given file name.
        """
        return self.trajectories[fileName + "Minus"]
    
    def retrieveAngle(self, fileName):
        """
        Retrieve the Euler angles from the specified file.

        Parameters:
        - fileName (str): The name of the file to retrieve the angles from.

        Returns:
        list: A list containing the Euler angles [Euler_X, Euler_Y, Euler_Z].
        """
        df = self.__dfs[fileName]
        return [df["Euler_X"], df["Euler_Y"], df["Euler_Z"]]
    
    def exportCSV(self):
        """
        Export the trajectory and angle data of all files to CSV files.

        Returns:
        None
        """
        for fileName in self.fileNames:
            traj = self.retrieveTrajectory(fileName)
            ang = self.retrieveAngle(fileName)
            while len(traj[0]) != len(ang[0]):
                for i in range(len(ang)):
                    ang[i] = ang[i].drop(ang[i].tail(1).index)
            df_res = pd.DataFrame({'x' : traj[0], 'y' : traj[1], 'z' : traj[2], 'eul_x' : ang[0], 'eul_y' : ang[1], 'eul_z' : ang[2] })
            df_res.to_csv(os.path.abspath(f"res_{fileName}.csv/"))
        return
    
    def displayTrajectory(self):
        """
        Display the trajectories in a 3D plot.

        Returns:
        tuple: A tuple containing the matplotlib Axes3D object and the Figure object.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for trajectoryName in self.fileNames:
            plusName = trajectoryName + 'Plus'
            minusName = trajectoryName + 'Minus'
            ax.plot(self.trajectories[plusName][0], self.trajectories[plusName][1], self.trajectories[plusName][2])
            ax.plot(self.trajectories[minusName][0], self.trajectories[minusName][1], self.trajectories[minusName][2])
            ax.plot(self.trajectories[trajectoryName][0], self.trajectories[trajectoryName][1], self.trajectories[trajectoryName][2])

            trajectoriesList = []
            trajectoriesList.extend([self.trajectories[plusName][0], self.trajectories[plusName][1], self.trajectories[plusName][2],
                                self.trajectories[minusName][0], self.trajectories[minusName][1], self.trajectories[minusName][2],
                                self.trajectories[trajectoryName][0], self.trajectories[trajectoryName][1], self.trajectories[trajectoryName][2]])

        ax.set_xlabel('Position X')
        ax.set_ylabel('Position Y')
        ax.set_zlabel('Position Z')

        extremes = np.array(trajectoriesList)
        min_extreme = np.min(extremes)
        max_extreme = np.max(extremes)

        ax.set_xlim([min_extreme, max_extreme])
        ax.set_ylim([min_extreme, max_extreme])
        ax.set_zlim([min_extreme, max_extreme])
        
        ax.set_box_aspect([1,1,1])
        return (ax, fig)

    def displayAnimation(self):
        """
        Display an animation of trajectories in a 3D plot.

        Returns:
        tuple: A tuple containing the axes and figure objects.
        """
        fig = plt.figure()

        ax = fig.add_subplot(111, projection='3d')

        segments = []
        for i in range(len(self.fileNames)):
            segment = ax.plot([], [], [], 'b-')
            segments.append(segment)

            plusName = self.fileNames[i] + 'Plus'
            minusName = self.fileNames[i] + 'Minus'
            trajectoriesList = []
            trajectoriesList.extend([self.trajectories[plusName][0], self.trajectories[plusName][1], self.trajectories[plusName][2],
                                self.trajectories[minusName][0], self.trajectories[minusName][1], self.trajectories[minusName][2]])

        extremes = np.array(trajectoriesList)
        min_extreme = np.min(extremes)
        max_extreme = np.max(extremes)

        margin = 0.1  # 10% de marge
        range_extreme = max_extreme - min_extreme
        ax.set_xlim([min_extreme - margin * range_extreme, max_extreme + margin * range_extreme])
        ax.set_ylim([min_extreme - margin * range_extreme, max_extreme + margin * range_extreme])
        ax.set_zlim([min_extreme - margin * range_extreme, max_extreme + margin * range_extreme])

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        def init():

            for segment in segments:
                segment[0].set_data([], [])
                segment[0].set_3d_properties([])

            return segments

        def update(num):

            for i, segment in enumerate(segments):

                plusName = self.fileNames[i] + 'Plus'
                minusName = self.fileNames[i] + 'Minus'

                segment_x = [self.trajectories[plusName][0][num], self.trajectories[minusName][0][num]]
                segment_y = [self.trajectories[plusName][1][num], self.trajectories[minusName][1][num]]
                segment_z = [self.trajectories[plusName][2][num], self.trajectories[minusName][2][num]]

                segment[0].set_data(segment_x, segment_y)
                segment[0].set_3d_properties(segment_z)

            return segments

        n = len(self.trajectories[self.fileNames[i]][0])


        ani = FuncAnimation(fig, update, frames=n, init_func=init, blit=False, repeat=True, interval=20)

        plt.show()

        return (ax, fig)
