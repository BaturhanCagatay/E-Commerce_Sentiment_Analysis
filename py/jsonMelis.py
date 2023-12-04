import requests
from bs4 import BeautifulSoup


URL ="https://www.trendyol.com/new-balance/kadin-spor-ayakkabi-mr530ema-nb-lifestyle-unisex-shoes-white-silver-p-368538249"
headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
page = requests.get(URL, headers=headers)
pageContent = BeautifulSoup(page.content, 'html.parser')

productName = pageContent.find('h1', class_="pr-new-br").getText()
print(productName)

price = pageContent.find('span', class_="prc-dsc").getText()
print(price)

commentSection = pageContent.find_all("div",attrs={"span ","comment-text"})
#comment = commentSection.find('p')

print(commentSection)


#comment = commentSection.find("p", class_=False).getText()

#print(comment)



