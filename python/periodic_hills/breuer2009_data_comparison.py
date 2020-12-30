import pandas as pd
import matplotlib.pyplot as plt


prefix = "./lit/Re_5600/"

path_to_data_1 = prefix+"Breuer2009/"
path_to_data_2 = prefix+"Breuer2009_UFR3-30/"

filename_1 = "Breuer2009"
filename_2 = "Breuer2009_3-30"

# Average velocities u at x = 0.05
data_file_1 = path_to_data_1 + filename_1 + "_01.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_01.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[1]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Average velocities u at x = 2
data_file_1 = path_to_data_1 + filename_1 + "_07.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_04.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[1]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Average velocities u at x = 4
data_file_1 = path_to_data_1 + filename_1 + "_13.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_06.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[1]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()


# Average velocities u at x = 8
data_file_1 = path_to_data_1 + filename_1 + "_19.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_10.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[1]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Average velocities v at x = 0.05
data_file_1 = path_to_data_1 + filename_1 + "_02.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_01.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[2]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Average velocities v at x = 2
data_file_1 = path_to_data_1 + filename_1 + "_08.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_04.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[2]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Average velocities v at x = 4
data_file_1 = path_to_data_1 + filename_1 + "_14.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_06.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[2]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()


# Average velocities v at x = 8
data_file_1 = path_to_data_1 + filename_1 + "_20.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_10.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[2]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()


# Reynolds stresses u'u' at x = 0.05
data_file_1 = path_to_data_1 + filename_1 + "_03.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_01.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[3]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Reynolds stresses u'u' at x = 2
data_file_1 = path_to_data_1 + filename_1 + "_09.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_04.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[3]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Reynolds stresses u'u' at x = 4
data_file_1 = path_to_data_1 + filename_1 + "_15.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_06.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[3]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()


# Reynolds stresses u'u' at x = 8
data_file_1 = path_to_data_1 + filename_1 + "_21.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_10.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[3]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()


# Reynolds stresses v'v' at x = 0.05
data_file_1 = path_to_data_1 + filename_1 + "_04.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_01.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[4]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Reynolds stresses v'v' at x = 2
data_file_1 = path_to_data_1 + filename_1 + "_10.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_04.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[4]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Reynolds stresses v'v' at x = 4
data_file_1 = path_to_data_1 + filename_1 + "_16.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_06.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[4]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()


# Reynolds stresses v'v' at x = 8
data_file_1 = path_to_data_1 + filename_1 + "_22.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_10.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[4]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Reynolds stresses u'v' at x = 0.05
data_file_1 = path_to_data_1 + filename_1 + "_06.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_01.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[5]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Reynolds stresses u'v' at x = 2
data_file_1 = path_to_data_1 + filename_1 + "_12.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_04.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[5]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()

# Reynolds stresses u'v' at x = 4
data_file_1 = path_to_data_1 + filename_1 + "_18.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_06.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[5]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()


# Reynolds stresses u'v' at x = 8
data_file_1 = path_to_data_1 + filename_1 + "_24.csv"
data_1 = pd.read_csv(data_file_1, sep=",")
data_file_2 = path_to_data_2 + filename_2 + "_10.csv"
data_2 = pd.read_csv(data_file_2, sep=";")

plt.figure()
plt.plot(data_1[data_1.columns[1]], data_1[data_1.columns[0]], label="data from paper")
plt.plot(data_2[data_2.columns[5]], data_2[data_2.columns[0]], '--', label="data from UFR 3-30")
plt.legend()
plt.show()
