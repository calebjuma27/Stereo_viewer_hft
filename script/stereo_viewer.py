#-------------------------------------------------------------------------------
# Name:        Creation of a stereoviewing tool
# Purpose:
#
# Author:      juma
#
# Created:     28-10-2019
# Copyright:   (c) juma 2019
# Licence:     Educational DEMO

import tkinter as tk
import os
from math import ceil
from math import sqrt
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import cv2

LARGE_FONT= ('Bodoni MT Black', 12)
Font1=('Copperplate Gothic Bold',11)
Font2=('Times New Roman',12)



class Stereo(tk.Tk):
    def __init__(self,*args,**kwargs): #initilializing the flight planner
        tk.Tk.__init__(self,*args,**kwargs)#initializing the class that we are inheriting
        container=tk.Frame(self)
        self.title("STEREO VIEWING")
        # can use pack or grid to arrange elements in window

        # side packs contents at the top, fill makes sure the top is filled on both sides,
        #if any whitesapce exists(in top or not), it will be filled too as per the expand command.
        container.pack(side='top', fill='both',expand=True )
        container.grid_rowconfigure(0,weight=1)#starting row is 0, no preference as indicated by 1
        container.grid_columnconfigure(0,weight=1)#starting column is 0

        self.frames={}# a dictionary empty but will contain keys and values

        for F in (StartPage, Pageone, Pagetwo, Pagethree):#creating a tuple F containing startpage and pageone
            frame=F(container,self)
            self.frames[F]=frame
            frame.grid(row=0, column=0, sticky='nsew')# sticky stretches and alligns the contents in a frame,nsew=northsoutheastwest
        self.show_frame(StartPage)#showframedoes not yet exist. we will have to create it

    def show_frame(self,cont): #cont means controller
        frame=self.frames[cont]# cont is the key. it will be used to look for the value in our earlier dictionary
        frame.tkraise()# takes that frame and raises it. i.e. we are able to interacct with it


class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self, text='Task 1', font=LARGE_FONT)
        label.pack(pady=10,padx=10)


        def browsefunc():

            browsefunc.filename = tk.filedialog.askopenfilename()
            pathlabel.config(text=browsefunc.filename)




        browsebutton = tk.Button(self, text="Browse for Image file: Zahlen1_9", command=browsefunc)
        browsebutton.pack()


        pathlabel = tk.Label(self)
        pathlabel.pack()



        def Calculate():

            ###load a colour image
            img=cv2.imread(browsefunc.filename)

