from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import requests
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#------------ Main Window to Add Window --------------------#
def mw_to_aw():
    mw.withdraw()
    aw.deiconify()

def aw_to_mw():
    aw.withdraw()
    mw.deiconify()
#-----------------------------------------------------------#

#------------ Main Window to View Window -------------------#
def mw_to_vemp():
    mw.withdraw()
    vw.deiconify()
    vw_emp_data.delete(1.0, END)
    con=None
    try:
        con=connect("final_project.db")
        cursor=con.cursor()
        sql="select * from employee"
        cursor.execute(sql)
        data=cursor.fetchall()
        info=""
        for d in data:
            info= info + "ID:" + str(d[0]) + "  Name:" + str(d[1]) + "  Salary:" + str(d[2]) + "\n"
        vw_emp_data.insert(INSERT, info)
    except Exception as e:
        showerror("Error", e)
    finally:
        if con is not None:
            con.close()

def vw_to_mw():
    vw.withdraw()
    mw.deiconify()
    
#-----------------------------------------------------------#

#------------ Main Window to Update Window -----------------#
def mw_to_uw():
    mw.withdraw()
    uw.deiconify()

def uw_to_mw():
    uw.withdraw()
    mw.deiconify()
#-----------------------------------------------------------#

#------------ Main Window to Delete Window -----------------#
def mw_to_dw():
    mw.withdraw()
    dw.deiconify()

def dw_to_mw():
    dw.withdraw()
    mw.deiconify()
#-----------------------------------------------------------#

#------------ Main Window to Chart Window -------------------#
def chart():
    mw.withdraw()
    
    con=None
    try:
        con=connect("final_project.db")
        cursor=con.cursor()
        sql="select name, salary from employee order by salary desc limit 5"
        cursor.execute(sql)
        data=cursor.fetchall()
        name=[]
        salary=[]
        for d in data:
            name.append(d[0])
            salary.append(d[1])

        
        plt.bar(name , salary, color=["red"],width=0.5)
                
        plt.xlabel("Name")
        plt.ylabel("Salary")
        plt.title("Salary Top 5")
        plt.show()
    except Exception as e:
        showerror("Error", e)
    finally:
        if con is not None:
            con.close()

    if askokcancel("Are you sure","Do you want to exit?"):
        mw.deiconify()


#-----------------------------------------------------------#

#----------------------- Add Employee Function --------------------#
def add_emp():
    con=None
    try:
        con=connect("final_project.db")
        cursor=con.cursor()
        sql="insert into employee values('%d', '%s', '%d')"

        
        eid=aw_ent_e_id.get()     
        if eid=="":
            raise Exception("ID should not be empty.")  
        elif not(eid.isdigit()):        
            raise Exception ('Only positive integers are allowed.')
        else:
            eid=int(aw_ent_e_id.get())
            if eid<=0: 
                raise Exception("ID should contain positive integers only.") 
        

        
        name=aw_ent_name.get()        
        if name=="":
            raise Exception("Name should not be empty.")
        elif not(name.isalpha()):
            raise Exception("Name should contain only alphabets.")
        elif len(name)==0 or len(name)<2:
            raise Exception("Minimum 2 alphabets must be provided in a name.")
        
		
        sal=aw_ent_sal.get()
        if sal=="":
            raise Exception("Salary should not be empty.")
        elif not(sal.isdigit()):
            raise Exception("Only positive integers are allowed.")
        else:
            sal=float(aw_ent_sal.get())
            if sal<=8000:
                raise Exception("Minimum salary should be 8000.")        


        cursor.execute(sql % (eid, name, sal))
        con.commit()
        showinfo("Success", "Record added")


    except IntegrityError:
        showerror("Error", "ID already exist.")
        raise Exception("ID already exist.")    
    except Exception as e:
        con.rollback()
        showerror("Error", e)
    
    finally:
        aw_ent_e_id.delete(0,END)
        aw_ent_name.delete(0,END)
        aw_ent_sal.delete(0,END)
        aw_ent_e_id.focus()
        if con is not None:
            con.close()
#----------------------------------------------------------------#

