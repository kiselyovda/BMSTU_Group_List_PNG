import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from time import sleep


def replace(string):
    rep = [" "]
    for item in rep:
        if item in string:
            string = string.replace(item, "")
    return string


def get_data(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) /"
                      "Chrome/88.0.4324.182 YaBrowser/21.2.4.165 Yowser/2.5 Safari/537.36"
    }
    req = requests.get(url, headers)

    # with open("index.html", "w", encoding="utf-8") as file:
    #     file.write(req.text)
    #
    # with open("index.html", encoding="utf-8") as file:
    #     src = file.read()

    soup = BeautifulSoup(req.text, "lxml")
    groups = soup.find_all("a", class_="btn-primary")
    # print(groups)
    groups_dict = {}
    for group in groups:
        group_name = group.text.strip()
        group_index = "https://lks.bmstu.ru" + group.get('href').strip()

        groups_dict[group_name] = group_index
    name = replace(input("Введите номер группы:").upper())
    while True:
        if name not in groups_dict:
            name = replace(input("Ошибка! Введите группу заново:").upper())

        else:
            print(f"Группа {name} обнаружена.\nНачинаю вывод данных!")
            options = webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(options=options)
            driver.get(f"{groups_dict[name]}")

            # S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
            driver.set_window_size(1080, 1450)
            driver.find_element_by_tag_name('body').screenshot(f'{name}.png')
            driver.quit()

            print("Задача выполнена!")

            os.replace(f"{name}.png", f"bam/{name}.png")
            os.startfile(f"C:/Users/Даниил/OneDrive/Документы/Python Projects/BMSTU_Group_List_PNG/BMSTU List Pars/bam/{name}.png")

            break
    while True:
        ask = input("Удалить файл (да/нет)?: ").lower()
        if ask == "да":
            print("Удаляю файл...")
            os.remove(f"bam/{name}.png")
            print(f"\nФайла {name}.png не осталось")
            break
        elif ask == "нет":
            print(f"OK...\nФайл {name}.png находится в папке bam")
            break
        else:
            print("Команда введена не верна. Попробуйте еще раз.")


def main():
    get_data("https://lks.bmstu.ru/schedule/list")


if __name__ == '__main__':
    main()
