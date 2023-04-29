from pandas import DataFrame
import datetime
import os
import requests
import re
import json
import pandas as pd
import smtplib
import time
import warnings
from tabulate import tabulate
warnings.filterwarnings('ignore')
def sendinfo(city_name):
    city = f'{city_name}/'
    #just grabbing the first 10 pages

    base_url = 'https://www.zillow.com/homes/for_sale/'
    urls = [f'{base_url}{city}/{page}_p/' for page in range(1, 11)]

    
    
    #add headers in case you use chromedriver (captchas are no fun); namely used for chromedriver
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    with requests.Session() as s:
        data_list = []
        for url in urls:
            response = s.get(url, headers=req_headers)
            data = json.loads(re.search(r'!--(\{"queryState".*?)-->', response.text).group(1))
            data_list.append(data)

 
    
    df = pd.DataFrame()
    
    
    
    def make_frame(frame):
        for i in data_list:
            for item in i['cat1']['searchResults']['listResults']:
                ## Filter to only include listings with at least 3 bedrooms and at least 2 bathrooms
                if item['beds'] is not None and item['beds'] >= 3 and item['baths'] is not None and item['baths'] >= 2:
                    frame = frame.append(item, ignore_index=True)
        return frame
    df = make_frame(df)
        
    #drop cols
    df = df.drop('hdpData', 1) #remove this line to see a whole bunch of other random cols, in dict format
    
    #drop dupes
    df = df.drop_duplicates(subset='zpid', keep="last")
    
    #filters
    df['zestimate'] = df['zestimate'].fillna(0)
    df['best_deal'] = df['unformattedPrice'] - df['zestimate']
    
     # Sort the DataFrame by the 'beds' column
    #df = df.sort_values(by='beds', ascending=True)
    
    #df['price per unit area'] = df['unformattedPrice'] / df['area']
    df = df.sort_values(by='best_deal',ascending=True)
    
    #print('shape:', df.shape)
    #display(df[['id','address','beds','baths','area','price','zestimate','best_deal','hdpData','brokerName',]].head(20))

    data = df[['statusText','address','beds','baths','area','price','zestimate','best_deal','detailUrl']].head(30)
    print(tabulate(data, headers='keys', tablefmt='psql', showindex=False))
    
    gmail_user = '@gmail.com' # Your email account
    gmail_password = '' # Your email password
    sent_from = gmail_user
    to = ['@gmail.com'] # target email account
   
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    msg = MIMEMultipart()
    msg['Subject'] = f"{datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')} {city_name}"

    
    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(data.to_html())
    part1 = MIMEText(html, 'html')
    msg.attach(part1)
    
    
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, msg.as_string())
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)
    
    
def time_send():
    last_sent_time = None
    while True:
        current_time = datetime.datetime.now()
        
        # Check if the last email was sent 10 hours ago or hasn't been sent yet
        if (last_sent_time is None) or (current_time - last_sent_time).seconds == 10*60*60:
           
            for city in cities:
                print(city)
                sendinfo(city)  # You can directly use this function to test if you can send the email.
                
            last_sent_time = datetime.datetime.now()  # Update the last sent time
            time.sleep(5)  # Wait for 5 seconds before checking again
           
        else:
            time.sleep(60)  # Wait for 1 minute before checking the time again


# You can modify it to your cities
cities = ['malden','weston','andover','belmont']
time_send()


