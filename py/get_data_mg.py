import requests
import json
import csv


# csv file name
csv_filename = "comments.csv"

# url without page number
base_url = "https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/150059024?merchantId=844339&storefrontId=1&culture=tr-TR&order=5&searchValue=&onlySellerReviews=false&page="


# get page number
json_response = requests.get(base_url + "1")
json_data = json.loads(json_response.text)
total_pages = json_data["result"]["productReviews"]["totalPages"]

print("total pages: ", total_pages)

# write csv
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["Rate", "Seller", "Comment"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # visit every page
    for page_num in range(1, total_pages + 1):
        # get json data
        json_url = base_url + str(page_num)
        response = requests.get(json_url)

        #HTTP 200 OK success status
        if response.status_code == 200:
            data = json.loads(response.text)
            comments = data["result"]["productReviews"]["content"]

            for comment in comments:
                rate = comment["rate"]
                comment_text = comment["comment"]
                seller_name = comment["sellerName"]

                # write comment and its rate
                writer.writerow({"Rate": rate, "Seller": seller_name, "Comment": comment_text})
        else:
            print(f"Hata: Sayfa {page_num} alınamadı.")

