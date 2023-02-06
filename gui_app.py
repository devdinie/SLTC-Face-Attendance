import os
import sys
import cv2

import tkinter as tk

from PIL import Image, ImageTk

bg_clr = "white"
ft_clr = "#191970"

scale_perc = 0.12

class GUI:
  
  def __init__(self, window_name):
    self.window_name = window_name
    
  def gui_init(self):
    
    self.window = tk.Tk()
    self.window.title(self.window_name)
    self.window.configure(bg=bg_clr)
    
    width = self.window.winfo_screenwidth()
    height= self.window.winfo_screenheight()
    self.window.geometry("%dx%d" % (width, height))
    
    #region title section
    logo_org = Image.open("images_logos/SLTC_LOGO_2022.png")
    
    logo_img = ImageTk.PhotoImage(logo_org.resize((int(logo_org.width*scale_perc),int(logo_org.height*scale_perc))))
    
    frame1a  = tk.Frame(self.window).pack()
    frame1b = tk.Frame(self.window).pack(anchor="center")
    frame1c = tk.Frame(self.window).pack(anchor="center")
    
    img = tk.Label(frame1a, image=logo_img, bg=bg_clr)
    img.image = logo_img
    img.place(x=int((width/2)-(logo_org.width*scale_perc)/2), y=20)
    
    label1b = tk.Label(frame1b, text= "FACE ATTENDANCE SYSTEM", bg=bg_clr, fg=ft_clr, font=('PT Pro',22, 'bold')).place(relx=0.4,y=logo_img.height()+30)
    label1c = tk.Label(frame1c, text= "SRI LANKA TECHNOLOGICAL CAMPUS (SLTC)", bg=bg_clr, fg=ft_clr, font=('PT Pro',18)).place(relx=0.37,y=logo_img.height()+70)
    #endregion title section
    
  def gui_run(self):
    
    GUI.gui_init(self)
    self.window.mainloop()
 
#gui = GUI("Face Attendance")   
#gui.gui_run()
  