#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
from BeautifulSoup import BeautifulSoup
import datetime
from libsport import db,get_url_content

def newSportLookUp(floor=3,querydate=datetime.date.today()):
   FLOOR = {3:1,1:2}
   url = 'https://info2.ntu.edu.tw/facilities/PlaceGrd.aspx?nFlag=0&placeSeq=%d&dateLst=%s' \
         % (FLOOR[floor],querydate.strftime("%Y/%m/%d"))
   content = get_url_content(url)
   if content == '': return

   schedule = dict()
   content = re.sub("add_user.png'.*?onclick=([^>]*?)>","add_user.png' onclick=\"\g<1>\">",content)
   soup = BeautifulSoup( content )
   table = soup.findAll('table', id="ctl00_ContentPlaceHolder1_tab1")
   trs = table[0].findAll('tr')
   for i in xrange(len(trs)):
      tds = trs[i].findAll('td')
      for j in xrange(1,len(tds)):
         if i==0 and j>0:
            date = re.findall( '([0-9]*)/([0-9]*)' , str(tds[j]) )
            date = datetime.date(year=querydate.year,month=int(date[0][0]),day=int(date[0][1]))
            if (date-querydate).days > 30:
               date = date - datetime.timedelta(days=365)
            elif (date-querydate).days < -30:
               date = date + datetime.timedelta(days=365)
            schedule[j-1] = {'date':date}
         elif i>0:
            detailURL = re.findall( '(PlaceDetail.aspx?[^\']*)', str(tds[j]) )
            detailURL = ("https://info2.ntu.edu.tw/facilities/%s"%detailURL[0]) if len(detailURL)>0 else ''
            purchaseURL = re.findall( '(PlaceOrderFrm.aspx?[^\']*)', str(tds[j]) )
            purchaseURL = url if len(purchaseURL)>0 else ''
            #purchaseURL = ("https://info2.ntu.edu.tw/facilities/%s"%purchaseURL[0]) if len(purchaseURL)>0 else ''
            remain = re.findall( 'img.*14dot1b.gif[^\(]*\(([0-9]*)' , str(tds[j]) )
            remain = (int(remain[0]) if len(remain)>0 else 0 )
            used   = re.findall( 'img.*actn010_2.gif[^\(]*\(([0-9]*)' , str(tds[j]) )
            used   = (int(used[0]) if len(used)>0 else 0)
            text   = tds[j].getText()
            if remain+used == 0 and text=='' :
               text = '?' 
            elif remain+used > 0 :
               text = ''
            schedule[j-1][i+7] = remain,used,text,detailURL,purchaseURL
   return schedule


def oldSportLookUp(querydate=datetime.date.today()):
   url = "http://ntusportscenter.ntu.edu.tw/ntu/front/order.aspx?d=y&acp2id=27&yearno=%s&monthno=%s&dayno=%s"\
         % (querydate.strftime("%Y"),querydate.strftime("%m"),querydate.strftime("%d"))
   schedule = dict()
   content = get_url_content(url)
   if content == '': return
   soup = BeautifulSoup( content )
   table = soup.find('table', id="cal")
   if not table:
      print "Error"
      return
   trs = table.findAll('tr')
   for i in xrange(len(trs)):
      tds = trs[i].findAll('td')
      for j in xrange(1,len(tds)):
         if i==0 and j>0:
            date = re.findall( '([0-9]*)/([0-9]*)' , str(tds[j]) )
            date = datetime.date(year=querydate.year,month=int(date[0][0]),day=int(date[0][1]))
            if (date-querydate).days > 30:
               date = date - datetime.timedelta(days=365)
            elif (date-querydate).days < -30:
               date = date + datetime.timedelta(days=365)
            schedule[j-1] = {'date':date}
         elif i>0:
            text = tds[j].getText().strip()
            detailURL = re.findall( '(showact.aspx?[^\']*)', str(tds[j]) )
            detailURL = ("http://ntusportscenter.ntu.edu.tw/ntu/front/%s"%detailURL[0]) if len(detailURL)>0 else ''
            schedule[j-1][i-1] = text,detailURL
   return schedule


#def sportDetailLookUp(entity):
#   url = "https://info2.ntu.edu.tw/facilities/PlaceDetail.aspx?placeSeq=%d&bookDate=%s&beginHour=%d&endHour=%d&orderTotal=0&orderNum=0&orderNum2=0" %(entity['place'],entity['date'],entity['time'],entity['time']+1)
#   content = get_url_content(url)
#   soup = BeautifulSoup(content)
#   soup.find(id='lblOrderNum4')
#   GridView1 = soup.find(id='GridView1')
#   GridView2 = soup.find(id='GridView2')
#   GridView3 = soup.find(id='GridView3')
#
#   lbd = lambda a: a.get('id','').find('GridView1')

