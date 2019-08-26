import random
import time 
from dan import NoData
import dai

import threading
'''
from pydub import AudioSegment
from pydub.playback import play
'''
### The register server host, you can use IP or Domain.
host = 'http://garden2.iottalk.tw/csm'

### [OPTIONAL] The register port, default = 9992
# port = 9992

### [OPTIONAL] If not given or None, server will auto-generate.
# device_name = 'Dummy_Test'

### [OPTIONAL] If not given or None, DAN will register using a random UUID.
### Or you can use following code to use MAC address for device_addr.
# from uuid import getnode
# device_addr = "{:012X}".format(getnode())
#device_addr = "aa8e5b58-8a9b-419b-b8d5-72624d61108d"

### [OPTIONAL] If not given or None, this device will be used by anyone.
username = 'A'

### The Device Model in IoTtalk, please check IoTtalk document.
device_model = 'Musictalk'

### The input/output device features, please check IoTtalk document.
idf_list = ['Note_i']
odf_list = ['Note_o']

### Set the push interval, default = 1 (sec)
### Or you can set to 0, and control in your feature input function.
push_interval = 0  # global interval
interval = {
    'Note_i': 0,  # assign feature interval
}

music_file = "night.wav"
data_file = "night.txt"


def register_callback():
    print('register successfully')

'''
global action_list
action_list = []
f = open('night.txt','r')
for line in f:
    line_action = line.strip().split(',')
    action_list.append(line_action[2])
# end of parsing
f.close()
'''

class ColorMapping:
    def __init__(self):
        """
        F#: (145, 25, 62) -> purple-red(?), 6
        G: (174, 0, 0) -> dark read, 7
        G#: (255, 0, 0) -> red, 8
        A: (255, 102, 0) -> orange-red, 9
        B-: (255, 239, 0) -> yello, 10
        B: (155, 255, 0) -> chartreuse, 11
        C: (40, 255, 0) -> lime, 0
        C#: (0, 255, 242) -> aqua, 1
        D: (0, 122, 255) -> sky blue, 2
        D#: (5, 0, 255) -> blue, 3
        E: (71, 0, 237) -> blue-indigo, 4
        F: (99, 0, 178) -> indigo, 5
        """
        self.freq_map = [65,69,73,78,82,87,92,98,104,110,117,123,
                         131,139,147,156,165,175,185,196,208,220,233,247,
                         262,277,294,311,330,349,370,392,415,440,466,494,
                         523,554,587,622,659,698,740,784,831,880,932,988]
        self.color_map = [[40, 255, 0], [0, 255, 242], [0, 122, 255], [
            5, 0, 255
        ], [71, 0, 237], [99, 0, 178], [145, 25, 62], [174, 0, 0], [255, 0, 0],
                          [255, 102, 0], [255, 239, 0], [155, 255, 0]]

    def get_data_color(self, freq):
        i = 0
        idx = 0
        for i in range(len(self.freq_map)):
            if (self.freq_map[i] <= freq and freq < self.freq_map[i+1]):
                if(freq-self.freq_map[i] > self.freq_map[i+1]-freq): idx=i+1
                else: idx = i
                break
        freq_to_color = idx % 12
        return self.color_map[freq_to_color]


time_sleep_list = []
color_list = []
time_tmp = 0
def ToDoList(data_file):
    global time_tmp
    data_color = ColorMapping()
    f = open(data_file,'r')
    for line in f:
        line_action = line.strip().split(',')
        time_sleep_list.append(float(line_action[0])-time_tmp)
        time_tmp = float(line_action[0])
        color = data_color.get_data_color(int(line_action[2]))
        color_list.append(color)
    # end of parsing
    f.close()


ToDoList(data_file)
'''
seq = 0
while (seq < len(color_list)):
    print (seq, time_sleep_list[seq])
    seq += 1
    print (color_list[seq-1])    
'''

seq = 0
def Note_i():
    global seq, time_sleep_list, color_list
    # job_of_play_music()
    while (seq < len(color_list)):
        time.sleep(time_sleep_list[seq])
        seq += 1
        return color_list[seq-1]


def Note_o(data):  # data is a list
    #data = list(map(int,data))
    print (data)
    return 0
