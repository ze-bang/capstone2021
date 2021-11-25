import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import csv


st1 = np.genfromtxt("./capstone_data/30cm_from_sipm_maskingtape_channel4.csv", dtype= float)
st2 = np.genfromtxt("./capstone_data/80cm_from_sipm_maskingtape_channel4.csv", dtype= float)
st3 = np.genfromtxt("./capstone_data/150cm_from_sipm_maskingtape_channel4.csv", dtype= float)
x = np.linspace(min(st1), max(st3), 20000)
mu1, sigma1 = norm.fit(st1)
pd1 = norm.pdf(x, mu1, sigma1)
etapos1 = mu1*3*10**8/1.59

mu2, sigma2 = norm.fit(st2)
pd2 = norm.pdf(x, mu2, sigma2)
etapos2 = mu2*3*10**8/1.59

mu3, sigma3 = norm.fit(st3)
pd3 = norm.pdf(x, mu3, sigma3)
etapos3 = mu3*3*10**8/1.59
mold = np.ones((1,20000));

steps = 4
data_img = np.zeros((2*steps+3, 20000))
data_img[0] = pd1
for i in range(steps):
    num = i+1
    mu = (etapos1 + num*(etapos2 - etapos1)/(steps+1))*1.59/(3*10**8)

    sigma = (sigma1 + num*(sigma2 - sigma1)/(steps+1))
    pdf_temp = norm.pdf(x, mu, sigma)
    data_img[num] = pdf_temp
data_img[5] = pd2

for i in range(steps):
    num = i+1

    mu = (etapos2 + num*(etapos3 - etapos2)/(steps+1))*1.59/(3*10**8)

    sigma = (sigma2 + num*(sigma3 - sigma2)/(steps+1))
    pdf_temp = norm.pdf(x, mu, sigma)
    data_img[5+num] = pdf_temp
data_img[10] = pd3

print(data_img)

fig = plt.figure(figsize=(15.34,7.58))
thismanager = plt.get_current_fig_manager()
thismanager.window.wm_geometry("+-7+0")
fig.canvas.set_window_title('')
fig.suptitle("Timing resolution at different position of the fiber", fontsize=16)

ax = fig.add_subplot(1,1,1)
img = ax.imshow(data_img,cmap='jet',aspect='auto',origin='lower',extent=(-1.8*10**(-8),-0.2*10**(-8),0,1.5))
ax.set_xlabel("Time delayed between 2 SiPMs")
ax.set_ylabel("Position away from SiPM#4 / $m$")
plt.colorbar(img)

plt.show()