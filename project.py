import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
from datetime import datetime , date

def connect_db():
    conn = sqlite3.connect("myydb.db")
    return conn
def create_Table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS friend(name text,mobile text primary key,address text,email text,dob text)')
    conn.commit()
    conn.close()
create_Table()

def Reminder():
    st.subheader(" Birthday Reminder")
    today_str = date.today().strftime("%m-%d")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name, mobile, email, dob FROM friend")
    data = cur.fetchall()
    conn.close()

    birthday_friends = []
    for name, mobile, email, dob_str in data:
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            if dob.strftime("%m-%d") == today_str:
                birthday_friends.append((name, mobile, email))
        except:
            continue

    if birthday_friends:
        st.success(" Happy Birthday to these friends today!")
        for friend in birthday_friends:
            st.write(f"**{friend[0]}** |  {friend[1]} |  {friend[2]}")
    else:
        st.info("No birthdays today!")

def AddDetails():
    st.header("Enter Details")
    name = st.text_input("Friend's Name:")
    mobile = st.text_input("Friend's Mobile No.:")
    address = st.text_area("Friend's address:")
    email = st.text_input("Friend's Email:")
    dob = st.date_input("Friend's date of birth:",min_value=date(1900,1,1))
    data = (name,mobile,address,email,dob)
    if st.button("save record"):
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(f'select * from friend where mobile={mobile}')
            if cur.fetchall():
                st.error("User already exists")
                conn.close()
            else:
                conn = connect_db()
                cur = conn.cursor()
                cur.execute('INSERT INTO friend(name,mobile,address,email,dob) values(?,?,?,?,?)',data)
                conn.commit()
                conn.close()
                st.success("Details Added")
        except Exception as e:
            st.error(e)    
            st.error("Data not added ! Contact to your admin") 

def ViewDetails():
    st.subheader("Your Friends List")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('select * from friend')
    data = cur.fetchall()
    conn.close()
    st.table(data)     

def DeleteDetails():
    st.header("Delete Details")
    mobile = st.text_input("Enter mobile No") 
    if st.button('Delete'):
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(f"select * from friend where mobile={mobile}")
            if cur.fetchall():
                conn.close()
                conn = connect_db()
                cur = conn.cursor()
                cur.execute(f"delete from friend where mobile={mobile}")
                conn.commit()
                conn.close()
                st.success("Details Deleted")
            else:
                st.error("Details Not Found")    
        except Exception as e:
            st.error(e)
            st.error("Something wrong Contact to your admin")  

data=[]
def UpdateDetails():
    st.header('Update Details')
    mobile = st.text_input("Enter Mobile no to update Details")
    if st.button("Load Data"):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(f'select * from friend where mobile={mobile}')
        global data
        data = cur.fetchall()
        conn.close()
    st.table(data)
    name = st.text_input("friend's Name")
    address = st.text_area("friend's Address")
    email = st.text_input("Enter email")
    dob = st.date_input("Enter Date of Birth",min_value=date(1900,1,1))
    if st.button("Update"):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('update friend set name=?,address=?,email=?,dob=? where mobile=?',(name,address,email,dob,mobile))
        conn.commit()
        conn.close() 
        st.success("Details Deleted")
    else:
        st.error("Details Not Found")             

with st.sidebar:
    st.header(" Friends Directory & Birthday Reminder ")
    st.subheader("Store and manage your friends' details!")
    selected = option_menu("Select From Here",['Reminder','Add Details','View Details','Delete Details','Update Details'])

if selected =="Reminder":
    Reminder()    
elif selected =="Add Details":
    AddDetails()   
elif selected =="View Details":
    ViewDetails()   
elif selected =="Delete Details":
    DeleteDetails()    
elif selected =="Update Details":
    UpdateDetails()      