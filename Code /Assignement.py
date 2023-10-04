'''
Web Scrapping
This project focuses on scrapping the reviews of Chip Reverse Mortgage from Trustpilot.com
It would create a CSV of the scrapped reviews
The CSV would have 4 columns and 1,183 rows
The columns are Company Name, Date Published, Rating value and Review body
The rows are each review documented about the company

'''
#import libraries
import requests
from bs4 import BeautifulSoup as soup
import csv
import pandas as pd
from datetime import datetime


#create a list for all columns 

Reviews = []

for num in range(1,59):
    source = requests.get(f'https://ca.trustpilot.com/review/chip.ca?page={num}')
        #convert the webpage to a beautiful soup object 
    webpage = soup(source.content, features="html.parser")

    for article in webpage.find_all(class_="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_reviewCard__hcAvl"):
        pub_date = article.find(class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_datesWrapper__RCEKH")
        time_element = pub_date.find('time')
        if time_element:
            raw_datetime = time_element['datetime']
            input_datetime_str = datetime.strptime(raw_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")
            pub_datetime = input_datetime_str.strftime("%A, %B %d, %Y at %I:%M:%S %p")
            
        
        compname = webpage.find(class_="typography_display-s__qOjh6 typography_appearance-default__AAY17 title_displayName__TtDDM")
        compname = compname.text.strip()
        

        rate = article.find(class_="star-rating_starRating__4rrcf star-rating_medium__iN6Ty")
        image_element = rate.find('img')
        if image_element:
            gen_rate = image_element['alt']
            words = gen_rate.split()
            if words[0].lower() == 'rated' and words[1].isdigit():
                Rate_num = int(words[1])

        review = article.find(class_="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn")
        if review is None:
            review_text = None
        else:
            review_text = review.text.strip()
        

        Reviews.append([compname,pub_datetime,Rate_num,review_text])


df= pd.DataFrame(Reviews,columns=['CompanyName','DatePublished','RatingValue','ReviewBody'])
df.to_csv('/Users/lumi/Downloads/Reveiws.csv')