#----------------------- Update Window Function ------------------------#
def update_emp():
    con=None
    try:
        con=connect("final_project.db")
        cursor=con.cursor()
        sql="update employee set name='%s', salary=%d where e_id='%d'"

        eid=uw_ent_e_id.get()
        if eid=="":
            raise Exception("ID should not be empty.")  
        elif not(eid.isdigit()):        
            raise Exception ('Only positive integers are allowed.')
        else:
            eid=int(uw_ent_e_id.get())
            if eid<=0: 
                raise Exception("ID should contain positive integers only.") 

		
        name=uw_ent_name.get()
        if name=="":
            raise Exception("Name should not be empty.")
        elif not(name.isalpha()):
            raise Exception("Name should contain only alphabets.")
        elif len(name)==0 or len(name)<2:
            raise Exception("Minimum 2 alphabets must be provided in a name.")
		
        sal=uw_ent_sal.get()
        if sal=="":
            raise Exception("Salary should not be empty.")
        elif not(sal.isdigit()):
            raise Exception("Only positive integers are allowed.")
        else:
            sal=float(uw_ent_sal.get())
            if sal<=8000:
                raise Exception("Minimum salary should be 8000.")

        cursor.execute(sql % (name, sal, eid))
        if cursor.rowcount==1:
            con.commit()
            showinfo("Success", "Record Updated.")
        else:
            showerror("Error", "ID does not exist.")

    except IntegrityError:
        showerror("Error", "ID already exist.")
        raise Exception("ID already exist.")
        
    except Exception as e:
        con.rollback()
        showerror("Error", e)
    finally:
        uw_ent_e_id.delete(0,END)
        uw_ent_name.delete(0,END)
        uw_ent_sal.delete(0,END)
        uw_ent_e_id.focus()
        if con is not None:
            con.close()

#-----------------------------------------------------------------------#

#------------------------Delete Window Function ------------------------#
def delete_emp():
	con = None
	try:
		con = connect("final_project.db")
		sql = "delete from employee where e_id='%d'"
		cursor = con.cursor()

        
		eid = int(dw_ent_e_id.get())
        
		cursor.execute(sql%(eid))
		if cursor.rowcount == 1:
			con.commit()
			showinfo("Notice","Employee Record Deleted")
		else:
			showerror("Error","Id does not exist")
    
    
    
	except Exception as e:
		con.rollback()
		showerror("Error",e)        
	finally:
		if con is not None:
			con.close()


#------------------------------------------ Main Window -----------------------------------------------#
mw=Tk()
mw.title("Employee Manageement System")
mw.geometry("900x700+50+50")
mw.configure(bg='MediumPurple2')

f=("Arial", 30, "bold")
f_med=("Arial", 20, "normal")
y=10


mw_title=Label(mw, text="Employee Management System", font=f, bg='MediumPurple2')
mw_add_btn = Button(mw, text="Add Employees", font=f, width=15, bg="SeaGreen3", command=mw_to_aw)
mw_view_btn = Button(mw, text="View Employees", font=f, width=15, bg="goldenrod3", command=mw_to_vemp)
mw_update_btn = Button(mw, text="Update Employees", font=f, width=15, bg="dark turquoise", command=mw_to_uw)
mw_delete_btn = Button(mw, text="Delete Employees", font=f, width=15, bg="OrangeRed3", command=mw_to_dw)
mw_charts_btn = Button(mw, text="Charts", font=f, width=15, bg='MediumOrchid3', command=chart)

mw_title.pack(pady=y)
mw_add_btn.pack(pady=y)
mw_view_btn.pack(pady=y)
mw_update_btn.pack(pady=y)
mw_delete_btn.pack(pady=y)
mw_charts_btn.pack(pady=y)


try:
	wa = "https://ipinfo.io"
	res = requests.get(wa)
	data = res.json()
	city = data["city"]
	state = data["region"]
	loc = data["loc"]
	latlong = loc.split(",")
	lat = latlong[0]
	lng = latlong[1]

	a1 = "https://api.openweathermap.org/data/2.5/weather"
	a2="?q=" + city
	a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
	a4 = "&units="+"metric"

	wa = a1 + a2+ a3 + a4
	res = requests.get(wa)
	data = res.json()
	temp = data["main"]["temp"]

except Exception as e:
	print("issue",e)

city_info = Label(mw, text="You Are In : ", bg="MediumPurple2", font = f_med)
city_name = Label(mw, text=city, bg="MediumPurple2" , font = f_med)
temp_info = Label(mw, text= "Temprature : ", bg="MediumPurple2" , font = f_med)
temp_value = Label(mw, text= temp, bg="MediumPurple2", font=f_med)


city_info.place(x = 120, y = 600)
city_name.place(x = 275, y = 600)
temp_info.place(x = 480, y = 600)
temp_value.place(x = 650, y = 600)


#---------------------------------- End Main Window ------------------------------------------#

#------------------------------------------ Add Window -----------------------------------------------#
aw=Toplevel(mw)
aw.title("Add Employee")
aw.geometry("900x700+50+50")
aw.configure(bg="SeaGreen1")

