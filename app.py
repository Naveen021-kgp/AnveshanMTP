# from flask import Flask, render_template, request, jsonify, Markup,redirect,url_for
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return render_template('index.html')
# @app.route("/inner-page")
# def hel():
#     return render_template('inner-page.html')
# @app.route("/portfolio")
# def hell(): 
#     return render_template('portfolio-details.html')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify, Markup,redirect,url_for
# added code to avoid Tkinter errors

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import io, base64, os
import pandas as pd
import plotly.express as px
import plotly.io as pio
import seaborn as sns
# In python 2.7
import sys

app = Flask(__name__)
longitude=0
latitude=0
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    global latitude,longitude
    if request.method == 'POST':
        latitude = float(request.form.get("latitude"))
        
        longitude = float(request.form.get("longitude"))
        
        return redirect(url_for('sign',latitude=latitude, longitude=longitude))
        
    return render_template('index.html')
@app.route('/inner-page',methods=['GET','POST'])
def sign():
    # latitude,longitude
    
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    # latitude = request.form.get("latitude")
    # latitude=latitude
    # longitude=longitude
    # longitude = request.form.get("longitude")
    
    # url='https://power.larc.nasa.gov/api/temporal/daily/point?parameters=CLRSKY_SFC_SW_DWN,WS2M,T2M,PS,WS10M,WS50M&community=RE&longitude=85.51320840331054&latitude=22.65344840806398&start=20150101&end=20230228&format=CSV'
    url=f'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=CLRSKY_SFC_SW_DWN,WS2M,T2M,PS,WS10M,WS50M&community=RE&longitude={longitude}&latitude={latitude}&start=20210101&end=20220101&format=CSV'

    df = pd.read_csv(url, header=None,skiprows=14)
    df.columns=df. iloc[0]
    df = df.drop(df.index[:1])
    df["Density"]=df["PS"].astype(float)/(287.05*(df["T2M"].astype(float)+273))*1000
    for x in df:
      i=0
      for y in df[x]:
        if float(y)<0:
            df =  df.drop(df.index[i])
            i-=1
        i+=1
        
    dict1 = {'YEAR': 'year',
        'MO': 'month',
        'DY': 'day'}
 
# call rename () method
    df.rename(columns=dict1,inplace=True)
    df['year'] = pd.to_datetime(df[['year', 'month', 'day']])

# Drop the original day, month, and year columns
    df = df.drop(columns=['day', 'month'])
    dict1 = {'year': 'Date'}
 
# call rename () method
    df.rename(columns=dict1,inplace=True)
    
    df['CLRSKY_SFC_SW_DWN']=df['CLRSKY_SFC_SW_DWN'].astype(float)
    df['Solar Energy']=df['CLRSKY_SFC_SW_DWN']*(1*12)
    df['WS10M']=df['WS10M'].astype(float)
    df['Density']=df['Density'].astype(float)
    df["wind Energy"]=0.5*df['Density']*1*df['WS10M']
    # fig = px.scatter(df, x='Date', y='Solar Energy')
    sns.set()
    sns.distplot(df["Solar Energy"])
    plt.title("Solar Energy Distribution")
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    img_b64 = base64.b64encode(img_bytes.getvalue()).decode()

    SE_plot = Markup('<img src="data:image/png;base64,{}">'.format(img_b64))
    plt.close()
    
    sns.set()
    sns.distplot(df["wind Energy"])
    plt.title("Wind Energy Distribution")
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    img_b64 = base64.b64encode(img_bytes.getvalue()).decode()

    WE_plot = Markup('<img src="data:image/png;base64,{}">'.format(img_b64))
    plt.close()
    
    sns.set()
    sns.distplot(df["WS2M"])
    plt.title("Wind Velocity at 2meters Distribution")
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    img_b64 = base64.b64encode(img_bytes.getvalue()).decode()

    WS2M_plot = Markup('<img src="data:image/png;base64,{}">'.format(img_b64))
    plt.close()
    
    sns.set()
    sns.distplot(df["WS10M"])
    plt.title("Wind Velocity at 10meters Distribution")
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    img_b64 = base64.b64encode(img_bytes.getvalue()).decode()

    WS10M_plot = Markup('<img src="data:image/png;base64,{}">'.format(img_b64))
    plt.close()
    
    sns.set()
    sns.distplot(df["WS50M"])
    plt.title("Wind Velocity at 50meters Distribution")
    img_bytes = io.BytesIO()    
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    img_b64 = base64.b64encode(img_bytes.getvalue()).decode()

    WS50M_plot = Markup('<img src="data:image/png;base64,{}">'.format(img_b64))
    plt.close()
    
    sns.set()
    sns.distplot(df["CLRSKY_SFC_SW_DWN"])
    plt.title("Clear Sky Surface Shortwave Downward Irradiance (kW-hr/m^2/day) Distribution")
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    img_b64 = base64.b64encode(img_bytes.getvalue()).decode()

    SKY_plot = Markup('<img src="data:image/png;base64,{}">'.format(img_b64))
    plt.close()
    
    fig, ax = plt.subplots()
    ax.scatter(df['Date'], df['Solar Energy'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Solar Energy in KWh')
    ax.set_title('Solar Energy vs time')
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()

    SEtime_plot = Markup('<img src="data:image/png;base64,{}">'.format(img_b64))
    plt.close()
    
    fig, ax = plt.subplots()
    ax.scatter(df['Date'], df['wind Energy'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Wind Energy in KWh')
    ax.set_title('Wind Energy vs time')
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()

    WEtime_plot = Markup('<img src="data:image/png;base64,{}">'.format(img_b64))
    plt.close()  
    # email=request.POST("email")
    # send_siler(email)
    # if(send_silver):
    #     return render_template('xe')
    # else:
    #     return  koi http response ya fr template   


    return render_template('inner-page.html',SE_plot = SE_plot,WE_plot = WE_plot,WS2M_plot = WS2M_plot,WS10M_plot = WS10M_plot,WS50M_plot = WS50M_plot,SKY_plot=SKY_plot,SEtime_plot=SEtime_plot,WEtime_plot=WEtime_plot)
if __name__=="__main__":
    app.run(debug=True) 