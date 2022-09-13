import requests
import random
import math
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

def loss(X,y,beta):
    '''
    temp_list = []
    for i in range(len(X)):
        left = y[i] * math.log(1 / (1 + math.exp(-sum([X[i][k]*beta[k] for k in range(len(beta))]))))
        right =  (1 - y[i]) * (1 - math.log(1 / (1 + math.exp(-sum([X[i][k]*beta[k] for k in range(len(beta))])))))
        temp_list.append(left + right)
    '''
    #'''
    temp_list = []
    for i in range(len(X)):
        left = (y[i]-1) * dot(X[i],beta)
        right =  math.log(1+math.exp(-dot(X[i],beta)))
        temp_list.append(left - right)
    #'''
    return -sum(temp_list)
    
def gradient_descent_algorithm(X,y,beta,eta):
    delta_beta = [0.0001 for i in range(len(beta))]
    
    partial_loss_list = []
    for i in range(len(beta)):
        temp_beta = []
        for j in range(len(beta)):
            if j == i:
                temp_beta.append(delta_beta[i])
            else:
                temp_beta.append(0)
        partial_loss_list.append((loss(X,y,[beta[k] + temp_beta[k] for k in range(len(beta))]) - loss(X,y,beta)) / delta_beta[i])
    # print("C(B)=", partial_loss_list)
    # print(partial_loss_list)
    new_beta = []
    for i in range(len(beta)):
        new_beta.append(beta[i] - eta * partial_loss_list[i])
    
    # print("loss=", loss(X,y,beta))
    return new_beta

def predict(beta,x):
    temp = 0
    temp += beta[0]
    for j in range(len(x)-1):
        temp += x[:][j] * beta[j+1]
    
    return 1/(1+math.exp(-temp))

def dot(x,y):
    temp = 0
    for i in range(len(x)):
        temp += x[i] * y[i]
    return temp
          
def get_data():
    # 取出此次資料
    url = "https://lol.moa.tw/WorldChampionship/year2021"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    # print(soup.prettify())
    
    li_tags = soup.find_all("li", class_="list-group-item")
    # print(li_tags)
    
    link_list = []
    for li_tag in li_tags:
        a_tag = li_tag.find("a")
        link_list.append(a_tag.get("href"))
    
    record_list = []
    progress = tqdm(total=len(link_list))
    for i in range(len(link_list)):
        url = link_list[i]
        html = requests.get("https://lol.moa.tw" + url)
        record_list.append(html)
        progress.update(1)
    progress.close()
        
    # print(record_list[0])
    
    '''
    [[[],[]],
     [[],[]],
     ...
     [[],[]],
     ]
    
    擊殺數
    死亡數
    助攻數
    kda
    金錢
    巴龍數
    小龍數
    放置守衛
    拆除守衛
    勝敗
    '''
    
    data = []
    for i in range(len(record_list)):
        list1 = []
        list2 = []
        soup = BeautifulSoup(record_list[i].text, "html.parser")
        div_tags = soup.find("div", class_="panel-body").find_all("div", class_="row text-center")
        
        # 擊殺數 死亡數 助攻數 kda
        info = div_tags[2].find_all("div", class_="col-xs-6")
        # print(info1[0].text)
        list1.append(int(re.search("(.+?)/",info[0].text).group(1)))
        list1.append(int(re.search("/(.+?)/",info[0].text).group(1)))
        list1.append(int(re.search(".+/(.+?) ",info[0].text).group(1)))
        list1.append(float(re.search("\((.+)\)",info[0].text).group(1)))
        # print(list1)
        
        # print(info1[1].text)
        list2.append(int(re.search("(.+?)/",info[1].text).group(1)))
        list2.append(int(re.search("/(.+?)/",info[1].text).group(1)))
        list2.append(int(re.search(".+/(.+?) ",info[1].text).group(1)))
        list2.append(float(re.search("\((.+)\)",info[1].text).group(1)))
        # print(list2)
        
        # 金錢 
        info = div_tags[3].find_all("div", class_="col-xs-6")
        # print(info[0].text)
        list1.append(float(re.search("\$(.+?)k",info[0].text).group(1)))
        # print(list1)
        
        # print(info[1].text)
        list2.append(float(re.search("\$(.+?)k",info[1].text).group(1)))
        # print(list2)
        
        # 巴龍 小龍
        info = div_tags[4].find_all("div", class_="col-xs-6")
        # print(info[0].text)
        list1.append(int(re.search("巴龍:\s(.+?)\s/",info[0].text).group(1)))
        list1.append(int(re.search("小龍:\s(.+?)\s/",info[0].text).group(1)))
        # print(list1)
        
        # print(info[1].text)
        list2.append(int(re.search("巴龍:\s(.+?)\s/",info[1].text).group(1)))
        list2.append(int(re.search("小龍:\s(.+?)\s/",info[1].text).group(1)))
        # print(list2)
        
        #放置守衛 拆除守衛
        tr_we_tags = soup.find("table", class_="table table-condensed summonerinfo").find_all("tr", class_="info")
        tr_you_tags = soup.find("table", class_="table table-condensed summonerinfo").find_all("tr", class_="danger")
        
        # 1
        temp_list = []
        for j in range(len(tr_we_tags)):
            td_tags = tr_we_tags[j].find_all("td")
            temp_list.append(int(re.search("(.+?)\(",td_tags[9].text).group(1)))
        list1.append(sum(temp_list))
        
        # 2
        temp_list = []
        for j in range(len(tr_we_tags)):
            td_tags = tr_you_tags[j].find_all("td")
            temp_list.append(int(re.search("\((.+?)\)",td_tags[9].text).group(1)))
        list1.append(sum(temp_list))
        
        # 3
        temp_list = []
        for j in range(len(tr_we_tags)):
            td_tags = tr_you_tags[j].find_all("td")
            temp_list.append(int(re.search("(.+?)\(",td_tags[9].text).group(1)))
        list2.append(sum(temp_list))
        
        # 4
        temp_list = []
        for j in range(len(tr_we_tags)):
            td_tags = tr_we_tags[j].find_all("td")
            temp_list.append(int(re.search("\((.+?)\)",td_tags[9].text).group(1)))
        list2.append(sum(temp_list))

        # 勝敗
        info = div_tags[1].find_all("div", class_="col-xs-6")
        if re.search("\((.+?)\)",info[0].text).group(1) == "勝":
            list1.append(1)
        else:
            list1.append(0)
        if re.search("\((.+?)\)",info[1].text).group(1) == "勝":
            list2.append(1)
        else:
            list2.append(0)
        
        # print(list1,list2)
        data.append([list1,list2])
    return data
        
