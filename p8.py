from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
from tkinter.ttk import Combobox
from tkintertable import TableCanvas,TableModel
import random
import time
import project_tables
import sqlite3
import gmail
from PIL import Image,ImageTk
import os
import shutil

win=Tk()
win.state('zoomed')
win.resizable(width=False,height=False)
win.configure(bg='pink')

img1=Image.open('logo1.jpg').resize((1300,180))
bitmap_image=ImageTk.PhotoImage(img1,master=win)

lbl_img=Label(win,image=bitmap_image)
lbl_img.place(relx=0,rely=0)

title=Label(win,text='Banking Automation',font=('arial',40,'bold','underline'),bg='pink',fg='blue')
title.pack()

date=time.strftime('%d-%B-%Y')
currdate=Label(win,text=date,font=('arial',20,'bold'),bg='pink')
currdate.pack(pady=10)


footer=Label(win,text='By:Rahul Sharma @ 8006843970\nducat noida sec-16\nProject Guide:Mr aditya',font=('arial',15,'bold','underline'),bg='pink',fg='blue')
footer.pack(side='bottom')

def main_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.73)

    global code_cap
    code_cap=''
    for i in range(3):
        i=random.randint(65,90)
        c=chr(i)
        j=random.randint(0,9)
        code_cap=code_cap+str(j)+c

    global lbl_captcha
    lbl_captcha=Label(frm,text=f'Captcha\t{code_cap}',font=('arial',20,'bold'),bg='powder blue',fg='green')
    lbl_captcha.place(relx=.35,rely=.5)

    def forgot_pass():
        frm.destroy()
        forgotpass_screen()

    def login():
        acn_type=cb_type.get()
        acno=e_acn.get()
        pwd=e_pass.get()
        user_cap=e_captcha.get()

        if acno=="" or pwd=="" or user_cap=="":
            messagebox.showerror('login','Empty fiedls are not allowed')
            return
        if acn_type=='admin' and acno=='0' and pwd=='admin':
            if user_cap==code_cap:
                frm.destroy()
                welcome_admin_screen()
            else:
                 messagebox.showerror('login','invalid captcha')

        elif acn_type=='user':
            if user_cap==code_cap:
                conobj=sqlite3.connect('bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select * from users where users_acno=? and users_pass=?',(acno,pwd) )
                tup=curobj.fetchone()
                if tup==None:
                    messagebox.showerror('login','invalid acn/pass')
                    return
                else:
                    global welcome_user,user_acno
                    welcome_user=tup[1]
                    user_acno=tup[0]
                    frm.destroy()
                    welcome_user_screen()
            else:
                messagebox.showerror('login','invalid captcha')

        else:
            messagebox.showerror('login','invalid acn or password')

    lbl_type=Label(frm,text='ACN Type',font=('arial',20,'bold'),bg='powder blue')
    lbl_type.place(relx=.2,rely=.1)

    cb_type=Combobox(frm,values=['----select acn type----','user','admin'],font=('arial',20,'bold'))
    cb_type.current(0)
    cb_type.place(relx=.35,rely=.1)

    lbl_acn=Label(frm,text='ACNo.',font=('arial',20,'bold'),bg='powder blue')
    lbl_acn.place(relx=.2,rely=.25)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.35,rely=.25)
    e_acn.focus()

    lbl_pass=Label(frm,text='password',font=('arial',20,'bold'),bg='powder blue')
    lbl_pass.place(relx=.2,rely=.39)


    def refresh():
        global code_cap
        global lbl_captcha

        code_cap=''
        for i in range(3):
            i=random.randint(65,90)
            c=chr(i)
            j=random.randint(0,9)
            code_cap=code_cap+str(j)+c
        lbl_captcha=Label(frm,text=f'Captcha\t{code_cap}',font=('arial',20,'bold'),bg='powder blue',fg='green')
        lbl_captcha.place(relx=.35,rely=.5)


    

    btn_refresh=Button(frm,text='refresh',font=('arial',10,),bd=5,bg='green',command=refresh)
    btn_refresh.place(relx=.55,rely=.5)

    lbl_captcha2=Label(frm,text=f'Enter Captcha',font=('arial',20,'bold'),bg='powder blue')
    lbl_captcha2.place(relx=.2,rely=.6)

    e_captcha=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_captcha.place(relx=.35,rely=.6)

    e_pass=Entry(frm,font=('arial',20,'bold'),show='*',bd=5)
    e_pass.place(relx=.35,rely=.38)

    btn_login=Button(frm,text='submit',font=('arial',20,'bold'),bg='blue',command=login)
    btn_login.place(relx=.38,rely=.7)

    btn_reset=Button(frm,text='reset',font=('arial',20,'bold'),bg='red',command=refresh)
    btn_reset.place(relx=.5,rely=.7)

    btn_forgot=Button(frm,text='forgot password',font=('arial',20,'bold'),bd=5,bg='red',command=forgot_pass)
    btn_forgot.place(relx=.38,rely=.82,relwidth=.2)

