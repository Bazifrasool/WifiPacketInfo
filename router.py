import requests
import re
import time
from bs4 import BeautifulSoup
import sys
from operator import itemgetter

username_=sys.argv[1]
password_=sys.argv[2]
timetorun=int(sys.argv[3])
period = int(sys.argv[4])

def get_router_data(param):
    login_data = {
    'username': username_,
    'password': password_,
    'submit.htm?login.htm': 'Send'
    }


    with requests.Session() as s:
        try:
            url="http://192.168.1.1/login.cgi"
            r=s.post(url,data=login_data)
            wifi_client=s.get("http://192.168.1.1/wlstatbl.htm")
            dhcp_table=s.get("http://192.168.1.1/dhcptbl.htm")
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
    if param == 1:
        f = open("wifi_tab.html","w+")
        f.write(wifi_client.text)
        f.close()
    if param == 2:
        f = open("wifi_tab2.html","w+")
        f.write(wifi_client.text)
        f.close()
    f = open("dhcp_tab.html","w+")
    f.write(dhcp_table.text)
    f.close()

    
    
    if param == 1:
        soup = BeautifulSoup(open("wifi_tab.html"), features="html5lib")
    if param == 2:
        soup = BeautifulSoup(open("wifi_tab2.html"), features="html5lib")

    my_table = soup.findAll("tr",{'bgcolor':"#b7b7b7"})

    lst = []

    for each in my_table:
      
        lst.append(each.findAll("font"))
    final_list = []
    for each in lst :
        tmp=[]
        for every in each:
            tmp.append(every.text)
        final_list.append(tmp)
    return final_list



def read_dhcp():
    soup = BeautifulSoup(open("dhcp_tab.html"),features="html5lib")
    lst_of_devs = []
    my_table_2 = soup.findAll("td",{'bgcolor':"#b7b7b7"})
    for each in my_table_2:
        lst_of_devs.append(each.text)
    list_of_things= []
    for i,each in enumerate(lst_of_devs):
        if i%5 == 0 or i%5 == 1 or i%5 == 2:
            list_of_things.append(each)
    fin_list = []
    tmp = []
    for i in range(0,len(list_of_things)):
        if i>0 and i%3 == 0:
            fin_list.append(tmp)
            tmp = []
            tmp.append(list_of_things[i])
        else:
            tmp.append(list_of_things[i])
    return fin_list



def processlist(prev_lst,current_lst):
    i=0
    
    while i < len(prev_lst):
        j=0
        while j < len(prev_lst[0]):
            if j == 1 or j==2 :
                prev_lst[i][j] = (-int(prev_lst[i][j]) + int(current_lst[i][j]))*1.2   
            j+=1    
        i+=1
        
    return prev_lst

if timetorun<0:
    while True :
        prev_lst = get_router_data(1)
        time.sleep(period)
        current_lst =get_router_data(2)

        processed_list = processlist(prev_lst,current_lst)
        dhcp_list = read_dhcp()

        for i,each in enumerate(processed_list):
            mac_key = processed_list[i][0]
            for j,every in enumerate(dhcp_list):
                if dhcp_list[j][2]==mac_key and len(dhcp_list[j][0])>2 :
                    processed_list[i][0]=dhcp_list[j][0]
                    break

        processed_list = sorted(processed_list, key = itemgetter(1),reverse=True)            
        for each in processed_list:
            print(str(each[0])+"---Sending---"+ str(each[1])+"---Receiving---" + str(each[2]))
        print("\n\n")
else:
    for i in range(0,timetorun):
        prev_lst = get_router_data(1)
        time.sleep(period)
        current_lst =get_router_data(2)

        processed_list = processlist(prev_lst,current_lst)
        dhcp_list = read_dhcp()

        for i,each in enumerate(processed_list):
            mac_key = processed_list[i][0]
            for j,every in enumerate(dhcp_list):
                if dhcp_list[j][2]==mac_key and len(dhcp_list[j][0])>2 :
                    processed_list[i][0]=dhcp_list[j][0]
                    break

        processed_list = sorted(processed_list, key = itemgetter(1),reverse=True)                  
        for each in processed_list:
            print(str(each[0])+"\nSending---"+ str(each[1])+"\nReceiving---" + str(each[2]))
            print("\n\n")
        print("\n\n")