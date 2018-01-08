import time
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader as reader
from mindwavemobile.MindwaveDataPoints import *

if __name__ == '__main__':
    data_list = []
    temp = 0
    med = 0
    att = 0
    f = open("data.txt", 'w')

    reader = reader()
    reader.start()
    if (reader.isConnected()):
        while True:
            data = reader.readNextDataPoint()
            if (data.__class__ is MeditationDataPoint):
                med = data.meditationValue
                temp = time.time()

            elif(data.__class__ is AttentionDataPoint):
                att = data.attentionValue
                unit = [temp, med, att]
                data_list.append(unit)
                print(unit)
                f.write(str(unit) + '\n')
                f.flush()
        f.close()

    else:
        print("device disconnected")