#querydate = datetime.date(year=2013,month=2,day=19)
if __name__ == "__main__":
   today = datetime.datetime.today()
   db.update( {'update':0} , {'update':0,'savetime':today.strftime("%Y/%m/%d %H:%M:%S")}, True )
   for floor in [1,3,-1]:
      print "#%s" % {-1:"Old",3:"New 3",1:"New 1"}[floor]
      for i in xrange(0,3):
         querydate = today + datetime.timedelta(days=7*i)
         # New Sport
         if floor>0:
            schedule = newSportLookUp(floor=floor,querydate=querydate.date())
            if not schedule:
               continue;
            for d in schedule.values():
               print d['date'],'\t',
               for i in range(8,22):
                  if d[i][0]+d[i][1] == 0 :
                     print d[i][2],"\t",
                  else:
                     print "%d/%d" %(d[i][1],(d[i][0]+d[i][1])) ,"\t",
                  ent={'date':d['date'].strftime("%Y/%m/%d"),
                     'time':i,
                     'remain':d[i][0],
                     'used':d[i][1],
                     'text':d[i][2],
                     'place':'New %d'%floor,
                     'savetime':today.strftime('%Y/%m/%d %H:%M:%S'),
                     'detailURL':d[i][3].replace("&amp;","&"),
                     'purchaseURL':d[i][4]}
                  db.update( {'date':d['date'].strftime("%Y/%m/%d"), 'time':i, 'place':'New %d'%floor},
                        ent, True )
                  print ent
               print ''
         # Old Sport
         else:
            schedule2 = oldSportLookUp(querydate=querydate.date())
            if schedule2 == None : continue
            for d in schedule2.values():
               print d['date'],'\t',
               for i, val in enumerate([8,10,12,13,15,17,18,20]):
                  print d
                  ent={'date':d['date'].strftime("%Y/%m/%d"),
                     'time':val,
                     'text':d[i][0],
                     'abbr':d[i][0].decode('UTF8')[:4],
                     'place':'Old',
                     'savetime':today.strftime('%Y/%m/%d %H:%M:%S'),
                     'detailURL':d[i][1].replace("&amp;","&")}
                  db.update( {'date':d['date'].strftime("%Y/%m/%d"), 'time':val, 'place':'Old'},
                        ent, True )
                  print ent
                  
                  if val == 12:
                      continue
                  val = val + 1
                  print d
                  ent={'date':d['date'].strftime("%Y/%m/%d"),
                     'time':val,
                     'text':d[i][0],
                     'abbr':d[i][0].decode('UTF8')[:4],
                     'place':'Old',
                     'savetime':today.strftime('%Y/%m/%d %H:%M:%S'),
                     'detailURL':d[i][1].replace("&amp;","&")}
                  db.update( {'date':d['date'].strftime("%Y/%m/%d"), 'time':val, 'place':'Old'},
                        ent, True )
                  print ent

##########################
#map ={ 'A':0 , 'B':1 , 'C':2 , 'D':3 , 'E':4 , 'F':5 , 'G':6 , 'H':7 , 'I':8 , 'J':9 , 'K':10, 'L':11, 'M':12, 'N':13, 'O':14, 'P':15, 'Q':16, 'R':17, 'S':18, 'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 'Y':24, 'Z':25, 'a':26, 'b':27, 'c':28, 'd':29, 'e':30, 'f':31, 'g':32, 'h':33, 'i':34, 'j':35, 'k':36, 'l':37, 'm':38, 'n':39, 'o':40, 'p':41, 'q':42, 'r':43, 's':44, 't':45, 'u':46, 'v':47, 'w':48, 'x':49, 'y':50, 'z':51, '0':52, '1':53, '2':54, '3':55, '4':56, '5':57, '6':58, '7':59, '8':60, '9':61, '+':62, '/':63 }
#def decodeBase64(word):
#   strcat = lambda x,y: x + y
#   # to binary, concatenation
#   s = reduce(strcat, [ bin(map[c])[2:].zfill(6) for c in word ])
#   # split
#   word = [ s[8*i:8*i+8] for i in range(0,len(s)/8) ]
#   # to word
#   li = [ chr(int(x,2)) for x in word ]
#   return reduce(strcat,li[0:-1:2])
#
#
#rePattern = 'onclick=javascript:location.href=\'(PlaceOrderFrm.aspx\?buildingSeq=[^&]*&placeSeq=([^&]*)&dateLst=([^&]*)&sTime=([^&]*)&eTime=([^&]*)&section=[^&]*&date=([^&]*)&week=[^\']*)'
#
#result = re.findall( rePattern , content )
#
#for one in result:
#   url,placeSeq,dateLst,sTime,eTime,date = one
#   placeSeq = decodeBase64(placeSeq)
#   sTime = decodeBase64(sTime)
#   eTime = decodeBase64(eTime)
#   date = decodeBase64(date)
#   print one   
#   if date=='2012/12/19' and sTime=='19':
#      pass
#      #url = open
#
