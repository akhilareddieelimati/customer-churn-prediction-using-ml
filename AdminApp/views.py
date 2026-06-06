from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import joblib
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib.pyplot as plt

# Create your views here.
def index(request):
    return render(request,'index.html')

def AdminAction(request):
    uname=request.POST['username']
    passw=request.POST['password']
    if uname == 'Admin' and passw == 'Admin':
        return render(request,'AdminApp/AdminHome.html')
    else:
        context={'msg':'Admin Login Failed..!!'}
        return render(request,'AdminApp/index.html',context)

def AdminHome(request):
    return render(request,'AdminApp/AdminHome.html')

global data
def loaddataset(request):
    global data
    data=pd.read_csv("Dataset/telecom_customer_churn.csv", encoding='unicode_escape')
    context={'data':data,'msg':'Dataset Loaded Successfully..!!'}
    return render(request,'AdminApp/AdminHome.html',context)

global X, y, X_train, X_test, y_train, y_test


def preprocess(request):

    global X, y, X_train, X_test, y_train, y_test

    data.drop(columns=['Customer ID','City','Zip Code','Offer','Churn Category','Churn Reason','Premium Tech Support'], inplace=True)
    data.dropna(inplace=True)

    data['Gender']=data['Gender'].map({'Female':1,'Male':0})
    data['Married']=data['Married'].map({'Yes':1,'No':0})
    data['Phone Service']=data['Phone Service'].map({'Yes':1,'No':0})

    data['Multiple Lines']=data['Multiple Lines'].map({'Yes':1,'No':0})
    data['Internet Service']=data['Internet Service'].map({'Yes':1,'No':0})
    data['Internet Type']=data['Internet Type'].map({'Cable':2,'Fiber Optic':0,'DSL':1})

    data['Online Security']=data['Online Security'].map({'Yes':1,'No':0})
    data['Online Backup']=data['Online Backup'].map({'Yes':1,'No':0})
    data['Device Protection Plan']=data['Device Protection Plan'].map({'Yes':1,'No':0})

    data['Streaming TV']=data['Streaming TV'].map({'Yes':1,'No':0})
    data['Streaming Movies']=data['Streaming Movies'].map({'Yes':1,'No':0})
    data['Streaming Music']=data['Streaming Music'].map({'Yes':1,'No':0})
    data['Unlimited Data']=data['Unlimited Data'].map({'Yes':1,'No':0})
    data['Contract']=data['Contract'].map({'Month-to-Month':0,'One Year':1,'Two Year':2})
    data['Paperless Billing']=data['Paperless Billing'].map({'Yes':1,'No':0})

    data['Payment Method']=data['Payment Method'].map({'Bank Withdrawal':0,'Credit Card':1,'Mailed Check':2})
    data['Customer Status']=data['Customer Status'].map({'Stayed':0,'Churned':1,'Joined':2})

    X = data.iloc[:, 0:30]
    y = data.iloc[:, 30:31]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    context={'data':str(len(data)),'train':str(len(X_train)), 'test':str(len(y_test))}
    return render(request, "AdminApp/Preprocess.html", context)

global svmacc
def runSVM(request):
    global svmacc
    svm_model=svm.SVC()
    svm_model.fit(X_train,y_train)
    joblib.dump(svm_model, "Model/SVMModel.joblib")
    pred = svm_model.predict(X_test)
    svmacc=accuracy_score(y_test, pred)
    pred = svmacc*100
    context={'data':'SVM Run Successfully..!!', 'acc': str(pred)}
    return render(request, "AdminApp/Algorithms.html", context)

global rmacc
def runRF(request):
    global rmacc
    rmmodel=RandomForestClassifier()
    rmmodel.fit(X_train,y_train)
    joblib.dump(rmmodel, "Model/RFModel.joblib")
    pred = rmmodel.predict(X_test)
    rmacc=accuracy_score(y_test, pred)
    pred = rmacc*100
    context={'data':'Random Forest Run Successfully..!!', 'acc': str(pred)}
    return render(request, "AdminApp/Algorithms.html", context)

def runComparison(request):
    bars = ['SVM','RandomForest']
    heights = [svmacc, rmacc]
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, heights)
    plt.xticks(y_pos, bars)
    plt.show()

    fig = plt.figure(figsize =(8, 5))
    plt.pie(heights, labels =bars )
    plt.show()
    return render(request,'AdminApp/AdminHome.html')
