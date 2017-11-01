import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import math
import glob
import os

if len(sys.argv) > 0 and sys.argv[1].find('csv') == -1:
    sys.argv.extend(glob.glob(sys.argv[1] + '*.csv'))
    del sys.argv[1]

for i in range(1, len(sys.argv)):
    infile = open(sys.argv[i], 'r')
    sys.argv[i] = sys.argv[i][sys.argv[i].rfind('/') + 1:]
    sys.argv[i] = sys.argv[i][sys.argv[i].rfind('\\') + 1:]

    try:
        os.mkdir(sys.argv[i][:-4])
    except FileExistsError:
        pass

    sys.argv[i] = sys.argv[i][:-4] + '/' + sys.argv[i]
    outfile = open(sys.argv[i][:-4] + "-result.csv", 'w')
    reader = csv.reader(infile)

    data_list = []
    result_data = [[] for j in range(4)]
    result_date = []

    activeDays = [0 for i in range(32)]
    pre_date = next(reader)[0]
    infile.seek(0)

    for row in reader:
        date = row[0]

        if pre_date[0:-3] != date[0:-3]:
            plt.clf()
            # plt.figure(figsize = (16,12))
            plt.figure(1)

            plt.suptitle(sys.argv[i][0:-4] + "'s data in" + pre_date[0:-3])

            # 毎月1日の午前８時から午後８時をサンプルとして描画
            plt.subplot(221)
            plt.ylim(-16, 16)
            plt.xticks([0, 320, 640, 960], ["8", "12", "16", "20"])
            plt.plot(data_list[960:1920], linewidth=0.1)
            plt.title("day 1")

            # 一ヶ月
            plt.subplot(222)
            plt.plot(data_list, linewidth=0.1)
            plt.title("A month activity volume")
            plt.xticks([0, 20160, 40320, 60480, 80640], ["1", "7", "14", "21", "28"])
            plt.ylim(-16, 20)
            plt.text(50000, 17, str(activeDays.count(1)) + " active days", fontsize=7)

            # データがある月はFFTを計算
            if activeDays.count(1) != 0:
                F = np.fft.fft(data_list)
                freqList = np.fft.fftfreq(len(F), d=1.0 / 2)[0:math.ceil(len(F) / 2)]
                FAbs = np.abs(F)[0:math.ceil(len(F) / 2)] / activeDays.count(1)

                # FFT結果の絶対値
                plt.subplot(223)
                plt.plot(freqList, FAbs)
                plt.xscale("log")
                plt.ylim(0, 1000)
                plt.title("FFT result")

                # FFT結果の円グラフ
                plt.subplot(224)
                FAbs[np.isnan(FAbs)] = 0
                q = math.ceil(len(FAbs) / 4)

                quarter = [math.ceil(sum(FAbs[0:q])),
                                    math.ceil(sum(FAbs[q:q * 2])),
                                    math.ceil(sum(FAbs[q * 2:q * 3])),
                                    math.ceil(sum(FAbs[q * 3:q * 4]))]

                plt.pie(quarter,
                        labels=["q1", "q2", "q3", "q4"],
                        counterclock=False,
                        startangle=90,
                        autopct="%1.1f%%")
                plt.axis('equal')
                plt.title("Frequency ratio")
                plt.title("FFT result")

                qsum = sum(quarter)
                outfile.write(pre_date[:-3] + ',' +
                            str(quarter[0] / qsum) + ',' +
                            str(quarter[0] / qsum) + ',' +
                            str(quarter[0] / qsum) + ',' +
                            str(quarter[0] / qsum) + '\n')

                result_date.append(pre_date[:-3])
                result_data[0].append(quarter[0] / qsum * 100)
                result_data[1].append(quarter[1] / qsum * 100)
                result_data[2].append(quarter[2] / qsum * 100)
                result_data[3].append(quarter[3] / qsum * 100)

            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            plt.savefig(sys.argv[i][0:-4] + "-" + pre_date[0:-3] + ".png")
            print(sys.argv[i][0:-4] + "-" + pre_date[0:-3] + " exported")

            data_list.clear()
            pre_date = date

        if date[-2:] == "01" and row[1] == "00:00":
            activeDays = [0 for i in range(32)]

        if len(row) > 2:
            data_list.append(0 if (row[2] == 'x' or row[2] == 'X' or row[2] == "0") else int(row[2], 16))
            if len(row) > 3:
                data_list.append(0 if (row[3] == 'x' or row[3] == 'X' or row[3] == "0") else -int(row[3], 16))
            else:
                data_list.append(0)
        else:
            data_list.append(0)
            data_list.append(0)

        if data_list[-1] != 0 or data_list[-2] != 0:
            activeDays[int(date[-2:])] = 1

    plt.clf()
    plt.plot(result_data[0], "-o", label="Q1")
    plt.plot(result_data[1], "-o", label="Q2")
    plt.plot(result_data[2], "-o", label="Q3")
    plt.plot(result_data[3], "-o", label="Q4")

    plt.xlabel("month")
    q = math.ceil(len(result_date) / 3)
    plt.xticks([0, q, q*2, q*3], [result_date[0], result_date[q], result_date[q*2], result_date[-1]])
    plt.ylabel("%")
    plt.title(sys.argv[i][0:-4] + "each frequent rate")

    plt.savefig(sys.argv[i][0:-4] + "-result.png")
