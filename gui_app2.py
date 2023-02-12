import cv2
import tkinter  as tk
import tkmacosx as tkmac

from PIL import Image, ImageTk

window_name = "Face Attendance"
video_width, video_height = 720, 420

bg_clr = ["white"  ,"Gray", "#80cbed","#4db6e6","grey22"]
ft_clr = ["#191970","White"]

"""
gui = GUI("Face Attendance")   
gui.gui_run()
"""
"""
class MainWindow():
  
  def __init__(self, window, window_name, cap):
    
    self.window = window
    self.window.title(window_name)
    
    self.window_width  = self.window.winfo_screenwidth()
    self.window_height = self.window.winfo_screenheight()
    self.window.geometry("%dx%d" % (self.window_width, self.window_height))
    
    self.cap = cap
    print(cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH ,frame_width)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT,frame_height)
    
    self.interval = 20 
    
    self.frame2b = tk.Frame(self.window, height=1000,width=700,bg=bg_clr[1])
    self.frame2b.pack()
    #self.label2b = tk.Label(self.frame2b, text= "Press start to load camera.",bg=bg_clr[1], fg=ft_clr[1], font=('PT Pro',15))
    
    self.canvas = tk.Canvas(self.frame2b,height=1000,width=700)
    self.canvas.grid(row=0, column=0)
    self.update_image()
        
  def update_image(self):

    self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
    self.image = Image.fromarray(self.image) # to PIL format
    self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
    
    self.canvas.create_image(0, 0, anchor=tk.CENTER, image=self.image)
    self.window.after(self.interval, self.update_image)
        
if __name__ == "__main__":
  
  window = tk.Tk()
  MainWindow(window, window_name, cv2.VideoCapture(0))
  window.mainloop()
""" 

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
    #self.update_image()

    #endregion video frame display
    
    #region buttons
    
    left_x = self.window_width/2 - self.video_width/2 - 6
    btns_y = self.video_height+(self.window_height/2 - self.video_height/2) -60

    self.btn_start = tkmac.Button(text = 'Start', fg=ft_clr[1], bg=bg_clr[1], focuscolor=bg_clr[1], font=('PT Pro',15), 
                                  activebackground=bg_clr[1], borderless=1, command=lambda:self.update_image())
    self.btn_start.place(x=left_x, y=btns_y, width = 100, height = 35)
    
    self.btn_stop = tkmac.Button(text = 'Stop', fg=ft_clr[1], bg=bg_clr[1], focuscolor=bg_clr[1], font=('PT Pro',15), 
                                  activebackground=bg_clr[1], borderless=1)
    self.btn_stop.place(x=left_x+110, y=btns_y, width = 100, height = 35)
    #endregion buttons
    
    
  def update_image(self):
    
    self.label_initvideo.destroy()
    
    self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB)
    self.image = cv2.resize(self.image, (self.video_width,self.video_height))
    self.image = Image.fromarray(self.image) # to PIL format
    self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
    
    self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
    
    self.window.after(self.interval, self.update_image)
        
if __name__ == "__main__":
  
    window = tk.Tk()
    MainWindow(window, window_name, cv2.VideoCapture(0))
    window.mainloop()