import numpy as np
import matplotlib.pyplot as plt
import cv2

img=cv2.imread('DATA/90.jpg')

def img_read():
    img=cv2.imread('DATA/90.jpg')
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    plt.imshow(img,cmap='gray')
    return img

img=img_read()


def display_img(img):
    fig=plt.figure(figsize=(12,10))
    ax=fig.add_subplot(111)
    ax.imshow(img,cmap='gray')


white_noise=np.random.randint(low=0,high=2,size=(224,224))
white_noise=white_noise*255

display_img(white_noise)

noise_image=white_noise+img
display_img(noise_image)


kernel=np.ones((5,5),dtype=np.uint8)
result=cv2.erode(img,kernel,iterations=0)
display_img(result) 

img=cv2.cvtColor(result,cv2.COLOR_BGR2RGB)
plt.imshow(result,cmap='gray')