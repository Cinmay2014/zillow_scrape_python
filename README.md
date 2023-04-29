# Introduction

I made some changes based on the Yulan-Fang's version that I forked from and now you can monitor multiple cities you interested in and get scheduled email everyday.
If you also want to use Gmail, you can go to your Gmail [account setting -> Security] to find the [App passwords] in section [Signing to Google]. 
You can create a 16 digits password for your code.

Changes I made:
1. add city_name as the parameter of sendinfo() function (line 13-14)
2. simplify the url get code(line 18)
3. simplify the data_list part code(line 31 -35)
4. specify the send time as H:M:S, for example, 12:30:23
5. include the while loop in time_send() function and add last_send_time to check if the last email was sent 10 hours ago or hasn't been sent yet,
you can change the duration as you wish.(line 109 - 125)
6. add city names in a list that let you can monitor multiple cities you interested in.(line 129)

Simply change the cities and run the code you will get the results, each city will get an email.

Email format just as before.
<img src="https://github.com/Yulan-Fang/zillow_scrape_python/blob/master/WechatIMG61.png" width="530"  height="1150">
