import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import csv
import yaml

base_colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0),
                    (255,0,255), (0,255,255), (0,140,255), (140,255,0),
                    (255,140,0), (0,255,140), (255,140,140), (140,255,140),
                    (140,140,255), (140,140,140)]
gray_color = (100,100,100)

with open('240308_120_square.yaml','r') as f:
    cfg = yaml.load(f,Loader=yaml.FullLoader)

# print(cfg)
# print('--------------')
keypoint = cfg['Keypoints']
line = []
print(cfg['Skeleton'])
for i in cfg['Skeleton']:
    keys = cfg['Skeleton'][f'{i}']['Keypoints']
    fir = keypoint.index(keys[0])
    sec = keypoint.index(keys[1])
    line.append([fir,sec])



with open('data3D.csv', 'r',) as f:
    csvreader = csv.reader(f,delimiter=',')
    next(csvreader)
    next(csvreader)
    position = []
    for i in csvreader:
        frame = []
        for j in range(0,len(i),4):
            pos = list(map(float,[i[j],i[j+1],i[j+2]]))
            frame.append(pos)
        position.append(frame)
    position = np.array(position)
    # print(position)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.view_init(elev=-170)
ax.set_xlim(position[:,:,0].min(),position[:,:,0].max())
ax.set_ylim(position[:,:,1].min(),position[:,:,1].max())
ax.set_zlim(position[:,:,2].min(),position[:,:,2].max())
# ax.set_axis_off()
# ax.margins(0)
# print(position[0][line[0][0]][0])
# print(line)
print('plotting....')


# ax.azim = azim
# ax.elev = elev

# def gen():
#     for frame in position:
#         yield frame
def gen(position):
    for i in position:
        yield i

def update(num,positions,target):
    p = positions[num]
    # print(target)
    for i in range(len(line)):
        target[i][0].set_data_3d([p[line[i][0]][0],p[line[i][1]][0]],[p[line[i][0]][1],p[line[i][1]][1]],[p[line[i][0]][2],p[line[i][1]][2]])

# data = np.array(list(gen(position)))
target = []
for i in range(len(line)):
    target.append(ax.plot3D([position[0][line[i][0]][0],position[0][line[i][1]][0]],[position[0][line[i][0]][1],position[0][line[i][1]][1]],[position[0][line[i][0]][2],position[0][line[i][1]][2]]))

# for frame in position:
#     for l in line:
#         print(frame[l[0]], frame[l[1]])
#     break




ani = FuncAnimation(fig,update,position.shape[0],fargs=(position,target),interval=8.3,cache_frame_data=False)
FFwriter = FFMpegWriter(fps=120)
ani.save('move.mp4',writer=FFwriter)
# plt.show()