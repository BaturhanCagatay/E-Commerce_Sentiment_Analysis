import requests
from bs4 import BeautifulSoup as bs
import csv

def scrape_comments(url, page_number):
    heading = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    page = requests.get(url, headers=heading)
    soup = bs(page.content, 'lxml')
    
    comments = soup.find_all('div', {'class': 'hermes-ReviewCard-module-KaU17BbDowCWcTZ9zzxw'})
    ratings = soup.find_all('div', {'class': 'hermes-RatingPointer-module-UefD0t2XvgGWsKdLkNoX'})

    if not comments:  
        return False

    with open("glasses_comments.csv", "a+", encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Page Number","Comment_ID", "Comment_Text", "Star_Count"])
        for i, (comment, rating) in enumerate(zip(comments, ratings), start=1):
            comment_text = comment.text.strip()
            star_elements = rating.find_all('div', class_='star')
            star_count = len(star_elements)
            writer.writerow([page_number, i, comment_text, star_count])
            print(f"Page {page_number} - Comment {i}: {comment_text} - Number Of Star: {star_count}")
    
    return True

main_url = 'https://www.hepsiburada.com/karaca-jungle-6-kisilik-kahve-fincani-takimi-80-ml-p-hbcv00000e1pa9-yorumlari'
heading = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

page_number = 1
while True:
    page_url = main_url + f'?sayfa={page_number}'
    response = requests.get(page_url, headers=heading)

    if response.status_code == 200:
        success = scrape_comments(page_url, page_number)
        if not success: 
            break
        page_number += 1
    else:
        break
    
    
    
