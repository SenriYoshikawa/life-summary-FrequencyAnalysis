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

        #if date[0][-2:] == "01" and date[1] == "00:00":
        #    month = [0 for i in range(31)]

        if pre_date != date:
            print(sys.argv[i][0:-4] + "-" + pre_date + " exported")
            plt.clf()
            plt.figure(1)

            plt.suptitle(sys.argv[i][0:-4] + "'s data in" + pre_date)

            # 毎月1日の午前８時から午後８時をサンプルとして描画
            plt.subplot(221)
            plt.xticks([0, 240, 480, 720],["8","12","16","20"])
            plt.plot(data_list[480:1200])
            plt.title("day 1")
            plt.ylim(-16,16)

            #一ヶ月の生活量
            plt.subplot(222)
            plt.plot(data_list)
            plt.title("A month activity volume")
            plt.xticks([0, 20160, 40320, 60480, 80640], ["1", "7", "14", "21", "28"])
            plt.ylim(-16, 16)

            #FFT結果の絶対値
            F = np.fft.fft(data_list)
            plt.subplot(223)
            plt.plot(np.abs(F)[0:math.ceil(len(F)/2)])
            plt.title("FFT result")

            #FFT結果の絶対値
            plt.subplot(224)
            plt.plot(np.abs(F)[0:math.ceil(len(F)/2)])
            plt.title("FFT result detail")
            plt.ylim(0,2000)


            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            plt.savefig(sys.argv[i][0:-4] + "-" + pre_date + ".png")

            data_list.clear()
            pre_date = date

        if len(row) > 2:
            data_list.append(0 if (row[2] == 'x' or row[2] == 'X') else int(row[2], 16))
            if len(row) > 3:
                data_list.append(0 if (row[3] == 'x' or row[3] == 'X') else -int(row[3], 16))
            else:
                data_list.append(0)

        #if data_list[-1] != 0 or data_list[-2] != 0:
        #    month[int(date[0][-2:])] = 1
