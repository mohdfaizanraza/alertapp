import datetime
import os
import mysql.connector
import playsound

# connecting to mysql database
mydb=mysql.connector.connect(host='localhost',user='root',password='',database='TODOTRACKER') 

# checking connection and if database exist if not then creating database and table
if mydb:   
    cur=mydb.cursor()
    stmt = "SHOW DATABASES LIKE 'TODOTRACKER'"
    cur.execute(stmt)
    result = cur.fetchone()
    if result:
        pass
    else:
        cur.execute("CREATE DATABASE TODOTRACKER")
        create_querry="CREATE TABLE Track(trackid integer(10) NOT NULL AUTO_INCREMENT,tdate date NOT NULL,twork varchar(20) NOT NULL,ttime time(0) NOT NULL,tampm varchar(2),PRIMARY KEY (trackid))"
        cur.execute(create_querry)
else:
    print("connection not established !!")


# function renders all activity done till date
def seeTrack():
    Select_Querry="select * from Track"
    cur.execute(Select_Querry)
    result=cur.fetchall()
    for x in result:
        print(x)


print("set your plan for today")

work=[]
time=[]
output=''

#creating list which has to complete today
while 1:
    n=input("Enter the work")
    work.append(n)
    opt=input("do you want to continue:[y/n]")
    
    if opt.lower()=='n':
        break
    
print("your plan for today")

count=1

#displaying play for today
for i in work:
    print(count,".",i)
    count+=1

#setting alert sound for particular work which will remind its time to complete task
for i in work:
    os.system("clear")
    print("Set the timer so tha we can alert you for",i)

    while 1:
        time.clear()
        hour=int(input("Enter hour"))
        time.append(hour)
        minute=int(input("And what minutes ?"))
        time.append(minute)
        amPm=str(input("am or pm?"))

        reset=input("Are you confirm [yes/no]")

        if reset.lower()=="yes":
            break
        
    
    print("waiting for timer",hour,minute,amPm)
    
    if(amPm=="pm"):
        hour=hour+12
        
    while 1:
        
        if(hour==datetime.datetime.now().hour and minute==datetime.datetime.now().minute):
            
            playsound.playsound('beep-02.mp3')
            print("Time to start",i)
            
            Insert_Query="INSERT INTO Track(tdate,twork,ttime,tampm) VALUES(%s,%s,%s,%s)"
            
            for x in time:
                output+=str(x)
                
            values=(datetime.date.today(),i,output,amPm)
            cur.execute(Insert_Query,values)
            mydb.commit()
            time.clear()
            break
        
print("plan executed for today")


#traking the plans which has executed
while 1:
    n=input("1 :- press 1 to see you track\n2 :- see date wise\n3 :- exit\n")
    
    if n=='1':
        seeTrack()
    elif n=='2':
     
        year=input("Enter the year")
            
        month=input("enter the month")
            
        date=input("enter the date")

        select_query="select * from Track where tdate = '%s'"
        
        #handling code for date
        try:
            cur.execute(select_query,datetime.date(int(year), int(month), int(date)))
        except  ValueError:
            print("pls enter proper date")
            
        result=cur.fetchall()
        
        if result:
            for x in result:
                print(x)
        else:
            print("No data found")
            
    elif n=='3':
        break
        
    else:
        print("pleas select proper option")

