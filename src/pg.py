import os
import sys
import math
from PIL import Image
import numpy as np

imageFiles = []
for root, dirs, files in os.walk(sys.argv[1]):
    for fname in files:
        filename, extension = os.path.splitext(fname)
        if extension == ".jpg" or extension == ".jpeg":
            imageFiles.append(fname)

# Big image dimension
N = int(math.sqrt(len(imageFiles)))
P = 128

fullData = np.zeros((N * P, N * P, 4), dtype=np.uint8)

row = 0
col = 0
count = 0
limit = (N * N)

for fname in imageFiles:
    im = Image.open(fname).convert('RGBA')

    data = np.array(im)
    print type(data[0])
    print type(data[0][1])
    # red, green, blue, alpha = data.T

    while data.shape[0] > (2 * P):
        data = data[1::2]
    while data.shape[1] > (2 * P):
        data = np.delete(data, np.s_[1::2], 1)

    for i in range(P):
        for j in range(P):
            fullData[row + i][col + j] = data[i][j]

    # Update the row...
    count += 1
    col += P
    if (col == (N * P)):
        col = 0
        row += P

    print row, col, data.shape, fullData.shape, count
    if count == limit:
        break # done with all of the images...

im2 = Image.fromarray(fullData)
im2.show()
im2.save("fig.png")
