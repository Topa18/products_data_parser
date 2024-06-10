from bs4 import BeautifulSoup
import requests
import json
import csv
from pathlib import Path


url = "https://calorizator.ru/product/all"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36"
}

# req = requests.get(url, headers=headers)
# src = req.text

#print(src)


#Сохраняем код сайта в фале на компьютере


# with open("index_for_products.html", "w") as file:
#     file.write(src)


# Создание словаря с ссылками на все страницы таблицы и его запись в .json  


# with open("index_for_products.html") as file:
#     src = file.read()

# soup = BeautifulSoup(src, "lxml")

# last_page = soup.find("li", class_="pager-last").find("a").text

# all_pages_dict = {}

# for i in range(int(last_page)):
#     item_text = f"Номер_страницы_{i + 1}"
#     if i == 0:
#         item_href = url
#         all_pages_dict[item_text] = item_href
#     else:
#         item_href = url + f"?page={i}"
#         all_pages_dict[item_text] = item_href

# with open("all_pages_dict.json", "w") as file:
#     json.dump(all_pages_dict, file, indent=4, ensure_ascii=False)


# Создание парсера, сохраняющего файлы .csv и .json о КБЖУ продуктов


with open("all_pages_dict.json") as file:
    all_pages = json.load(file)

cwd_ = Path.cwd()
pages_qty = int(len(all_pages))
counter = pages_qty

for page_number, page_href in all_pages.items():
    print(f"Осталось итераций: {counter}")
    req = requests.get(url=page_href, headers=headers)
    src = req.text

    with open(f"data/{page_number}.html", 'w') as file:
        file.write(src)

    with open(f"data/{page_number}.html") as file:
        src = file.read()
    
    soup = BeautifulSoup(src, "lxml")

    table_head = soup.find(class_="view-content").find("tr").find_all("th")
    product = table_head[1].find("a").text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text
    kcal = table_head[5].text

    with open(f"data/{page_number}.csv", 'w', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow((product, proteins, fats, carbohydrates, kcal))
    
    data = soup.find(class_="view-content").find("tbody").find_all("tr")
    
    product_data_dict = []

    for item in data:
        product_data = item.find_all("td")
        title = product_data[1].find("a").text
        proteins = product_data[2].text
        fats = product_data[3].text
        carbohydrates = product_data[4].text
        kcal = product_data[5].text

        product_data_dict.append(
            {
                "Title": title,
                "proteins": proteins,
                "fats": fats,
                "carbohydrates": carbohydrates,
                "kcal": kcal
            }
        )

        with open(f"data/{page_number}.csv", 'a', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow((title, proteins, fats, carbohydrates, kcal))
    
    with open(f"data/{page_number}.json", 'a') as file:
            json.dump(product_data_dict, file, indent=4, ensure_ascii=False)
   
    print(f"Записана страница: {page_number}. Продолжается сбор данных...")
    
    counter -= 1        
    if counter == 0:
        print("Сбор данных завершен.")
        print("Данные сохранены в папку \"data\" в директории: " + str(cwd_))
        break