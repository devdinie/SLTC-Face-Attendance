import os
import sys
import cv2

import tkinter  as tk
import tkmacosx as tkmac

from PIL import Image, ImageTk

bg_clr = ["white"  ,"Gray", "#80cbed","#4db6e6"]
ft_clr = ["#191970","White"]

scale_perc = 0.12
frame_width, frame_height = 720, 420

class GUI:
  
  def __init__(self, window_name):
    self.window_name = window_name
    
  def open_camera(self):
    _, frame = self.video.read()
    opencv_image   = frame#cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    captured_image = Image.fromarray(opencv_image)
    photo_image = ImageTk.PhotoImage(image=captured_image)
    #self.label2b.configure(image=photo_image)
    self.label2b.photo_image = photo_image
    self.label2b.configure(image=photo_image)
    #self.label2b.place()
    #label.image=photo_image
  
    print("in here")
    #label_widget.configure(image=photo_image)
    self.label2b.after(10, GUI.open_camera(self))
    
  def gui_init(self, vid):
    self.video  = vid
    self.window = tk.Tk()
    self.window.title(self.window_name)
    self.window.configure(bg=bg_clr[0])
    
    self.width = self.window.winfo_screenwidth()
    self.height= self.window.winfo_screenheight()
    self.window.geometry("%dx%d" % (self.width, self.height))

    #region title section
    logo_org = Image.open("images_logos/SLTC_LOGO_2022.png")
    logo_img = ImageTk.PhotoImage(logo_org.resize((int(logo_org.width*scale_perc),int(logo_org.height*scale_perc))))
    
    self.frame1a = tk.Frame(self.window).pack(anchor="center")
    self.frame1b = tk.Frame(self.window).pack(anchor="center")
    self.frame1c = tk.Frame(self.window).pack(anchor="center")
    
    img = tk.Label(self.frame1a, image=logo_img, bg=bg_clr[0])
    img.image = logo_img
    img.place(x=int((self.width/2)-(logo_org.width*scale_perc)/2), y=20)
    
    self.label1b = tk.Label(self.frame1b, text= "FACE ATTENDANCE SYSTEM", bg=bg_clr[0], fg=ft_clr[0], font=('PT Pro',22, 'bold')).place(relx=0.4,y=logo_img.height()+30)
    self.label1c = tk.Label(self.frame1c, text= "SRI LANKA TECHNOLOGICAL CAMPUS (SLTC)", bg=bg_clr[0], fg=ft_clr[0], font=('PT Pro',18)).place(relx=0.37,y=logo_img.height()+70)
    #endregion title section
    
    #region camera-view sections
    self.frame2a = tk.Frame(self.window,height=frame_height+10,width=frame_width+10,bg=bg_clr[2]).place(relx=0.254,y=logo_img.height()+120)
    self.frame2b = tk.Frame(self.window,height=frame_height,width=frame_width,bg=bg_clr[1]).place(relx=0.2575,y=logo_img.height()+125)
    self.label2b = tk.Label(self.frame2b, text= "Press start to load camera.",bg=bg_clr[1], fg=ft_clr[1], font=('PT Pro',15))
    self.label2b.place(relx=0.44,rely=0.48)
    #endregion camera-view sections
    
    #region buttons
    self.btn_start = tkmac.Button(text = 'Start', fg=ft_clr[1], bg=bg_clr[3], focuscolor=bg_clr[3], 
                      font=('PT Pro',16), activebackground=bg_clr[3], borderless=1, 
                      command=lambda:GUI.open_camera(self)).place( relx=0.253,y=logo_img.height()+560,  width = 100, height = 35)
    #endregion buttons
    
     
  def gui_run(self):
    
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH ,frame_width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT,frame_height)

    GUI.gui_init(self, vid)
    self.window.mainloop()
    
    
 
#gui = GUI("Face Attendance")   
#gui.gui_run()
  