def forgotpass_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.73)

    frm_title=Label(frm,text=' Password Recovery Screen',font=('arial',30,'bold'),bg='powder blue',fg='green')
    frm_title.pack()
    
    def back():
        frm.destroy()
        main_screen()

    def reset():
        e_acn.delete(0,"end")
        e_mob.delete(0,"end")
        e_email.delete(0,"end")
        e_acn.focus()

    def forgotpass_db():
        uacno=e_acn.get()
        umob=e_mob.get()
        uemail=e_email.get()

        conobj=sqlite3.connect('bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select users_name,users_pass from users where users_acno=? and users_email=? and users_mob=?',(uacno,uemail,umob) )
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror('forgot Pass','Invalid Details')
            return
        else:
            global upass,uname
            uname=tup[0]
            upass=tup[1]
            otp=random.randint(1000,9999)

            try:
                con=gmail.GMail('rahulvatskirthal@gmail.com','ovct rcyq sadi dvcg')
                utext=f'''hello,{uname},
            OTP to recover password is {otp}
            Your password is {upass}

            Thanks
            HDFC BANK corp
            '''

                msg=gmail.Message(to=uemail,subject='OTP for password recovery',text=utext)
                con.send(msg)
                messagebox.showinfo('New User',f'Mail send successfully')
                lbl_otp=Label(frm,text='OTP',font=('arial',15,'bold'),bg='powder blue')
                lbl_otp.place(relx=.25,rely=.8)

                e_otp=Entry(frm,font=('arial',15,'bold'),bd=5)
                e_otp.place(relx=.35,rely=.8)

                def verify_otp():
                    if otp==int(e_otp.get()):
                        messagebox.showinfo('Forgot pass',f'Your pass is :\t{upass}')
                    else:
                        messagebox.showerror('Forgot Pass',f'Invalid OTP')
                    
                btn_submit=Button(frm,text='submit',font=('arial',15,'bold'),bd=5,bg='green',command=verify_otp)
                btn_submit.place(relx=.55,rely=.8)

            except:
                messagebox.showerror('Network Problem','something went wrong with network')


    btn_back=Button(frm,text='back',font=('arial',20,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='ACNo.',font=('arial',20,'bold'),bg='powder blue')
    lbl_acn.place(relx=.25,rely=.2)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.35,rely=.2)
    e_acn.focus()

    lbl_mob=Label(frm,text='Mob',font=('arial',20,'bold'),bg='powder blue')
    lbl_mob.place(relx=.25,rely=.36)

    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=.35,rely=.35)

    lbl_email=Label(frm,text='Email',font=('arial',20,'bold'),bg='powder blue')
    lbl_email.place(relx=.25,rely=.51)

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.35,rely=.5)

    btn_submit=Button(frm,text='submit',font=('arial',20,'bold'),bd=5,bg='green',command=forgotpass_db)
    btn_submit.place(relx=.36,rely=.6,relwidth=.1)

    btn_reset=Button(frm,text='reset',font=('arial',20,'bold'),bd=5,bg='red',command=reset)
    btn_reset.place(relx=.48,rely=.6,relwidth=.1)

