import requests, re, xlrd, xlwt
from bs4 import BeautifulSoup
import time, os.path, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import choice

# def get_proxy():
#     html = requests.get('https://free-proxy-list.net/').text
#     soup = BeautifulSoup(html, 'lxml')
#     trs = soup.find('table', id='proxylisttable').find_all('tr')[1:11]
#     proxies = []
#     for tr in trs:
#         tds = tr.find_all('td')
#         ip = tds[0].text.strip()
#         port = tds[1].text.strip()
#         schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
#         proxy = {'schema': schema, 'address': ip + ':' + port}
#         proxies.append(proxy)
#     mas = [1, 2, 3, 4, 5, 6, 7]
#     # time.sleep(choice(mas))
#     return choice(proxies)

def get_html(URL):
    open('useragents.txt').readlines()
    text = choice(open('useragents.txt').readlines())
    headers = {'User-Agent': text[:-2]}
    html = requests.get(URL, headers=headers)
    # print(html.text)
    return html.text


def get_ads(html):

    soup = BeautifulSoup(html, "lxml")
    link = soup.find_all('a', class_='link')

    if len(link)>=1:
        return link



def get_one_price(URL, i):
    try:
        open('useragents.txt').readlines()
        text = choice(open('useragents.txt').readlines())
        headers = {'User-Agent': text[:-2]}
        html = requests.get(URL, headers=headers).text
        soup = BeautifulSoup(html, "lxml")
        link = soup.find('div', class_='info-description').find('a').get('href')
        URL= 'https://hotline.ua' + link

        mas = [1, 2, 3, 4, 5, 6, 7]
        time.sleep(choice(mas))
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
        driver.get(URL)
        time.sleep(2)
        price = driver.find_element_by_xpath('//div[@class="auction-offers"]//span[@class="value"]').text
        centy = driver.find_element_by_xpath('//div[@class="auction-offers"]//span[@class="penny"]').text
        name_magaz = driver.find_element_by_xpath('//div[@class="auction-offers"]//a[@class="ellipsis"]').text
        write_file_xlsx(i, 2, str(price) + str(centy) )
        write_file_xlsx(i, 3, name_magaz)
        print(str(price) + str(centy), name_magaz)

        print('получили', price, centy, name_magaz)
    except:
        print('ошибка')


def get_price_value(URL, i):
    mas = [1, 2, 3, 4, 5, 6, 7]
    time.sleep(choice(mas))
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    driver.get(URL)

    time.sleep(2)
    price = driver.find_element_by_xpath('//div[@class="hidden viewbox all-offers"]//span[@class="value"]').text
    centy = driver.find_element_by_xpath('//div[@class="hidden viewbox all-offers"]//span[@class="penny"]').text
    name_magaz = driver.find_element_by_xpath('//div[@class="auction-offers"]//a[@class="ellipsis"]').text
    print(str(price) + str(centy), name_magaz)
    write_file_xlsx(i, 2, str(price) + str(centy))
    write_file_xlsx(i, 3, name_magaz)


def finf_name():
    try:
        rb = xlrd.open_workbook('price.xlsx')
        sheet = rb.sheet_by_index(0)
        vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
    except:
        input('Файл price.xlsx не найден !')
        sys.exit()
    global wb, ws
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Test')
    write_file_xlsx(0, 0, 'Артикул')
    write_file_xlsx(0, 1, 'Наименование')
    write_file_xlsx(0, 2, 'Цена hotline')
    write_file_xlsx(0, 3, 'Название магазина')
    write_file_xlsx(0, 4, 'Закупочная цена')
    write_file_xlsx(0, 5, 'Цена')
    write_file_xlsx(0, 6, 'Валюта')
    write_file_xlsx(0, 7, 'Ссылка на витрину')
    write_file_xlsx(0, 8, 'Ссылка на hotline')

    for i in range(1, len(vals)):
        try:
            name= vals[i][2]
            write_file_xlsx(i, 0, name)
            naimenovanie = vals[i][0]
            write_file_xlsx(i, 1, naimenovanie)
            zakup_price = vals[i][7]
            write_file_xlsx(i, 4, zakup_price)
            price_file = vals[i][4]
            write_file_xlsx(i, 5, price_file)
            valuta = vals[i][3]
            write_file_xlsx(i, 6, valuta)
            link_file = vals[i][18]
            write_file_xlsx(i, 7, link_file)
            print(name)
            URL = 'https://hotline.ua/sr/?q=' + str(name)
            write_file_xlsx(i, 8, URL)
            link_ads = get_ads(get_html(URL))
            # print(link_ads)
            link_ads = 'https://hotline.ua' + link_ads[0].get('href') + '#1/0'

            get_price_value(link_ads, i)
        except:
            get_one_price(URL, i)
    input('Готово!')
    sys.exit()

def write_file_xlsx(s, t, value, flag = False):


    ws.write(s, t, value)
    wb.save('hotline.xls')



def main():

    finf_name()
    # get_one_price('https://hotline.ua/sr/?q=WQ10-12G')






if __name__ == '__main__':
    main()
