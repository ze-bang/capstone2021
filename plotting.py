import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import csv
bins = int(np.sqrt(5000))
st1 = np.genfromtxt("./capstone_data/30cm_from_sipm_maskingtape_channel4.csv", dtype= float)
mu1, sigma1 = norm.fit(st1)
x1 = np.linspace(min(st1), max(st1), 5000)
pd1 = norm.pdf(x1, mu1, sigma1)
etapos1 = mu1*3*10**8/1.59

st2 = np.genfromtxt("./capstone_data/80cm_from_sipm_maskingtape_channel4.csv", dtype= float)
mu2, sigma2 = norm.fit(st2)
x2 = np.linspace(min(st2), max(st2), 5000)
pd2 = norm.pdf(x2, mu2, sigma2)
etapos2 = mu2*3*10**8/1.59

st3 = np.genfromtxt("./capstone_data/150cm_from_sipm_maskingtape_channel4.csv", dtype= float)
mu3, sigma3 = norm.fit(st3)

x3 = np.linspace(min(st3), max(st3), 5000)
pd3 = norm.pdf(x3, mu3, sigma3)

etapos3 = mu3*3*10**8/1.59
mold = np.ones((1,5000));

steps = 4
data_entry = np.zeros((2*steps+3, 2, 5000), dtype=float)
data_img = np.zeros((2*steps+3, 5000))
data_entry[0] = [x1, pd1]
data_img[0] = pd1
for i in range(steps):
    num = i+1
    mu = (etapos1 + num*(etapos2 - etapos1)/(steps+1))*1.59/(3*10**8)

    sigma = (sigma1 + num*(sigma2 - sigma1)/(steps+1))
    x_temp = np.linspace(2.5*sigma+mu, mu-2.5*sigma, 5000)
    pdf_temp = norm.pdf(x_temp, mu, sigma)
    data_entry[num] = [x_temp, pdf_temp]
    data_img[num] = pdf_temp
data_entry[5] = [x2, pd2]
data_img[5] = pd2
for i in range(steps):
    num = i+1

    mu = (etapos2 + num*(etapos3 - etapos2)/(steps+1))*1.59/(3*10**8)

    sigma = (sigma2 + num*(sigma3 - sigma2)/(steps+1))
    x_temp = np.linspace(2.5*sigma+mu, mu-2.5*sigma, 5000)
    pdf_temp = norm.pdf(x_temp, mu, sigma)
    data_entry[5+num] = [x_temp, pdf_temp]
    data_img[5+num] = pdf_temp
data_entry[10] = [x3, pd3]
data_img[10] = pd3
#
fig = plt.figure(figsize=(15.34,7.58))
# thismanager = plt.get_current_fig_manager()
# thismanager.window.wm_geometry("+-7+0")
# fig.canvas.set_window_title('')
# fig.suptitle("Timing resolution at different position of the fiber", fontsize=16)
#
# ax = fig.add_subplot(1,1,1)
# img = ax.imshow(data_img,cmap='jet',aspect='auto',origin='lower',extent=(-1.8*10**(-8),-0.2*10**(-8),0,1.5))
# ax.set_xlabel("Timing resolution")
# ax.set_ylabel("Position")
# plt.colorbar(img)

ax = fig.add_subplot(111, projection = '3d')
ax.scatter(data_entry[0][0], data_entry[0][1], 30*mold)
ax.scatter(data_entry[1][0], data_entry[1][1], 40*mold)
ax.scatter(data_entry[2][0], data_entry[2][1], 50*mold)
ax.scatter(data_entry[3][0], data_entry[3][1], 60*mold)
ax.scatter(data_entry[4][0], data_entry[4][1], 70*mold)
ax.scatter(data_entry[5][0], data_entry[5][1], 80*mold)
ax.scatter(data_entry[6][0], data_entry[6][1], 94*mold)
ax.scatter(data_entry[7][0], data_entry[7][1], 108*mold)
ax.scatter(data_entry[8][0], data_entry[8][1], 122*mold)
ax.scatter(data_entry[9][0], data_entry[9][1], 136*mold)
ax.scatter(data_entry[10][0], data_entry[10][1], 150*mold)

ax.set_xlabel('Time delay between SiPM / $s^{-1}$', fontsize=10, rotation=150)
ax.set_ylabel('Counts')
ax.set_zlabel('Distance away from SiPM #4 / $cm$', fontsize=10, rotation=60)
plt.show()

