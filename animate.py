import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

#  read a npy file
x = np.load('11.npy', allow_pickle=True)
print(x.shape)
trial=x[13]
gazex=trial[:,0]
gazey=trial[:,1]
print(gazex,gazey)
print(gazex.shape, gazey.shape)
print(gazex[gazex.shape[0]-1])


fig, ax = plt.subplots()
x, y = [],[]
sc = ax.scatter(x,y)


screen_dim = [1920,1080]
# fig = plt.figure(1, figsize=(12, 9))
# ax = fig.add_subplot(111)
img = plt.imread("background.png")
ax.imshow(img, extent=[0, screen_dim[0], screen_dim[1], 0])

plt.xlim((0, screen_dim[0]))
plt.ylim((screen_dim[1], 0))
plt.axis('scaled')
# plt.scatter(gaze_array[:, 0], gaze_array[:, 1])
plt.axis('auto')
# plt.savefig("aoi.png")
# plt.show()





def animate(i):
    if i==gazex.shape[0]-1:
        plt.close()
    # print(i)
    # print(gazex[i])
    x.append(gazex[i])
    y.append(gazey[i])
    # print(x)
    sc.set_offsets(np.c_[x,y])

ani = matplotlib.animation.FuncAnimation(fig, animate, frames=gazex.shape[0]-1, interval=10, repeat=False)
# anim = matplotlib.animation.FuncAnimation(fig, animate, frames=gazex.shape, interval=300, blit=True)
# ani.save('test.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

# # saving to m4 using ffmpeg writer
writervideo = matplotlib.animation.FFMpegWriter(fps=60)
ani.save('gaze_anim.mp4', writer=writervideo)

# plt.show()