def welcome_admin_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.73)

    frm_title=Label(frm,text=' Admin Home Screen',font=('arial',30,'bold'),bg='powder blue',fg='green')
    frm_title.pack()
    
    def logout():
        frm.destroy()
        main_screen()

    def newuser():
        frm.destroy()
        newuser_screen()

    def deleteuser():
        frm.destroy()
        deleteuser_screen()

    def viewuser():
        frm.destroy()
        viewuser_screen()

    btn_logout=Button(frm,text='logout',font=('arial',20,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.91,rely=0)

    btn_newuser=Button(frm,text='open user acn',font=('arial',20,'bold'),bd=5,bg='green',fg='yellow',command=newuser)
    btn_newuser.place(relx=0,rely=.12,relwidth=.2)

    btn_deleteuser=Button(frm,text='delete user acn',font=('arial',20,'bold'),command=deleteuser,bd=5,bg='red',fg='white')
    btn_deleteuser.place(relx=0,rely=.35,relwidth=.2)

    btn_viewuser=Button(frm,text='view user acn',font=('arial',20,'bold'),bd=5,bg='blue',fg='white',command=viewuser)
    btn_viewuser.place(relx=0,rely=.55,relwidth=.2)
   
def newuser_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.73)

    frm_title=Label(frm,text=' Open New Account',font=('arial',30,'bold'),bg='powder blue',fg='green')
    frm_title.pack()
    
    def logout():
        frm.destroy()
        main_screen()

    def back():
        frm.destroy()
        welcome_admin_screen()

    def reset():
        e_name.delete(0,"end")
        e_mob.delete(0,"end")
        e_email.delete(0,"end")
        e_adhar.delete(0,"end")

    def newuser_db():
        uname=e_name.get()
        umob=e_mob.get()
        umail=e_email.get()
        uadhar=e_adhar.get()
        ubal=0
        upass=''
        for i in range(3):
            i=random.randint(65,90)
            c=chr(i)
            j=random.randint(0,9)
            upass=upass+str(j)+c

        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into users(users_name,users_pass,users_mob,users_email,users_bal,users_adhar,users_opendate) values(?,?,?,?,?,?,?)",(uname,upass,umob,umail,ubal,uadhar,date))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute('select max(users_acno) from users')
        uacn=curobj.fetchone()[0]
        conobj.close()

        messagebox.showinfo('New User',f'ACN created with ACN:{uacn} & PASS:{upass}')
        try:
            con=gmail.GMail('rahulvatskirthal@gmail.com','ovct rcyq sadi dvcg')
            utext=f'''hello,{uname},
            Your account has been opened successfully with HDFC BANK
            Your Account No is {uacn}
            Your password is {upass}

            kindly change your password when you login to app

            Thanks
            HDFC BANK corp
            '''

            msg=gmail.Message(to=umail,subject='Account opened successfully',text=utext)
            con.send(msg)
            messagebox.showinfo('New User',f'Mail send successfully')
   
        except:
            messagebox.showerror('Network problem','somthing want wrong with network')
            
    btn_logout=Button(frm,text='logout',font=('arial',20,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.91,rely=0)

    btn_back=Button(frm,text='back',font=('arial',20,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_name=Label(frm,text='Name',font=('arial',20,'bold'),bg='powder blue')
    lbl_name.place(relx=.25,rely=.2)

    e_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_name.place(relx=.35,rely=.2)
    e_name.focus()

    lbl_mob=Label(frm,text='Mob',font=('arial',20,'bold'),bg='powder blue')
    lbl_mob.place(relx=.25,rely=.36)

    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=.35,rely=.35)

    lbl_email=Label(frm,text='Email',font=('arial',20,'bold'),bg='powder blue')
    lbl_email.place(relx=.25,rely=.51)

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.35,rely=.5)

    lbl_adhar=Label(frm,text='Adhar',font=('arial',20,'bold'),bg='powder blue')
    lbl_adhar.place(relx=.25,rely=.65)

    e_adhar=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_adhar.place(relx=.35,rely=.65)

    btn_submit=Button(frm,text='submit',font=('arial',20,'bold'),bd=5,bg='green',command=newuser_db)
    btn_submit.place(relx=.37,rely=.8,relwidth=.1)

    btn_reset=Button(frm,text='reset',font=('arial',20,'bold'),bd=5,bg='red',command=reset)
    btn_reset.place(relx=.48,rely=.8,relwidth=.1)

def deleteuser_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.73)

    frm_title=Label(frm,text=' Delete User Account',font=('arial',30,'bold'),bg='powder blue',fg='green')
    frm_title.pack()
    
    def logout():
        frm.destroy()
        main_screen()

    def back():
        frm.destroy()
        welcome_admin_screen()

    def reset():
        e_acn.delete(0,"end")
        e_adhar.delete(0,"end")

    def delete():
        uacn=e_acn.get()
        uadhar=e_adhar.get()
        conobj=sqlite3.connect('bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('delete from users where users_acno=? and users_adhar=?',(uacn,uadhar))
        curobj.execute('delete from txn where txn_acno=?',(uacn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo('Delete User','Account deleted' )
     
    btn_logout=Button(frm,text='logout',font=('arial',20,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.91,rely=0)

    btn_back=Button(frm,text='back',font=('arial',20,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='ACNo.',font=('arial',20,'bold'),bg='powder blue')
    lbl_acn.place(relx=.2,rely=.2)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.3,rely=.2)
    e_acn.focus()

    lbl_adhar=Label(frm,text='Adhar',font=('arial',20,'bold'),bg='powder blue')
    lbl_adhar.place(relx=.2,rely=.35)

    e_adhar=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_adhar.place(relx=.3,rely=.35)

    btn_submit=Button(frm,text='submit',font=('arial',20,'bold'),bd=5,bg='green',command=delete)
    btn_submit.place(relx=.31,rely=.45,relwidth=.1)

    btn_reset=Button(frm,text='reset',font=('arial',20,'bold'),bd=5,bg='red',command=reset)
    btn_reset.place(relx=.43,rely=.45,relwidth=.1)

def viewuser_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.73)

    frm_title=Label(frm,text=' View User Account',font=('arial',30,'bold'),bg='powder blue',fg='green')
    frm_title.pack()
    
    def logout():
        frm.destroy()
        main_screen()

    def back():
        frm.destroy()
        welcome_admin_screen()

    def view():
        uacn=e_acn.get()

        conobj=sqlite3.connect('bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select * from users where users_acno=?",(uacn,))
        tup=curobj.fetchone()
        conobj.close()

        if tup==None:
            messagebox.showerror('View','Account does not exist')
            return
        
        lbl_acn=Label(frm,text=f'ACNo',font=('arial',20,'bold'),bg='powder blue')
        lbl_acn.place(relx=.1,rely=.35)

        lbl_acn_val=Label(frm,text=tup[0],font=('arial',20,'bold'),bg='powder blue',fg='purple')
        lbl_acn_val.place(relx=.35,rely=.35)

        lbl_name=Label(frm,text=f'Name',font=('arial',20,'bold'),bg='powder blue')
        lbl_name.place(relx=.6,rely=.35)

        lbl_name_val=Label(frm,text=tup[1],font=('arial',20,'bold'),bg='powder blue',fg='purple')
        lbl_name_val.place(relx=.72,rely=.35)

        lbl_mob=Label(frm,text=f'mob',font=('arial',20,'bold'),bg='powder blue')
        lbl_mob.place(relx=.1,rely=.55)

        lbl_mob_val=Label(frm,text=tup[3],font=('arial',20,'bold'),bg='powder blue',fg='purple')
        lbl_mob_val.place(relx=.25,rely=.55)

        lbl_adhar=Label(frm,text=f'Adhar',font=('arial',20,'bold'),bg='powder blue')
        lbl_adhar.place(relx=.6,rely=.55)

        lbl_adhar_val=Label(frm,text=tup[6],font=('arial',20,'bold'),bg='powder blue',fg='purple')
        lbl_adhar_val.place(relx=.72,rely=.55)

        lbl_opendate=Label(frm,text='Oped date',font=('arial',20,'bold'),bg='powder blue')
        lbl_opendate.place(relx=.1,rely=.75)

        lbl_opendate_val=Label(frm,text=tup[7],font=('arial',20,'bold'),bg='powder blue',fg='purple')
        lbl_opendate_val.place(relx=.28,rely=.75)

        lbl_bal=Label(frm,text='Bal',font=('arial',20,'bold'),bg='powder blue')
        lbl_bal.place(relx=.6,rely=.75)

        lbl_bal_val=Label(frm,text=tup[5],font=('arial',20,'bold'),bg='powder blue',fg='purple')
        lbl_bal_val.place(relx=.75,rely=.75)


    btn_logout=Button(frm,text='logout',font=('arial',20,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.91,rely=0)

    btn_back=Button(frm,text='back',font=('arial',20,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='ACNo.',font=('arial',20,'bold'),bg='powder blue')
    lbl_acn.place(relx=.2,rely=.15)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.3,rely=.15)
    e_acn.focus()

    btn_search=Button(frm,text='Search',font=('arial',20,'bold'),bd=5,bg='green',command=view)
    btn_search.place(relx=.57,rely=.13)

def welcome_user_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.73)
    screen_title='User Home Screen'
    frm_title=Label(frm,text=screen_title,font=('arial',30,'bold','underline'),bg='powder blue',fg='blue')
    frm_title.pack() 

    lbl_wel=Label(frm,text=F'Welcome,{welcome_user}',font=('arial',20,'bold'),bg='powder blue',fg='green')
    lbl_wel.place(relx=0,rely=0)
    
    def logout():
        frm.destroy()
        main_screen()

    def deposite_screen():
        screen_title='User Deposite Screen'
        frm_title.configure(text=screen_title)

        def deposit():
            uamt=int(e_amt.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,user_acno))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select users_bal from users where users_acno=?',(user_acno,))
            ubal=curobj.fetchone()[0]

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'cr',uamt,ubal,date))
            conobj.commit()
            conobj.close()

            messagebox.showinfo('Deposit',f'{uamt} deposited,Updated bal:{ubal}')


        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.65,relheight=.85)

        lbl_amt=Label(ifrm,text='Amt',font=('arial',20,'bold'),bg='white')
        lbl_amt.place(relx=.25,rely=.2)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.35,rely=.2)

        btn_submit=Button(frm,text='Submit',font=('arial',20,'bold'),bd=5,bg='green',command=deposit)
        btn_submit.place(relx=.55,rely=.38)

    def withdraw_screen():
        screen_title='User Withdraw Screen'
        frm_title.configure(text=screen_title)

        def withdraw():
            uamt=int(e_amt.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select users_bal from users where users_acno=?',(user_acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()
            if ubal>uamt:

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('Update users set users_bal=users_bal-? where users_acno=?',(uamt,user_acno))
                conobj.commit()
                conobj.close()

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'dr',uamt,ubal-uamt,date))
                conobj.commit()
                conobj.close()

                messagebox.showinfo('Withdraw',f'{uamt} withdrawn,Updated bal:{ubal-uamt}')

            else:
                messagebox.showerror('withdraw',f'Insufficient Bal:{ubal}')
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.65,relheight=.85)

        lbl_amt=Label(ifrm,text='Amt',font=('arial',20,'bold'),bg='white')
        lbl_amt.place(relx=.25,rely=.2)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.35,rely=.2)

        btn_submit=Button(frm,text='Submit',font=('arial',20,'bold'),bd=5,bg='green',command=withdraw)
        btn_submit.place(relx=.55,rely=.38)

    def update_screen():
        screen_title='User Update Screen'
        frm_title.configure(text=screen_title)

        def update_db():
            upass=e_pass.get()
            umob=e_mob.get()
            uemail=e_email.get()
            conobj=sqlite3.connect('bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('update users set users_pass=?,users_mob=?,users_email=? where users_acno=?',(upass,umob,uemail,user_acno))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Update Details','Updated')

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.65,relheight=.85)

        lbl_pass=Label(ifrm,text='Pass',font=('arial',20,'bold'),bg='white')
        lbl_pass.place(relx=.15,rely=.15)

        e_pass=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_pass.place(relx=.25,rely=.15)

        lbl_mob=Label(ifrm,text='Mob',font=('arial',20,'bold'),bg='white')
        lbl_mob.place(relx=.15,rely=.3)

        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_mob.place(relx=.25,rely=.3)

        lbl_email=Label(ifrm,text='Email',font=('arial',20,'bold'),bg='white')
        lbl_email.place(relx=.15,rely=.45)

        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_email.place(relx=.25,rely=.45)

        btn_submit=Button(frm,text='Submit',font=('arial',20,'bold'),bd=5,bg='green',command=update_db)
        btn_submit.place(relx=.48,rely=.6)
        
        conobj=sqlite3.connect('bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select users_pass,users_mob,users_email from users where users_acno=?",(user_acno,))
        tup=curobj.fetchone()
        conobj.close()

        e_pass.insert(0,tup[0])
        e_mob.insert(1,tup[1])
        e_email.insert(2,tup[2])


    def transfer_screen():
        screen_title='User Transfer Screen'
        frm_title.configure(text=screen_title)

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.65,relheight=.85)

        def transfer():
            uamt=int(e_amt.get())
            utoacn=int(e_to.get())

            conobj=sqlite3.connect('bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select * from users where users_acno=?',(utoacn,) )
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                    messagebox.showerror('Transfer','Invalid to ACN')
                    return
            else:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select users_bal from users where users_acno=?',(user_acno,))
                ubal=curobj.fetchone()[0]
                conobj.close()
                if ubal>uamt:

                    conobj=sqlite3.connect(database='bank.sqlite')
                    curobj=conobj.cursor()
                    curobj.execute('Update users set users_bal=users_bal-? where users_acno=?',(uamt,user_acno))
                    curobj.execute('Update users set users_bal=users_bal+? where users_acno=?',(uamt,utoacn))

                    conobj.commit()
                    conobj.close()

                    conobj=sqlite3.connect(database='bank.sqlite')
                    curobj=conobj.cursor()
                    curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'dr',uamt,ubal-uamt,date))
                    curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(utoacn,'cr',uamt,ubal+uamt,date))

                    conobj.commit()
                    conobj.close()

                    messagebox.showinfo('Transfer',f'{uamt} Transferd,Updated bal:{ubal-uamt}')

                else:
                    messagebox.showerror('Transfer',f'Insufficient Bal:{ubal}')

  
    
        lbl_to=Label(ifrm,text='To ACno',font=('arial',20,'bold'),bg='white')
        lbl_to.place(relx=.15,rely=.3)

        e_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_to.place(relx=.35,rely=.3)

        lbl_amt=Label(ifrm,text='Amt',font=('arial',20,'bold'),bg='white')
        lbl_amt.place(relx=.15,rely=.45)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.35,rely=.45)

        btn_submit=Button(frm,text='Submit',font=('arial',20,'bold'),bd=5,bg='green',command=transfer)
        btn_submit.place(relx=.55,rely=.6)

    def acn_history_screen():
        screen_title='User Txn History Screen'
        frm_title.configure(text=screen_title)

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.65,relheight=.85)

        data={}
        conobj=sqlite3.connect('bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select * from txn where txn_acno=?",(user_acno,))
        tups=curobj.fetchall()
        i=1
        for tup in tups:
            data[str(i)]={'Txn Amt':tup[3],'Txn type':tup[2],'Updated Bal':tup[4],'Txn date':tup[5],'Txn Id':tup[0]}
            i+=1
        model = TableModel()
        model.importDict(data)

        table_frm=Frame(ifrm)
        table_frm.place(relx=.2,rely=.2)
        table=TableCanvas(table_frm,model=model,editable=False)
        table.show()

    def details_screen():
        screen_title='User Details Screen'
        frm_title.configure(text=screen_title)

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.1,relwidth=.65,relheight=.85)

        conobj=sqlite3.connect('bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select * from users where users_acno=?",(user_acno,))
        tup=curobj.fetchone()
        conobj.close()

        lbl_acn=Label(ifrm,text=f'ACNo',font=('arial',20,'bold'),bg='white')
        lbl_acn.place(relx=.1,rely=.15)

        lbl_acn_val=Label(ifrm,text=tup[0],font=('arial',20,'bold'),bg='white',fg='purple')
        lbl_acn_val.place(relx=.35,rely=.15)

        lbl_name=Label(ifrm,text=f'Name',font=('arial',20,'bold'),bg='white')
        lbl_name.place(relx=.6,rely=.15)

        lbl_name_val=Label(ifrm,text=tup[1],font=('arial',20,'bold'),bg='white',fg='purple')
        lbl_name_val.place(relx=.72,rely=.15)

        lbl_mob=Label(ifrm,text=f'mob',font=('arial',20,'bold'),bg='white')
        lbl_mob.place(relx=.1,rely=.35)

        lbl_mob_val=Label(ifrm,text=tup[3],font=('arial',20,'bold'),bg='white',fg='purple')
        lbl_mob_val.place(relx=.25,rely=.35)

        lbl_adhar=Label(ifrm,text=f'Adhar',font=('arial',20,'bold'),bg='white')
        lbl_adhar.place(relx=.6,rely=.35)

        lbl_adhar_val=Label(ifrm,text=tup[6],font=('arial',20,'bold'),bg='white',fg='purple')
        lbl_adhar_val.place(relx=.72,rely=.35)

        lbl_opendate=Label(ifrm,text='Oped date',font=('arial',20,'bold'),bg='white')
        lbl_opendate.place(relx=.1,rely=.55)

        lbl_opendate_val=Label(ifrm,text=tup[7],font=('arial',20,'bold'),bg='white',fg='purple')
        lbl_opendate_val.place(relx=.28,rely=.55)

        lbl_bal=Label(ifrm,text='Bal',font=('arial',20,'bold'),bg='white')
        lbl_bal.place(relx=.6,rely=.55)

        lbl_bal_val=Label(ifrm,text=tup[5],font=('arial',20,'bold'),bg='white',fg='purple')
        lbl_bal_val.place(relx=.75,rely=.55)

    def update_picture():
        img_path=filedialog.askopenfilename()
        shutil.copy(img_path,f'{user_acno}.png')

        pro_img=Image.open(f'{user_acno}.png').resize((250,120))
        pro_bitmap_img=ImageTk.PhotoImage(pro_img,master=frm)

        prolbl_img=Label(frm,image=pro_bitmap_img)
        prolbl_img.image=pro_bitmap_img

        prolbl_img.place(relx=0,rely=.06)


    btn_logout=Button(frm,text='logout',font=('arial',20,'bold'),bd=5,command=logout,bg='red')
    btn_logout.place(relx=.91,rely=0)

    if os.path.exists(f'{user_acno}.png'):
        pro_img=Image.open(f'{user_acno}.png').resize((250,120))
    else:
        pro_img=Image.open('default.jpg').resize((250,120))

    pro_bitmap_img=ImageTk.PhotoImage(pro_img,master=frm)

    prolbl_img=Label(frm,image=pro_bitmap_img)
    prolbl_img.image=pro_bitmap_img
    prolbl_img.place(relx=0,rely=.06)

    btn_update_pro=Button(frm,text='update picture',font=('arial',10),bd=5,command=update_picture)
    btn_update_pro.place(relx=0,rely=.28)

    btn_details=Button(frm,text='Check details',command=details_screen,font=('arial',20,'bold'),bd=5,bg='yellow',fg='red')
    btn_details.place(relx=0,rely=.34,relwidth=.2)

    btn_deposit=Button(frm,text='deposit',command=deposite_screen,font=('arial',20,'bold'),bd=5,bg='green',fg='white')
    btn_deposit.place(relx=0,rely=.44,relwidth=.2)

    btn_withdraw=Button(frm,text='withraw',command=withdraw_screen,font=('arial',20,'bold'),bd=5,bg='red',fg='white')
    btn_withdraw.place(relx=0,rely=.55,relwidth=.2)

    btn_update=Button(frm,text='update',command=update_screen,font=('arial',20,'bold'),bd=5,bg='yellow',fg='blue')
    btn_update.place(relx=0,rely=.66,relwidth=.2)

    btn_transfer=Button(frm,text='tranfer',command=transfer_screen,font=('arial',20,'bold'),bd=5,bg='blue',fg='white')
    btn_transfer.place(relx=0,rely=.77,relwidth=.2)

    btn_history=Button(frm,text='txn history',command=acn_history_screen,font=('arial',20,'bold'),bd=5)
    btn_history.place(relx=0,rely=.88,relwidth=.2)

main_screen()
win.mainloop()

