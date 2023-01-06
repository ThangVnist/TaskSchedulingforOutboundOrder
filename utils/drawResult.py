# This file use to draw figure 

from calendar import c
import matplotlib.pyplot as plt

plt.title("Figure 6")
plt.ylabel("total cost Schedule")
plt.xlabel("item number")

n_item = [5,7,10,13,15]
#Scenario 1  -Data set 1 - NSGA II 
objectives_totalCost1 = [[838785.8, 837437.5, 828481.3], [1190373.5, 1165475.7, 1171262.6], [1697152.2, 1671433.6,1671433.6],
[2165429.8, 2166125.2, 2151593.9], [2506486.0, 2554678.4, 2646441.3]]
objectives_totalTime1 = [[3125, 3000, 3239], [4400, 4538, 4517], [6095, 6278, 6278], 
[8744, 8787, 8842], [9187, 9145, 9077]]
objectives_notOnTime1 = [[0 , 0, 0], [2, 2, 2], [7, 7, 7], [9, 9 , 9], [10, 10, 10]]


#Scenario 1  -Data set 1 - Pymoo
objectives_totalCost2 = [[1427207.8, 1386097.5, 1392705.8], [1974721.3, 1996196.1, 2071942.9], [2891728.3, 2886337.7,2827632.3],
[3655065.9, 3641048.7, 3654052.9], [4223665.7, 4223665.7, 4223665.7]]
objectives_totalTime2 = [[1845, 1927, 1855], [2985, 2947, 2932], [3242, 3386, 3295], 
[4532, 4672, 4667], [4754, 4755, 4754]]
objectives_notOnTime2 = [[0 , 0, 0], [0 , 0, 0], [3, 4, 5], [9, 9 , 9], [10, 10, 10]]


#Scenario 2  -Data set 2 - NSGA II 
objectives_totalCost3 = [[832744.6, 830539.2, 839086.9], [1172612.7, 1160941.5,1175447.6], [1658193.6, 1672562.4,1661303.5],
[2185953.1, 2172904.2, 2174435.9], [2510963.3, 2494659.6, 2526133.6]]
objectives_totalTime3 = [[3085, 3308, 3005], [4493, 4679, 4453], [6347, 6278, 6339], 
[7580, 7894, 7742], [8975, 8999, 8868]]
objectives_notOnTime3 = [[0 , 0, 0], [0 , 0, 0], [0 , 0, 0], [0 , 1, 1], [4, 4, 4]]


#Scenario 2  -Data set 2 - Pymoo
objectives_totalCost4 = [[1392705.8, 1386097.5, 1427207.8], [1950220.5, 1959961.8, 1935323.3], [2907162.6, 2784628.2,2911762.7],
[3655065.9, 3641048.7, 3654052.9], [4223665.7, 4223665.7, 4223665.7]]
objectives_totalTime4 = [[1854, 1928, 1846], [3014, 2942, 3227], [3314, 3315, 3285], 
[4532, 4672, 4667], [4754, 4755, 4754]]
objectives_notOnTime4 = [[0 , 0, 0], [0 , 0, 0], [0 , 0, 0], [0 , 0, 0], [0 , 0, 0]]

# Scenario 3 - Data set 2 - NSGA II
objectives_totalCost5 = [[3100973.7, 3674572.5, 2991682.1], [4420546.0, 4802662.3, 4284851.7], [6612689.4, 6488695.7,6647216.0],
[7276632.2, 8064920.8, 7762810.9], [8418167.4, 8587580.4, 8288637.7]]

# Scenario 3 - Data set 2 - Pymoo
objectives_totalCost6 = [[2741868.3, 2819240.3, 2858084.2], [3660028.8, 3788485.6, 3680775.7], [4422270.9, 4400080.6,4492929.4],
[5525249.2, 5608453.3, 5584838.6], [6039542.2, 6038284.7, 6039542.2]]

for i in range(0,5):
    for j in range(0, 3):
        x, y = [], []
        plt.plot(n_item[i], objectives_totalCost5[i][j], 'ro')
        plt.plot(n_item[i], objectives_totalCost6[i][j], 'bo')
# plt.plot([1190373.5, 1165475.7], [4400, 4538], 'bo')
# plt.plot([1697152.2, 1671433.6], [6095, 6278], 'co')
plt.plot(1, 8000000, 'ro')
plt.plot(1, 7000000, 'bo')
plt.text(1.5, 7700000, 'Improved NSGA II')
plt.text(1.5, 6800000, 'Pure NSGA II')
plt.axis([0, 20, 0, 9000000])
plt.show()


# import numpy as np

# # evenly sampled time at 200ms intervals
# t = np.arange(0., 5., 1)

# # red dashes, blue squares and green triangles
# plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
# plt.show()