import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import math

for i in range(1, len(sys.argv)):
    infile = open(sys.argv[i], 'r')
    reader = csv.reader(infile)

    data_list = []
    pre_date = next(reader)[0][0:-3]
    infile.seek(0)

    for row in reader:
        date = row[0][0:-3]

        if pre_date != date:
            print(sys.argv[i][0:-4] + "-" + pre_date + " exported")
            plt.clf()
            plt.figure(1)

            plt.subplot(221)
            plt.plot(data_list[480:1200])
            #毎月1日の午前８時から午後８時をサンプルとして描画

            plt.subplot(222)
            plt.plot(data_list)
            plt.title(sys.argv[i][0:-4] + "-" + pre_date)

            F = np.fft.fft(data_list)
            plt.subplot(223)
            plt.plot(np.abs(F)[0:math.ceil(len(F))])
            plt.xlim(0, len(data_list) / 2)

            plt.savefig(sys.argv[i][0:-4] + "-" + pre_date + ".png")
            data_list.clear()

            pre_date = date

        if len(row) > 2:
            data_list.append(0 if (row[2] == 'x' or row[2] == 'X') else int(row[2], 16))
            if len(row) > 3:
                data_list.append(0 if (row[3] == 'x' or row[3] == 'X') else -int(row[3], 16))
            else:
                data_list.append(0)

