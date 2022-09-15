import tkinter
import sqlite3
from random import randint

class gui():
    def __init__(self, root):
        self.dataBase = sqlite3.connect('Vending_Machine.db')
        self.currentUsr = ""

        self.root = root
        self.root.resizable(False,  False)
        self.main()

    def main(self):
        ########: bulds menu bar with cascades
        menuBar = tkinter.Menu(self.root)

        profile = tkinter.Menu(menuBar, tearoff=0)
        profile.add_command(label="Account", command=self.account_window)
        profile.add_command(label="Basket", command=self.basket_window)
        profile.add_separator()
        profile.add_command(label="Login", command=self.logon_window)
        profile.add_command(label="Quit", command=self.root.quit)

        menuBar.add_cascade(label="Profile", menu=profile)
        self.root.config(menu=menuBar)
    

        ########: frames with widgets specific searching of the database
        frame = tkinter.Frame(self.root, padx=5,pady=5)
        frame.pack(padx=10,pady=10)

        searchLib = tkinter.Label(frame, text="If you know what you want...",font=("TkDefaultFont", 8))
        searchLib1 = tkinter.Label(frame, text="Search!", font=("TkDefaultFont", 20))
        self.searchStr = tkinter.StringVar()
        searchEntry = tkinter.Entry(frame, width=15, textvariable=self.searchStr)
        searchButton = tkinter.Button(frame, text="Enter", command=lambda: self.search_window(btn=1))

        searchLib.grid(column=0, row=0, columnspan=2, sticky='w')
        searchLib1.grid(column=0, columnspan=2, row=1)
        searchEntry.grid(column=0, row=2, padx=2)
        searchButton.grid(column=1, row=2)


        ########: second frame with widgets random and all searching of the data base
        frame2 = tkinter.Frame(self.root, padx=5, pady=5)
        frame2.pack(padx=10, pady=10)

        searchLib2 = tkinter.Label(frame2, text="Not sure what to get?", font=("TkDefaultFont", 8))
        searchLib3 = tkinter.Label(frame2, text="Try these!", font=("TkDefaultFont", 20))
        searchAllBtn = tkinter.Button(frame2, text="Browse all", command=lambda: self.search_window(btn=2))
        searchRandBtn = tkinter.Button(frame2, text="Random", command=lambda: self.search_window(btn=3))

        searchLib2.grid(column=0, row=0, columnspan=2, sticky='w')
        searchLib3.grid(column=0, row=1, columnspan=2)
        searchAllBtn.grid(column=0, row=2)
        searchRandBtn.grid(column=1, row=2) 

    def search_window(self, btn):
        dataWindow = tkinter.Toplevel(self.root)
        dataWindow.resizable(False, False)

        if(btn == 1):
            query = list(self.dataBase.execute("SELECT * FROM items WHERE NAME = '{}'".format(str(self.searchStr.get()))))
        else:
            query = list(self.dataBase.execute("SELECT * FROM items;"))
            if(btn == 3):
                rand = randint(1, len(query))
                query = list(self.dataBase.execute("SELECT * FROM items WHERE ID = {}".format(rand)))

        ########: itterate trough the 2d array given by the sql
        for i in range(0, len(query)):
            for j in range(0, len(query[0])):

                ########: give each record a seperate label in a grid
                l = tkinter.Label(dataWindow, text=query[i][j])
                l.grid(column=j, row=i)


    def account_window(self):
        acountWindow = tkinter.Toplevel()
        acountWindow.resizable(False,False)
        
        acountLab = tkinter.Label(acountWindow, text="Username")
        acountLab1 = tkinter.Label(acountWindow, text="Recently bought")
        acountBtn = tkinter.Button(acountWindow, text="Change Password")

        acountLab.pack()
        acountBtn.pack()
        acountLab1.pack()
    
    def basket_window(self):
        basketWindow = tkinter.Toplevel(self.root)
        basketWindow.resizable(False,False)
    
    def logon_window(self):
        logonWindow = tkinter.Toplevel(self.root)
        logonWindow.resizable(False, False)

        self.isNewusr = False
        logonLab = tkinter.Label(logonWindow, text="Login", font=("TkDefaultFont", 15))
        logonLab1 = tkinter.Label(logonWindow, text="Username")
        logonLab2 = tkinter.Label(logonWindow, text="Password")
        logonStr = tkinter.StringVar()
        logonStr1 = tkinter.StringVar()
        logonEntry = tkinter.Entry(logonWindow, textvariable=logonStr)
        logonEntry1 = tkinter.Entry(logonWindow, show='*', textvariable=logonStr1)
        logonBtn = tkinter.Button(logonWindow, text="Enter", command=lambda: self.login(usr=logonStr.get(),passwd=logonStr1.get(), win=logonWindow))
        logonNewUsr = tkinter.Checkbutton(logonWindow, text="create a newuser", variable=self.isNewusr, onvalue=True, offvalue=False, command=self.newusr)

        logonLab.grid(column=0, row=0, columnspan=2)    
        logonLab1.grid(column=0, row=1)
        logonLab2.grid(column=0, row=2)
        logonEntry.grid(column=1, row=1)
        logonEntry1.grid(column=1, row=2)
        logonBtn.grid(column=0, row=4, columnspan=2)
        logonNewUsr.grid(column=0, row=3)

    def login(self, usr, passwd, win):
        try:
            out.destroy()
        except(Exception):
            pass
        out = tkinter.Label(win)
        print(self.isNewusr)

        if(self.isNewusr == True):
            query = len(list(self.dataBase.execute("SELECT * FROM users;")))
            query = self.dataBase.execute("INSERT INTO users (ID, NAME, PASSWORDS) VALUES({},'{}', '{}');".format(query + 1, usr, passwd))
        else:
            try:
                query = self.dataBase.execute("SELECT NAME, PASSWORDS  FROM users WHERE NAME = '{}' AND PASSWORDS = '{}';".format(str(usr), str(passwd)))
                q = list(query)
                self.currentUsr = q[0][0] 
                out.config(text="you have been logged in!")
            except(Exception):
                out.config(text="Oops username or password is incorrect")
            out.grid(column=0, row=5, columnspan=2)
    
    def newusr(self):
        self.isNewusr = not(self.isNewusr)
            
    
if(__name__ == "__main__"):
    tk = tkinter.Tk()
    gui = gui(tk)
    tk.mainloop()
