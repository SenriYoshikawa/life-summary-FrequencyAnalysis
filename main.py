import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import math

for i in range(1, len(sys.argv)):
    infile = open(sys.argv[i], 'r')
    reader = csv.reader(infile)

    data_list = []
    activeDays = [0 for i in range(32)]
    pre_date = next(reader)[0]
    infile.seek(0)

    for row in reader:
        date = row[0]

        if pre_date[0:-3] != date[0:-3]:
            print(sys.argv[i][0:-4] + "-" + pre_date[0:-3] + " exported")
            plt.clf()
            plt.figure(1)

            plt.suptitle(sys.argv[i][0:-4] + "'s data in" + pre_date[0:-3])

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
            plt.ylim(-16, 20)
            plt.text(50000,17, str(activeDays.count(1)) + " active days", fontsize = 7)

            F = np.fft.fft(data_list)
            FAbs = np.abs(F)[0:math.ceil(len(F)/2)] / activeDays.count(1)

            #FFT結果の絶対値
            plt.subplot(223)
            plt.plot(FAbs)
            plt.title("FFT result")

            #FFT結果の絶対値
            plt.subplot(224)
            q = math.ceil(len(FAbs) / 4)
            quarter = np.array([math.ceil(sum(FAbs[0:q])),
                               math.ceil(sum(FAbs[q:q*2])),
                               math.ceil(sum(FAbs[q*2:q*3])),
                               math.ceil(sum(FAbs[q*3:q*4]))])
            plt.pie(quarter,
                    labels = ["q1", "q2", "q3", "q4"],
                    counterclock=False,
                    startangle=90,
                    autopct="%1.1f%%")
            plt.axis('equal')
            plt.title("Frequency ratio")


            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            plt.savefig(sys.argv[i][0:-4] + "-" + pre_date[0:-3] + ".png")

            data_list.clear()
            pre_date = date

        if date[-2:] == "01" and row[1] == "00:00":
            activeDays = [0 for i in range(32)]

        if len(row) > 2:
            data_list.append(0 if (row[2] == 'x' or row[2] == 'X') else int(row[2], 16))
            if len(row) > 3:
                data_list.append(0 if (row[3] == 'x' or row[3] == 'X') else -int(row[3], 16))
            else:
                data_list.append(0)

        if data_list[-1] != 0 or data_list[-2] != 0:
            activeDays[int(date[-2:])] = 1
