import requests
import pymysql
from bs4 import BeautifulSoup
import queue
import time

conn = pymysql.connect(host='127.0.0.1',user='root',passwd='1234',db='recipe',charset='utf8')
cur = conn.cursor()

def storeIngredient(name,imageURL):
	ins = 'INSERT INTO ingredient(name,imageURL) VALUES(%s,%s)'
	cur.execute(ins,(name,imageURL))
	cur.connection.commit()

def storeFood(mainItem,subItem,kind,recipeURL):
	ins = 'INSERT INTO food(mainItem,subItem,kind,recipeURL) VALUES(%s,%s,%s,%s)'
	cur.execute(ins,(mainItem,subItem,kind,recipeURL))
	cur.connection.commit()

def isInserted(name):
    cur.execute('SELECT * FROM ingredient WHERE name = %s',(name))
    return cur.fetchone()

def getIdByName(name):
    cur.execute('SELECT id FROM ingredient WHERE name = %s',(name))
    return cur.fetchone()[0]

domain = 'http://www.10000recipe.com'
targetServer = '/recipe/list.html'
keywords = queue.Queue()
#keywords.put('레몬')
keywords.put('고등어')
keywords.put('연어')
while(True):
    try:
        keyword = keywords.get()
        print(keyword)
        if not isInserted(keyword):
            storeIngredient(keyword, None)
        mainItem = getIdByName(keyword)
        pageNum = 1
        while(True):
            try:
                print(pageNum)
                rep = requests.get(domain + targetServer, params={
                    'q' : keyword,
                    'order' : 'reco',
                    'page' : pageNum
                })
                bsObj = BeautifulSoup(rep.content,'html.parser',from_encoding='utf8')
                itemList = bsObj.find('div', {'class': 'row'}).findAll('a')
                for item in itemList:
                    try:
                        location = item.attrs['href']
                        itemRep = requests.get(domain + location)
                        itemBsObj = BeautifulSoup(itemRep.content, 'html.parser', from_encoding='utf8')
                        kind = itemBsObj.find('div', {'class': 'info_title'}).get_text().split('\u00B7')[0].strip()
                        ingredients = itemBsObj.find('div', {'class': 'ready_ingre3'}).findAll('li')
                        for ingredient in ingredients:
                            targetItem = ingredient.get_text()
                            targetItem = ' '.join(targetItem.split()).split(' ')[0]
                            #print(pageNum,targetItem)
                            if not isInserted(targetItem):
                                storeIngredient(targetItem, None)
                            subItem = getIdByName(targetItem)
                            #print(mainItem,subItem,kind)
                            print(pageNum,keyword,targetItem)
                            storeFood(mainItem,subItem,kind,domain+location)
                    except AttributeError as err:
                        print('[재료] 항목이 없는 아이템')
                        continue
                pageNum += 1
                #time.sleep(1)
            except requests.exceptions.ConnectionError as pageEND:
                print('키워드',keyword,'에 대한 크롤링이 종료되었습니다.')
                print(pageEND)
                break
    except queue.Empty as err:
        print('queue is empty')
        print(err)
        break