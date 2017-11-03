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
    result = [[]]
    activeDays = [0 for i in range(32)]
    pre_date = next(reader)[0]
    infile.seek(0)

    for row in reader:
        date = row[0]

        if pre_date[0:-3] != date[0:-3]:
            plt.clf()
            # plt.figure(figsize = (16,12))
            plt.figure(1)

            plt.suptitle(sys.argv[i][0:-4] + "'s data in" + pre_date[0:-3] + 'volume living')

            # 毎月1日の午前８時から午後８時をサンプルとして描画
            plt.subplot(221)
            plt.xticks([0, 160, 320, 480], ["8", "12", "16", "20"])
            plt.plot(data_list[480:960], linewidth=0.1)
            plt.title("day 1")

            # 一ヶ月
            plt.subplot(222)
            plt.plot(data_list, linewidth=0.1)
            plt.title("A month activity volume")
            plt.xticks([0, 10080, 20160, 30240, 40320], ["1", "7", "14", "21", "28"])
            plt.ylim(0, 18)
            plt.text(25000, 16.5, str(activeDays.count(1)) + " active days", fontsize=7)

            # データがある月はFFTを計算
            if activeDays.count(1) != 0:
                F = np.fft.fft(data_list)
                freqList = np.fft.fftfreq(len(F), d=1.0 / 2)[0:math.ceil(len(F) / 2)]
                FAbs = np.abs(F)[0:math.ceil(len(F) / 2)] / activeDays.count(1)

                # FFT結果の絶対値
                plt.subplot(223)
                plt.plot(freqList, FAbs)
                plt.xscale("log")
                #plt.ylim(0, 1000)
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

            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            plt.savefig(sys.argv[i][0:-4] + "-" + pre_date[0:-3] + ".png")
            print(sys.argv[i][0:-4] + "-" + pre_date[0:-3] + " exported")

            data_list.clear()
            pre_date = date

        if date[-2:] == "01" and row[1] == "00:00":
            activeDays = [0 for i in range(32)]

        if len(row) > 2:
            data_list.append(0 if (row[2] == 'x' or row[2] == 'X' or row[2] == "0") else int(row[2], 16))
        else:
            data_list.append(0)

        if data_list[-1] != 0:
            activeDays[int(date[-2:])] = 1

