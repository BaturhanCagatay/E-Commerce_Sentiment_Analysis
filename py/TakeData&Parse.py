import requests
from bs4 import BeautifulSoup as bs
import csv

def scrape_comments(url, page_number,file_name):
    heading = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    page = requests.get(url, headers=heading)
    soup = bs(page.content, 'lxml')
    
    comments = soup.find_all('div', {'class': 'hermes-ReviewCard-module-KaU17BbDowCWcTZ9zzxw'})
    ratings = soup.find_all('div', {'class': 'hermes-RatingPointer-module-UefD0t2XvgGWsKdLkNoX'})

    if not comments:  
        print("No Comments Found")
        return False

    with open(file_name, "a+", encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file)
        for i, (comment, rating) in enumerate(zip(comments, ratings), start=1):
            full_comment_text = comment.text.strip()
            
            
            user_index = full_comment_text.find("Kullanıcı")
            if user_index != -1:
                comment_text = full_comment_text[:user_index].strip()
            else:
                comment_text = full_comment_text
            
             
            seller_index = full_comment_text.find("Kullanıcı")
            if seller_index != -1:
                parsed_comment_text = full_comment_text[seller_index + len("Kullanıcı"):].strip()
            else:
                parsed_comment_text = full_comment_text
            
            any_info = parsed_comment_text.find(".")
            if seller_index != -1:
                info_comment_text = parsed_comment_text[any_info + len("."):].strip()
            else:
                info_comment_text = parsed_comment_text
                
            star_elements = rating.find_all('div', class_='star')
            star_count = len(star_elements)
            writer.writerow([page_number, i, comment_text, star_count, parsed_comment_text])
            print(f"Page {page_number} / Comment {i}: Comment Text: {comment_text} / Number Of Stars: {star_count} / Seller Info: {parsed_comment_text} / Any Info: {info_comment_text}")
    
    return True

main_url = 'https://www.hepsiburada.com/philips-hd9243-90-3000-serisi-airfryer-large-rapid-air-teknolojisi-4-1l-p-hbcv00004ovgx2'
heading = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

page_number = 1
file_name = input("Enter the output file name (e.g., output_comments.csv): ")
previous_page_content = None

while True:
    page_url = main_url + f'?sayfa={page_number}'
    response = requests.get(page_url, headers=heading)

    if response.status_code == 200:
        current_page_content = response.content

        if previous_page_content and previous_page_content == current_page_content:
            print("No more comments found or reached a duplicate page. Stopping the process.")
            break

        previous_page_content = current_page_content

        success = scrape_comments(page_url, page_number,file_name)

        if not success:
            print("No more comments found. Stopping the process.")
            break

        page_number += 1
    else:
        print("Error fetching the page. Stopping the process.")
        break