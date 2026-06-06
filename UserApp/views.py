from django.shortcuts import render
import sqlite3
import joblib

# Create your views here.
def login(request):
    return render(request,'UserApp/Login.html')
def register(request):
    return render(request,'UserApp/register.html')

def Userction(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    con = sqlite3.connect("ChurnDB.db")
    cur=con.cursor()
    cur.execute("select *  from user where username='"+username+"'and password='"+password+"'")
    data=cur.fetchone()
    if data is not None:
        request.session['user']=data[2]
        request.session['userid']=data[0]
        return render(request,'UserApp/UserHome.html')
    else:
        context={'data':'Login Failed ....!!'}
        return render(request,'UserApp/Login.html',context)
def UserHome(request):
    return render(request,'UserApp/UserHome.html')

def RegAction(request):
    name=request.POST['name']
    email=request.POST['email']
    mobile=request.POST['mobile']
    address=request.POST['address']
    username=request.POST['username']
    password=request.POST['password']

    con = sqlite3.connect("ChurnDB.db")
    cur=con.cursor()
    #cur.execute("CREATE TABLE user (ID INTEGER PRIMARY KEY AUTOINCREMENT,name varchar(100),email varchar(100),mobile varchar(100),address varchar(100) ,username varchar(100),password varchar(100))")
    cur.execute("select * from user where email='"+email+"'")
    d=cur.fetchone()
    if d is None:
        i=cur.execute("insert into user values(null,'"+name+"','"+email+"','"+mobile+"','"+address+"','"+username+"','"+password+"')")
        con.commit()
        con.close()
        if i == 0:
            context = {'data': 'Registration Failed...!!'}
            return render(request,'UserApp/register.html',context)
        else:
            context = {'data': 'Registration Successful...!!'}
            return render(request,'UserApp/register.html',context)
    else:
        context={'data':'Email Already Exist...!!'}
        return render(request,'UserApp/register.html',context)


def predictchurn(request):
    return render(request,'UserApp/predictchurn.html')

def PredAction(request):
    g=request.POST['gender']
    a=request.POST['age']
    m=request.POST['married']
    d=request.POST['dependents']
    lt=request.POST['latitude']
    Lg=request.POST['Longitude']

    ref=request.POST['referrals']
    ten=request.POST['tenure']
    ps=request.POST['phone_service']
    ld=request.POST['long_distance']
    ml=request.POST['multiple_lines']
    i_s=request.POST['internet_service']

    it=request.POST['internet_type']
    ad=request.POST['avg_download']
    os=request.POST['online_security']
    ob=request.POST['online_backup']
    dp=request.POST['device_protection']
    ST=request.POST['Streaming_TV']

    SM=request.POST['Streaming_Movies']
    SMu=request.POST['Streaming_Music']
    udata=request.POST['unlimited_data']
    Cont=request.POST['Contract']
    Pb=request.POST['Paperless_Billing']
    PM=request.POST['Payment_Method']

    Mc=request.POST['Monthly_Charge']
    TC=request.POST['Total_Charges']
    TR=request.POST['Total_Refunds']
    ec=request.POST['extra_charge']
    ld=request.POST['long_distance']
    TR=request.POST['Total_Revenue']

    RF_model=joblib.load("Model/RFModel.joblib")
    pred=RF_model.predict([[g,a,m,d,lt,Lg,ref,ten,ps,ld,ml,i_s,it,ad,os,ob,dp,ST,SM,SMu,udata,Cont,Pb,PM,Mc,TC,TR,ec,ld,TR]])
    print("predicted value: "+str(pred))
    if pred[0] == 0:
        context = {'data':'Predicted As ::: Stayed'}
        return render(request,'UserApp/PredictedData.html', context)
    elif pred[0] == 1:
        context = {'data':'Predicted As ::: Churned'}
        return render(request,'UserApp/PredictedData.html', context)
    else:
        context = {'data':'Predicted As ::: Joined'}
        return render(request,'UserApp/PredictedData.html', context)

