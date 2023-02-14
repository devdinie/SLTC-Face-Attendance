import cv2
import time
import datetime
import calendar

import tkinter  as tk
import tkmacosx as tkmac



from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from face_recognition_main import facerec_main

window_name = "Face Attendance"
video_width, video_height = 720, 420

ft_clr  = ["#191970","White"]
bg_clr  = ["white"  ,"Gray", "#80cbed","#4db6e6","grey22"]
days_arr= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class MainWindow():
  
  def __init__(self, window, window_name, cap):
    
    #region title and init
    
    self.cap = cap
    self.window = window
    self.window.title(window_name)
    self.window.configure(bg=bg_clr[0])
    
    self.window_width = self.window.winfo_screenwidth()
    self.window_height= self.window.winfo_screenheight()
    
    self.video_width  = video_width
    self.video_height = video_height
    self.window.geometry("%dx%d" % (self.window_width, self.window_height))
    
    self.interval = 20 
    self.no_clicks= 0
    
    logo_org = Image.open("images_logos/SLTC_LOGO_2022.png")
    logo_img = ImageTk.PhotoImage(logo_org.resize((int(logo_org.width*0.12),int(logo_org.height*0.12))))
    
    self.frame1a = tk.Frame(self.window).pack(anchor="center")
    self.frame1b = tk.Frame(self.window).pack(anchor="center")
    self.frame1c = tk.Frame(self.window).pack(anchor="center")
    
    img = tk.Label(self.frame1a, image=logo_img, bg=bg_clr[0])
    img.image = logo_img
    img.place(relx=0.5, y=int(logo_org.height*0.12)-25,anchor=tk.CENTER)
    
    self.label1b = tk.Label(self.frame1b, text= "FACE ATTENDANCE SYSTEM", bg=bg_clr[0], fg=ft_clr[0], font=('PT Pro',20, 'bold')).place(relx=0.4,y=int(logo_org.height*0.12)-25+45)
    self.label1c = tk.Label(self.frame1c, text= "SRI LANKA TECHNOLOGICAL CAMPUS (SLTC)", bg=bg_clr[0], fg=ft_clr[0], font=('PT Pro',18)).place(relx=0.37,y=int(logo_org.height*0.12)-25+80)
    
    #endregion title and init
    
    #region video frame display
    
    self.bg_canvas = tk.Canvas(self.window, width=self.video_width+6, height=self.video_height+6, background=bg_clr[4], bd=0, highlightthickness=0)
    self.bg_canvas.place(relx=0.5, rely=0.5,anchor=tk.CENTER)
    
    self.canvas = tk.Canvas(self.window, width=self.video_width, height=self.video_height, bd=0, highlightthickness=0, bg=bg_clr[1], background=bg_clr[1])
    self.canvas.place(relx=0.5, rely=0.5,anchor=tk.CENTER)
    
    self.label_initvideo = tk.Label(self.canvas, text= "Press start to load camera.",bg=bg_clr[1], fg=ft_clr[1], font=('PT Pro',15))
    self.label_initvideo.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    #endregion video frame display
    
    #region buttons
    
    left_x = self.window_width/2 - self.video_width/2 - 6
    btns_y = self.video_height+(self.window_height/2 - self.video_height/2) -60

    self.btn_start = tkmac.Button(text = 'Start', fg=ft_clr[1], bg=bg_clr[1], focuscolor=bg_clr[1], font=('PT Pro',15), 
                                  activebackground=bg_clr[1], borderless=1, command=lambda:self.toggled()) #command=lambda:self.update_image()
    self.btn_start.place(x=left_x, y=btns_y, width = 100, height = 35)
    
    #endregion buttons
    
    #region clock display
    
    self.clk_canvas = tk.Canvas(self.window, width=310, height=90, bd=0, highlightthickness=2, highlightbackground=bg_clr[1], background=bg_clr[4])
    self.clk_canvas.place(x = self.window_width-left_x/2, y = (self.window_height/2 - self.video_height/2)-23, anchor=tk.CENTER)
    
    self.clk_label = tk.Label(self.clk_canvas, text="", font=("ds-digital", 80), bg =bg_clr[4], fg="limegreen")
    self.clk_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def digitalclock():
      time_display = time.strftime("%H:%M:%S")
      self.clk_label.config(text=time_display,font=("ds-digital", 80))
      self.clk_label.after(200, digitalclock)
    digitalclock()

    #endregion clock display
    
    #region date display
    
    self.dte_canvas = tk.Canvas(self.window, width=310, height=50, bd=0, highlightthickness=2, highlightbackground=bg_clr[1], background=bg_clr[4])
    self.dte_canvas.place(x = self.window_width-left_x/2, y = (self.window_height/2 - self.video_height/2)+70, anchor=tk.CENTER)
    
    dte_dflt_arr= str(datetime.datetime.today()).split(' ')[0].split('-')
    dte_dflt_arr= [int(i) for i in dte_dflt_arr]
    
    dte_display =  days_arr[datetime.datetime.today().weekday()]+", "+calendar.month_name[dte_dflt_arr[1]] + " " + str(dte_dflt_arr[2])+", "+ str(dte_dflt_arr[0]) 
    self.dte_label = tk.Label(self.dte_canvas, text=dte_display, font=("ds-digital", 27), bg =bg_clr[4], fg="limegreen")
    self.dte_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    #endregion date display
    
    
    """
    #region mode selection
    
    self.mode_canvas = tk.Canvas(self.window, width=310, height=90, bd=0, highlightthickness=2, highlightbackground=bg_clr[1], background=bg_clr[4])
    self.mode_canvas.place(x = left_x/2, y = (self.window_height/2 - self.video_height/2)-23, anchor=tk.CENTER)
    
    RadioVar = IntVar()
    f = tkFont.Font(family='Helvetica',size=36, weight='bold')
    self.Radbtn1 = Radiobutton(self.mode_canvas, text="Option 1", variable=RadioVar, value=1)
    self.Radbtn1.place( relx=0.5, rely=0.25, anchor = tk.CENTER ) #command=sel
    
    self.Radbtn2 = Radiobutton(self.mode_canvas, text="Option 2", variable=RadioVar, value=2)
    self.Radbtn2.place( relx=0.5, rely=0.75, anchor = tk.CENTER )
    #endregion mode selection
    """
  def toggled(self):
    
    self.no_clicks = self.no_clicks+1
    
    if self.no_clicks == 1: 
      self.update_image()
      self.btn_start.configure(text="Stop")
    
    else:
      
      self.window.after_cancel(self.after_id)
      
      self.no_clicks = 0
      self.btn_start.configure(text="Start")
      
      self.canvas = tk.Canvas(self.window, width=self.video_width, height=self.video_height, bd=0, highlightthickness=0, bg=bg_clr[1], background=bg_clr[1])
      self.canvas.place(relx=0.5, rely=0.5,anchor=tk.CENTER)
    
      self.label_initvideo = tk.Label(self.canvas, text= "Press start to load camera.",bg=bg_clr[1], fg=ft_clr[1], font=('PT Pro',15))
      self.label_initvideo.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    
  def update_image(self):
    
    self.label_initvideo.destroy()
    
    self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB)
    self.image = cv2.resize(self.image, (self.video_width,self.video_height))
    
    self.image = facerec_main(self.image)
    self.image = Image.fromarray(self.image) # to PIL format
    self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
    
    self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
    
    self.after_id = self.window.after(self.interval, self.update_image)
    
        
if __name__ == "__main__":
  
    window = tk.Tk()
    MainWindow(window, window_name, cv2.VideoCapture(0))
    window.mainloop()