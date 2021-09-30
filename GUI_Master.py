from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class RootGUI:
    def __init__(self):
        self.root=Tk() 
        self.root.title("TizenRT Debug Analyzer Tool")
        self.root.geometry("360x120")
        self.root.config(bg="white")

class ComGui():
    def __init__(self,root,serial):
        self.root=root
        self.serial = serial
        
        self.frame=LabelFrame(root,text = "Com Manager",padx=5 , pady=5 , bg="white")
        
        self.lable_com=Label(self.frame,text="Available Port(s): ",bg="white",width=15,anchor="w")
        
        self.lable_bd =Label(self.frame,text="Baud Rate: ",bg="white",width=15,anchor="w")
        
        
        self.ComOptionMenu() 
        self.BaudOptionMenu()
        
        self.btn_refresh = Button(self.frame , text = "Refresh",width=10,command=self.com_refresh)
        
        self.btn_connect = Button(self.frame , text = "Connect",width = 10 , state="disabled",command=self.serial_connect)
        
        self.padx=20
        self.pady=5
        self.publish()
        
    def publish(self):
        self.frame.grid(row=0,column=0,rowspan=3,columnspan=3,padx=5,pady=5)   
        self.lable_com.grid(column=1,row=2)
        self.drop_com.grid(column=2,row=2,padx=self.padx,pady=self.pady)
        self.lable_bd.grid(column=1,row=3)
        self.drop_baud.grid(column=2,row=3,padx=self.padx,pady=self.pady)
        self.btn_refresh.grid(column=3,row=2)
        self.btn_connect.grid(column=3,row=3)
        
        
    def  ComOptionMenu(self):
        #Generate list of all available coms
        self.serial.getCOMList() 
        self.clicked_com= StringVar() 
        self.clicked_com.set(self.serial.com_list[0])
        self.drop_com = OptionMenu(
            self.frame,self.clicked_com , self.serial.com_list,command=self.connect_ctrl)
        self.drop_com.config(width=10)
        
     
    def BaudOptionMenu(self):
        self.clicked_bd=StringVar()
        bds=["-","300","600","1200","2400","4800","9600","14400","19200",
             "28800","38400","56000","57600","115200","128000","256000"]
        self.clicked_bd.set(bds[0])
        self.drop_baud=OptionMenu(self.frame,self.clicked_bd,*bds,command=self.connect_ctrl)
        self.drop_baud.config(width=10)
            
        
        
    def connect_ctrl(self,other):
        '''method to control state of connect button'''
        if "-" in self.clicked_com.get() or "-" in self.clicked_bd.get():
            self.btn_connect["state"] = "disable"
        else:
            self.btn_connect["state"] = "active"
             
             
    def com_refresh(self):
        self.drop_com.destroy()
        self.ComOptionMenu()
        self.drop_com.grid(column=2,row=2,padx=self.padx,pady=self.pady)
        logic=[]
        self.connect_ctrl(logic)  
    
    def serial_connect(self):
        if self.btn_connect["text"] in "Connect":
            #start the connection
            self.serial.SerialOpen(self)
            if self.serial.ser.status:
                self.btn_connect["text"]="Disconnect"
                self.btn_refresh["state"]="disable"
                self.drop_baud["state"]="disable"
                self.drop_com["state"]="disable" 
                InfoMsg = f"Successful   UART connection using {self.clicked_com.get()}"
                messagebox.showerror("showerror",InfoMsg) 
            else:
                ErrorMsg = f"Failure to establish UART connection using {self.clicked_com.get()}"
                messagebox.showerror("showerror",ErrorMsg) 
        else:
            #start closing the connection
             # Closing the Serial COM
            # Close the serial communication
            self.serial.SerialClose(self)

            # Closing the Conn Manager
            # Destroy the channel manager
            self.conn.ConnGUIClose(self)

            InfoMsg = f"UART connection using {self.clicked_com.get()} is now closed"
            messagebox.showwarning("showinfo", InfoMsg)
            self.btn_connect["text"] = "Connect"
            self.btn_refresh["state"] = "active"
            self.drop_baud["state"] = "active"
            self.drop_com["state"] = "active"
            

class ConnGUI():
    def __init__(self, root, serial):
        '''
        Initialize main Widgets for communication GUI
        '''
        self.root = root
        self.serial = serial

        # Build ConnGui Static Elements
        self.frame = LabelFrame(root, text="Connection Manager",
                                padx=5, pady=5, bg="white", width=60)
        self.sync_label = Label(
            self.frame, text="Sync Status: ", bg="white", width=15, anchor="w")
        self.sync_status = Label(
            self.frame, text="..Sync..", bg="white", fg="orange", width=5)

        self.ch_label = Label(
            self.frame, text="Active channels: ", bg="white", width=15, anchor="w")
        self.ch_status = Label(
            self.frame, text="...", bg="white", fg="orange", width=5)

        self.btn_start_stream = Button(self.frame, text="Start", state="disabled",
                                       width=5, command=self.start_stream)

        self.btn_stop_stream = Button(self.frame, text="Stop", state="disabled",
                                      width=5, command=self.stop_stream)

        self.btn_add_chart = Button(self.frame, text="+", state="disabled",
                                    width=5, bg="white", fg="#098577",
                                    command=self.new_chart)

        self.btn_kill_chart = Button(self.frame, text="-", state="disabled",
                                     width=5, bg="white", fg="#CC252C",
                                     command=self.kill_chart)
        self.save = False
        self.SaveVar = IntVar()
        self.save_check = Checkbutton(self.frame, text="Save data", variable=self.SaveVar,
                                      onvalue=1, offvalue=0, bg="white", state="disabled",
                                      command=self.save_data)

        self.separator = ttk.Separator(self.frame, orient='vertical')

        # Optional Graphic parameters
        self.padx = 20
        self.pady = 15

        # Extending the GUI
        self.ConnGUIOpen()

    def ConnGUIOpen(self):
        '''
        Method to display all the widgets 
        '''
        self.root.geometry("800x120")
        self.frame.grid(row=0, column=4, rowspan=3,
                        columnspan=5, padx=5, pady=5)

        self.sync_label.grid(column=1, row=1)
        self.sync_status.grid(column=2, row=1)

        self.ch_label.grid(column=1, row=2)
        self.ch_status.grid(column=2, row=2, pady=self.pady)

        self.btn_start_stream.grid(column=3, row=1, padx=self.padx)
        self.btn_stop_stream.grid(column=3, row=2, padx=self.padx)

        self.btn_add_chart.grid(column=4, row=1, padx=self.padx)
        self.btn_kill_chart.grid(column=5, row=1, padx=self.padx)

        self.save_check.grid(column=4, row=2, columnspan=2)
        self.separator.place(relx=0.58, rely=0, relwidth=0.001, relheight=1)

    def ConnGUIClose(self):
        '''
        Method to close the connection GUI and destorys the widgets
        '''
        # Must destroy all the element so they are not kept in Memory
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.root.geometry("360x120")

    def start_stream(self):
        pass

    def stop_stream(self):
        pass

    def new_chart(self):
        pass

    def kill_chart(self):
        pass

    def save_data(self):
        pass
             
            
if __name__ =="__main__":   
    RootGUI()  
    ComGui()    
    ConnGUI()