aw_lab_e_id=Label(aw, text="Enter Employee ID", font=f, bg="SeaGreen1")
aw_ent_e_id=Entry(aw, font=f)
aw_lab_name=Label(aw, text="Enter Employee Name", font=f, bg="SeaGreen1")
aw_ent_name=Entry(aw, font=f)
aw_lab_sal=Label(aw, text="Enter Employee Salary", font=f, bg="SeaGreen1")
aw_ent_sal=Entry(aw, font=f)
aw_btn_save=Button(aw, text="Save", font=f, command=add_emp, bg="SeaGreen3")
aw_btn_back=Button(aw, text="Back", font=f, command=aw_to_mw, bg="SeaGreen3")

aw_lab_e_id.pack(pady=y)
aw_ent_e_id.pack(pady=y)
aw_lab_name.pack(pady=y)
aw_ent_name.pack(pady=y)
aw_lab_sal.pack(pady=y)
aw_ent_sal.pack(pady=y)
aw_btn_save.pack(pady=y)
aw_btn_back.pack(pady=y)
aw.withdraw()
#----------------------------------------- End Add Window ------------------------------------------#

#------------------------------------------ View Window -----------------------------------------------#
vw=Toplevel(mw)
vw.title("View Employee")
vw.geometry("900x700+50+50")
vw.configure(bg="goldenrod1")

vw_emp_data=ScrolledText(vw, width=30, height=10, font=f, bg="khaki1")
vw_btn_back=Button(vw, text="Back", font=f, command=vw_to_mw, bg="goldenrod3")
vw_emp_data.pack(pady=y)
vw_btn_back.pack(pady=y)
vw.withdraw()
#---------------------------------- End View Window ------------------------------------------#

#------------------------------------------ Update Window -----------------------------------------------#
uw=Toplevel(mw)
uw.title("Update Employee")
uw.geometry("900x700+50+50")
uw.configure(bg='cyan')

uw_lab_e_id=Label(uw, text="Enter Employee ID", font=f, bg='cyan')
uw_ent_e_id=Entry(uw, font=f)
uw_lab_name=Label(uw, text="Enter Employee Name", font=f, bg='cyan')
uw_ent_name=Entry(uw, font=f)
uw_lab_sal=Label(uw, text="Enter Employee Salary", font=f, bg='cyan')
uw_ent_sal=Entry(uw, font=f)
uw_lab_e_id.pack(pady=y)
uw_ent_e_id.pack(pady=y)
uw_lab_name.pack(pady=y)
uw_ent_name.pack(pady=y)
uw_lab_sal.pack(pady=y)
uw_ent_sal.pack(pady=y)

uw_btn_update=Button(uw, text="Update", font=f, command=update_emp, bg="dark turquoise")
uw_btn_back=Button(uw, text="Back", font=f, command=uw_to_mw, bg="dark turquoise")
uw_btn_update.pack(pady=y)
uw_btn_back.pack(pady=y)
uw.withdraw()
#---------------------------------- End Update Window ------------------------------------------#

#------------------------------------------ Delete Window -----------------------------------------------#
dw=Toplevel(mw)
dw.title("Delete Employee")
dw.geometry("900x700+50+50")
dw.configure(bg='firebrick1')

dw_lab_e_id=Label(dw, text="Enter Employee ID", font=f, bg='firebrick1')
dw_ent_e_id=Entry(dw, font=f)
dw_lab_e_id.pack(pady=y)
dw_ent_e_id.pack(pady=y)


dw_btn_delete=Button(dw, text="Delete", font=f, command=delete_emp, bg="OrangeRed3")
dw_btn_back=Button(dw, text="Back", font=f, command=dw_to_mw, bg="OrangeRed3")
dw_btn_delete.pack(pady=y)
dw_btn_back.pack(pady=y)
dw.withdraw()
#---------------------------------- End Delete Window ------------------------------------------#

#------------------------------------------ Chart Window -----------------------------------------------#
'''
cw=Toplevel(mw)
cw.title("Chart")
cw.geometry("900x700+50+50")
cw.configure(bg='orchid1')


canvas=FigureCanvasTkAgg(cw, master=mw)
canvas.draw()
canvas.get_tk_widget().pack(pady=y)

cw_btn_back=Button(cw, text="Back", font=f, command=cw_to_mw, bg='MediumOrchid3')
cw_btn_back.pack(pady=y)
cw.withdraw()
'''
#---------------------------------- End Chart Window ------------------------------------------#


def confirmExit():
    if askokcancel("Are you sure","Do you want to exit?"):
        mw.destroy()
mw.protocol('WM_DELETE_WINDOW', confirmExit)

mw.mainloop()


