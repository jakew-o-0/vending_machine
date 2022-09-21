import tkinter
import sqlite3
from random import randint

class gui():
    def __init__(self, root):
        self.dataBase = sqlite3.connect('./Vending_Machine.db')
        self.currentUsr = None

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
        F = tkinter.Frame(dataWindow, padx=5,pady=5)
        F.grid(column=0,row=0, padx=10,pady=10)

        ########: query items database depending on which button is pressed
        if(btn == 1):
            query = list(self.dataBase.execute("SELECT * FROM items WHERE NAME = '{}';".format(str(self.searchStr.get()))))
        else:
            query = list(self.dataBase.execute("SELECT * FROM items;"))
            if(btn == 3):
                rand = randint(1, len(query))
                query = list(self.dataBase.execute("SELECT * FROM items WHERE ID = {};".format(rand)))

        ########: itterate trough the 2d array given by the sql
        for i in range(0, len(query)):
            for j in range(0, len(query[0])):

                ########: give each record a seperate label in a grid
                l = tkinter.Label(F, text=query[i][j])
                l.grid(column=j, row=i)

            
        f = tkinter.Frame(dataWindow,padx=5,pady=5)
        sVAR = tkinter.StringVar(value=1)
        sVAR1 = tkinter.StringVar()
        b = tkinter.Button(f, text="Add to basket", comman=lambda: self.add_to_basket(item=sVAR1.get(), quantity=sVAR.get(), win=f))
        e = tkinter.Entry(f, textvariable=sVAR1)
        l = tkinter.Label(f, text="Item number or name:")
        l1 = tkinter.Label(f, text="Quantity:")
        s = tkinter.Spinbox(f, from_=1, to=10, wrap=True, textvariable=sVAR, width=18)

        f.grid(column=1, row=0, padx=10,pady=10)
        l.grid(column=0, row=0)
        e.grid(column=1, row=0)
        b.grid(column=0, row=2, columnspan=2)
        l1.grid(column=0, row=1)
        s.grid(column=1, row=1)

    def add_to_basket(self, item, quantity, win):
        if(self.currentUsr == None):
            l = tkinter.Label(win, text="you are not currently logged in, please login")
            l.grid(column=0, row=3, columnspan=2)
        else:
            ########: if the item can be casted then the database will be queried for the name of said item with the id int
            try:
                item = int(item)
                query = list(self.dataBase.execute("SELECT NAME FROM items WHERE ID = {}".format(item)))
                item = query[0][0]
            except(Exception):
                pass
                
            #######: if there is an existing record in the basket it will update the quantity otherwise make a new record
            query = list(self.dataBase.execute("SELECT QUANTITY FROM '{}' WHERE ITEM = '{}';".format(self.currentUsr, item)))
            if(query == []):
                #######: otherwise item will be the name of the item and that will be used insted
                self.dataBase.execute("INSERT INTO '{}' (ITEM, QUANTITY) VALUES('{}', {});".format(self.currentUsr, item, int(quantity)))
            else:
                self.dataBase.execute("UPDATE '{}' SET QUANTITY = '{}' WHERE ITEM = '{}'".format(self.currentUsr, int(query[0][0]) + int(quantity), item))

            self.dataBase.commit()

    def account_window(self):
        acountWindow = tkinter.Toplevel(self.root)
        acountWindow.resizable(False,False)
        acountLab = tkinter.Label(acountWindow)

        ########: desplay appropriate username
        if(self.currentUsr == None):
            acountLab.config(text="Your not currently logged in please login") 
        else:    
            query = list(self.dataBase.execute("SELECT NAME FROM users WHERE ID = {}".format(self.currentUsr)))
            acountLab.config(text="Username: {}".format(query[0][0]))

        acountLab1 = tkinter.Label(acountWindow, text="Recently bought")
        acountBtn = tkinter.Button(acountWindow, text="Change Password", command=self.change_passwd)

        acountLab.pack()
        acountBtn.pack()
        acountLab1.pack()

    def change_passwd(self):
        passWindow = tkinter.Toplevel(self.root)
        passWindow.resizable(False, False)

        #######: gui stuff
        oldPass = tkinter.StringVar()
        newPass = tkinter.StringVar()
        oPassEntry = tkinter.Entry(passWindow, textvariable=oldPass)
        nPassEntry = tkinter.Entry(passWindow, textvariable=newPass)
        passLab = tkinter.Label(passWindow, text="Old password:")
        passLab1 = tkinter.Label(passWindow, text="New password:")
        passBttn = tkinter.Button(passWindow, text="Enter", command=lambda:self.update_passwd(oPass=oldPass.get(), nPass=newPass.get(), win=passWindow))

        passLab.grid(column=0, row=0)
        passLab1.grid(column=0, row=1)
        oPassEntry.grid(column=1, row=0)
        nPassEntry.grid(column=1, row=1)
        passBttn.grid(column=0, row=2, columnspan=2)

    def update_passwd(self, oPass, nPass, win):
        ########: update password and authentication
        out = tkinter.Label(win)
        
        try:
            passAuth = list(self.dataBase.execute("SELECT PASSWORDS FROM users WHERE ID = '{}'".format(self.currentUsr)))
            if(self.currentUsr != None and str(oPass) == str(passAuth[0][0])):
                self.dataBase.execute("UPDATE users SET PASSWORDS = '{}' WHERE ID = '{}'".format(str(nPass), self.currentUsr))
                out.config(text="Updated password!")
            else:
                out.config(text="password was incorrect")
        except(Exception):
            out.config(text="something whent wrong")
        
        self.dataBase.commit()
        out.grid(column=0, row=3, columnspan=2)

    def basket_window(self):
        basketWindow = tkinter.Toplevel(self.root)
        basketWindow.resizable(False,False)
        F = tkinter.Frame(basketWindow)
        F.pack()

        if(self.currentUsr == None):
            l = tkinter.Label(F, text="Your currently not logged in, please login")
            l.pack()
        else:
            basketLab = tkinter.Label(F, text="Item")
            basketLab1 = tkinter.Label(F, text="Quantity")
            basketLab.grid(column=0, row=0)
            basketLab1.grid(column=1, row=0)

            query = list(self.dataBase.execute("SELECT * FROM '{}'".format(self.currentUsr)))

            ########: itterate trough the 2d array given by the sql
            for i in range(0, len(query)):
                for j in range(0, len(query[0])):

                    ########: give each record a seperate label in a grid
                    l = tkinter.Label(F, text=query[i][j])
                    l.grid(column=j, row=i + 1)

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
        out = tkinter.Label(win)
        out.destroy()

        if(self.isNewusr == True):
            ########: adding a newuser into the database
            query = len(list(self.dataBase.execute("SELECT * FROM users")))
            self.dataBase.execute("INSERT INTO users (ID, NAME, PASSWORDS) VALUES({},'{}', '{}');".format(query + 1, usr, passwd))
            self.dataBase.execute("CREATE TABLE '{}'(ITEM TEXT, QUANTITY INT)".format(query + 1)) 
            out = tkinter.Label(win, text="New account created!")
        else:
            ########: logging in with correct username and passwords
            try:
                query = self.dataBase.execute("SELECT * FROM users WHERE NAME = '{}' AND PASSWORDS = '{}';".format(str(usr), str(passwd)))
                q = list(query)
                ########: setting the current user to the id of the user in the data
                self.currentUsr = q[0][0] 
                out = tkinter.Label(win, text="You have been logged in!")
            except(Exception):
                out = tkinter.Label(win, text="Oops username or password was wrong")
            
        out.grid(column=0, row=5, columnspan=2)
        self.dataBase.commit()
    
    def newusr(self):
        self.isNewusr = not(self.isNewusr)
            
    
if(__name__ == "__main__"):
    tk = tkinter.Tk()
    gui = gui(tk)
    tk.mainloop()