##            img = cv2.imread('Zahlen1_9.jpg')

            height, width = img.shape[:2]# only consider the rows and columns, leaves ouytthe bands if they exist

            ## cut the left image
            start_row, start_col = int(0), int(0)
            # Let's get the ending pixel coordinates (bottom right of cropped top)
            end_row, end_col = int(height), int(750)
            cropped_top = img[start_row:end_row , start_col:end_col]

            ##cut second right image
            start_row2, start_col2 = int(0), int(750)
            # Let's get the ending pixel coordinates (bottom right of cropped top)
            end_row2, end_col2 = int(height), int(1500 )
            cropped_top2 = img[start_row2:end_row2 , start_col2:end_col2]

            ##dispaly left image (cropped_top)  in red
            Conv_hsv_Gray = cv2.cvtColor(cropped_top, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
            cropped_top[mask == 255] = [0, 0, 255]


            ##dispaly cropped_top in cyan i.e green + blue
            Conv_hsv_Gray = cv2.cvtColor(cropped_top2, cv2.COLOR_BGR2GRAY)
            ret, mask1 = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
            cropped_top2[mask1 == 255] = [255, 255, 0]

            ##do orientation
            # Create translation matrix.
            # If the shift is (x, y) then matrix would be
            # M = [1 0 x]
            #     [0 1 y]

            M = np.float32([[1, 0, -20], [0, 1, 3]])
            (rows, cols) = cropped_top.shape[:2]
            # warpAffine does appropriate shifting given the
            # translation matrix.
            res = cv2.warpAffine(cropped_top, M, (cols, rows))

            #blend the images
            weightedSum = cv2.addWeighted(res, 0.5, cropped_top2, 0.5, 0)

            cv2.imshow('Zahlen1_9 Stereo', weightedSum)
            cv2.waitKey(0) & 0xFF # press any key to close window
            cv2.destroyAllWindows()

        button2=tk.Button(self, text='see Stereo Image', command=Calculate)
        button2_1=tk.Button(self, text='Next', command= lambda:controller.show_frame(Pageone))
        button2.pack()
        button2_1.pack()

class Pageone(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self, text='Task 2', font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        def browsefunc():
            browsefunc.filename = tk.filedialog.askopenfilename()
            pathlabel.config(text=browsefunc.filename)


        browsebutton = tk.Button(self, text="Browse for Image file: RandomDotStereogram", command=browsefunc)
        browsebutton.pack()


        pathlabel = tk.Label(self)
        pathlabel.pack()




        def Calculate():
            ###load a colour image
            img=cv2.imread(browsefunc.filename)

            #img = cv2.imread('RandomDotStereogram.jpg')
            height, width = img.shape[:2]# only consider the rows and columns, leaves ouytthe bands if they exist

            ## cut the left image
            start_row, start_col = int(0), int(0)
            # Let's get the ending pixel coordinates (bottom right of cropped top)
            end_row, end_col = int(height), int(250)
            cropped_top = img[start_row:end_row , start_col:end_col]

            ##cut second right image
            start_row2, start_col2 = int(0), int(250)
            # Let's get the ending pixel coordinates (bottom right of cropped top)
            end_row2, end_col2 = int(height), int(500 )
            cropped_top2 = img[start_row2:end_row2 , start_col2:end_col2]

            ##dispaly left image (cropped_top)  in red
            Conv_hsv_Gray = cv2.cvtColor(cropped_top, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
            cropped_top[mask == 255] = [0, 0, 255]

            ##dispaly cropped_top in cyan i.e green + blue
            Conv_hsv_Gray = cv2.cvtColor(cropped_top2, cv2.COLOR_BGR2GRAY)
            ret, mask1 = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
            cropped_top2[mask1 == 255] = [255, 255, 0]


            ##do orientation
            # Create translation matrix.
            # If the shift is (x, y) then matrix would be
            # M = [1 0 x]
            #     [0 1 y]

            M = np.float32([[1, 0, 6], [0, 1, 0]])
            (rows, cols) = cropped_top.shape[:2]
            # warpAffine does appropriate shifting given the
            # translation matrix.
            res = cv2.warpAffine(cropped_top, M, (cols, rows))

            #blend the images
            weightedSum = cv2.addWeighted(res, 0.5, cropped_top2, 0.5, 0)

            cv2.imshow('RandomDotStereogram stereo', weightedSum)


            cv2.waitKey(0) & 0xFF # press any key to close window
            cv2.destroyAllWindows()
        button3=tk.Button(self, text='see Stereo Image', command=Calculate)#.grid(row=4,column=2)
        button3_1=tk.Button(self, text='Next', command= lambda:controller.show_frame(Pagetwo))
        button3_2=tk.Button(self, text="Back", command= lambda: controller.show_frame(StartPage))

        button3.pack()
        button3_1.pack()
        button3_2.pack()

class Pagetwo(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self, text='Task 3', font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        def browsefunc():
            browsefunc.filename = tk.filedialog.askopenfilename()
            pathlabel.config(text=browsefunc.filename)


        browsebutton = tk.Button(self, text="Browse for Image file: Buchstaben und Zahlen", command=browsefunc)
        browsebutton.pack()


        pathlabel = tk.Label(self)
        pathlabel.pack()




        def Calculate():
            ###load a colour image

            img=cv2.imread(browsefunc.filename)

            #img = cv2.imread('Buchstaben und Zahlen.jpg')

            height, width = img.shape[:2]# only consider the rows and columns, leaves ouytthe bands if they exist

            ## cut the left image
            start_row, start_col = int(0), int(0)
            # Let's get the ending pixel coordinates (bottom right of cropped top)
            end_row, end_col = int(height), int(750)
            cropped_top = img[start_row:end_row , start_col:end_col]

            ##cut second right image
            start_row2, start_col2 = int(0), int(750)
            # Let's get the ending pixel coordinates (bottom right of cropped top)
            end_row2, end_col2 = int(height), int(1500 )
            cropped_top2 = img[start_row2:end_row2 , start_col2:end_col2]

            ##dispaly left image (cropped_top)  in red
            Conv_hsv_Gray = cv2.cvtColor(cropped_top, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
            cropped_top[mask == 255] = [0, 0, 255]

            ##dispaly cropped_top in cyan i.e green + blue
            Conv_hsv_Gray = cv2.cvtColor(cropped_top2, cv2.COLOR_BGR2GRAY)
            ret, mask1 = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
            cropped_top2[mask1 == 255] = [255, 255, 0]

            ##do orientation
            # Create translation matrix.
            # If the shift is (x, y) then matrix would be
            # M = [1 0 x]
            #     [0 1 y]

            M = np.float32([[1, 0, -49], [0, 1, -3]])
            (rows, cols) = cropped_top.shape[:2]
            # warpAffine does appropriate shifting given the
            # translation matrix.
            res = cv2.warpAffine(cropped_top, M, (cols, rows))

            #blend the images
            weightedSum = cv2.addWeighted(res, 0.5, cropped_top2, 0.5, 0)

            cv2.imshow('Buchstaben und Zahlen Stereo', weightedSum)
            cv2.waitKey(0) & 0xFF # press any key to close window
            cv2.destroyAllWindows()

        button4=tk.Button(self, text='see Stereo Image', command=Calculate)#.grid(row=4,column=2)
        button4_1=tk.Button(self, text='Next', command= lambda:controller.show_frame(Pagethree))
        button4_2=tk.Button(self, text="Back", command= lambda: controller.show_frame(Pageone))

        button4.pack()
        button4_1.pack()
        button4_2.pack()



class Pagethree(tk.Frame):
    def __init__(self,parent,controller):#parent is our class flight planner
        tk.Frame.__init__(self,parent)
        label=tk.Label(self, text='Task 4', font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        def browsefunc():
            browsefunc.filename = tk.filedialog.askopenfilename()
            pathlabel.config(text=browsefunc.filename)


        browsebutton = tk.Button(self, text="Browse for Image file: Pruftafel Zeiss", command=browsefunc)
        browsebutton.pack()


        pathlabel = tk.Label(self)
        pathlabel.pack()


        ##backend
        def Calculate():

            img=cv2.imread(browsefunc.filename)
            #img = cv2.imread('Pruftafel Zeiss.jpg')

            height, width = img.shape[:2]# only consider the rows and columns, leaves ouytthe bands if they exist

            ## cut the left image
            start_row, start_col = int(0), int(0)
            # Let's get the ending pixel coordinates (bottom right of cropped top)
            end_row, end_col = int(height), int(width * .5)
            cropped_top = img[start_row:end_row , start_col:end_col]

            ##cut second right image
            start_row2, start_col2 = int(0), int(width * .5)
            # Let's get the ending pixel coordinates (bottom right of cropped top)
            end_row2, end_col2 = int(height), int(width )
            cropped_top2 = img[start_row2:end_row2 , start_col2:end_col2]

            ##dispaly left image (cropped_top)  in red
            Conv_hsv_Gray = cv2.cvtColor(cropped_top, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
            cropped_top[mask == 255] = [0, 0, 255]

            ##dispaly cropped_top in cyan i.e green + blue
            Conv_hsv_Gray = cv2.cvtColor(cropped_top2, cv2.COLOR_BGR2GRAY)
            ret, mask1 = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
            cropped_top2[mask1 == 255] = [255, 255, 0]



            ##do orientation
            # Create translation matrix.
            # If the shift is (x, y) then matrix would be
            # M = [1 0 x]
            #     [0 1 y]

            M = np.float32([[1, 0, -100.5], [0, 1, -3.75]])
            (rows, cols) = cropped_top.shape[:2]
            # warpAffine does appropriate shifting given the
            # translation matrix.
            res = cv2.warpAffine(cropped_top, M, (cols, rows))

            #blend the images
            weightedSum = cv2.addWeighted(res, 0.5, cropped_top2, 0.5, 0)

            cv2.imshow('Pruftafel Zeiss Stereo', weightedSum)


            cv2.waitKey(0) & 0xFF # press any key to close window
            cv2.destroyAllWindows()



        button5=tk.Button(self, text='see Stereo Image', command=Calculate)#.grid(row=4,column=2)
        button5_1=tk.Button(self, text="Back", command= lambda: controller.show_frame(Pagetwo))

        button5.pack()
        button5_1.pack()



app=Stereo()
app.mainloop()