def set_data(data):
    info = []
    for i in range(len(data)):
        temp_list = []
        # 擊殺數
        if data[i][0][0] >= data[i][1][0]:
            temp_list.append(1)
        else:
            temp_list.append(0)
        # 死亡數
        if data[i][0][1] <= data[i][1][1]:
            temp_list.append(1)
        else:
            temp_list.append(0)
        #  助攻數 kda
        if data[i][0][2] >= data[i][1][2]:
            temp_list.append(1)
        else:
            temp_list.append(0)
        #  助攻數 kda
        if data[i][0][3] >= data[i][1][3]:
            temp_list.append(1)
        else:
            temp_list.append(0)
        # 金錢 
        if data[i][0][4] >= data[i][1][4]:
            temp_list.append(1)
        else:
            temp_list.append(0)
        # 巴龍
        if data[i][0][5] >= data[i][1][5]:
            temp_list.append(1)
        else:
            temp_list.append(0)
        # 小龍 
        if data[i][0][6] >= data[i][1][6]:
            temp_list.append(1)
        else:
            temp_list.append(0)
        # 放置守衛
        if data[i][0][7] >= data[i][1][7]:
            temp_list.append(1)
        else:
            temp_list.append(0)
        # 拆除守衛
        if data[i][0][8] >= data[i][1][8]:
            temp_list.append(1)
        else:
            temp_list.append(0)
        # 勝敗
        temp_list.append(data[i][0][9])
        info.append(temp_list)
    
    # print(info)
    
    # 分割 train data (80%) / test data (20%)
    pos_list = list([i for i in range(len(info))])
    random.shuffle(pos_list)
    
    # 設定訓練資料
    train_lists = []
    for i in range(len(info) * 80 // 100):
        train_lists.append(info[pos_list[len(train_lists)-1]])

    # 設定測試資料
    test_lists = []
    for i in range((len(info) * 80) // 100, len(info)):
        test_lists.append(info[pos_list[len(test_lists)-1]])
        
    return train_lists, test_lists

loss_data = []
def training(train_lists, test_lists):
    # train
    X = [[1,v1,v2,v3,v4,v5,v6,v7,v8,v9] for v1,v2,v3,v4,v5,v6,v7,v8,v9,v10 in train_lists]
    y = [v10 for v1,v2,v3,v4,v5,v6,v7,v8,v9,v10 in train_lists]
    beta = [1,1,1,1,1,1,1,1,1,1]
    eta = 0.005
    interval_error = 0.0001
    need_update = True
    print("running...")
    while need_update:
        # print(loss(X, y, beta))
        loss_data.append(loss(X, y, beta))
        new_beta = gradient_descent_algorithm(X,y,beta,eta)
        need_update = False
        for i in range(len(beta)):
            if abs(new_beta[i] - beta[i]) > interval_error:
                need_update = True
                beta = new_beta.copy()
                break
    print("beta =", beta)
    
    # test
    correct_count = 0
    for i in range(len(test_lists)):
        if predict(beta,test_lists[i][:-1]) >= 0.5:
            if test_lists[i][2] == 1:
                correct_count += 1
        else:
            if test_lists[i][2] == 0:
                correct_count += 1
    # ans    
    print("Accuracy =", round(correct_count/len(test_lists) * 100, 1) , "%")
    return beta
   
def inspection():
    # 擊殺數/死亡數/助攻數/KDA/金錢/巴龍數/小龍數/放置守衛/拆除守衛
    test = []
    for dnum in range(512):
        bnum_str = format(dnum, 'b')
        bnum_list = list(bnum_str)
        for i in range(9 - len(bnum_list)):
            bnum_list.insert(0, "0")
            
        for i in range(len(bnum_list)):
            bnum_list[i] = int(bnum_list[i])
        test.append(bnum_list)
    
    ans = []
    for i in range(len(test)):
        ans.append([])
        ans[i].append(test[i])
        ans[i].append(round(predict(beta, test[i]) * 100, 1))
    
    
if __name__ == '__main__':
    data = get_data()
    train_lists, test_lists = set_data(data)
    beta = training(train_lists, test_lists)
    inspection()
    
    # 修改處
    test_data = [1,0,1,0,1,0,1,0,1] 
    print()
    print(str(test_data), ":", round(predict(beta, test_data) * 100, 1), "%", end=' ')
    if predict(beta, test_data) >= 0.5:
        print("勝")
    else:
        print("敗")
    
        

    
