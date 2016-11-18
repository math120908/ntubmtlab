#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from libsport import get_url_content,db
from IPython import embed

def parseWakeUp( content ):
   lines = content.split('\r')

   enable = {}
   for line in lines:
      for segment in re.findall( '\d+[^\(]*\([^\)]*\d+樓-\d+[^\)]*\)' , line ):
         print segment
         rlt = re.findall( '(\d+)樓-(\d+)' , segment )
         if len(rlt)>0:
            floor,nfield = int(rlt[0][0]),int(rlt[0][1])

            rlt=re.findall( '\d+/\d+' , segment )
            if len(rlt)==0:
               segment = "0/" + segment

            rlt=re.findall( '\d+/(\d+)' , segment )
            if len(rlt)>0:
               enable[int(rlt[0]),floor] = nfield 

            rlt=re.findall( '\d+/(\d+)[~-]\d+/(\d+)' , segment )
            if len(rlt)>0: 
               for i in xrange(int(rlt[0][0]),int(rlt[0][1])+1):
                  enable[i,floor] = nfield
            else:
               rlt=re.findall( '\d+/(\d+)[-~](\d+)' , segment )
               if len(rlt)>0: 
                  for i in xrange(int(rlt[0][0]),int(rlt[0][1])+1):
                     enable[i,floor] = nfield

            rlt=re.findall( '\d+/(\d+(、\d+)*)' , segment )
            if len(rlt)>0:
               for day in re.findall( '(\d+)', rlt[0][0] ):
                  enable[int(day),floor] = nfield

            rlt=re.findall( '\d+/(\d+(\.\d+)*)' , segment )
            if len(rlt)>0:
               for day in re.findall( '(\d+)', rlt[0][0] ):
                  enable[int(day),floor] = nfield

   return enable

if __name__ == "__main__":
   soup = BeautifulSoup(get_url_content('http://ntusportscenter.ntu.edu.tw/ntu/front/news.aspx'))
   lbd = lambda a: a.get('id','').find(u'DataList1_')!=-1 and a.text.find(u'晨間球場')!=-1
   for result in soup.findAll(lbd):
      url = re.findall( '(shownews.aspx.bid=[0-9]*)' , str(result) )
      url = "http://ntusportscenter.ntu.edu.tw/ntu/front/%s" %url[0]
      try:
          year,month = re.findall( u'([0-9]*)年([0-9]*)月' , result.text )[0]
      except:
          continue
      year = int(year); month = int(month)
      if year < 1000 : year+=1911
      #if month < datetime.today().month:
      #   continue
      ent={ 'date':'%s/%02d'%(year,month),
            'title':result.text.decode('UTF8'),
            'url':url,
            'savetime':datetime.today().strftime('%Y/%m/%d %H:%M:%S'),
            'place':'wakeup' }
      db.update({'date':'%s/%02d'%(year,month)}, ent, True)
      #print ent

      content = get_url_content(ent['url'])
      dateinfo = parseWakeUp( content )
      print sorted(dateinfo.items())
      for floor in [1,3]:
         for date in range(1,32):
            #print (date,floor)
            remain = dateinfo.get( (date,floor), 0 )
            text = '' if (date,floor) in dateinfo else '不開放'
            ent={'date':"%s/%02d/%02d"%(year,month,date),
                  'time':6,
                  'remain':remain,
                  'used':0,
                  'text':text,
                  'place':'New %d'%floor,
                  'savetime':datetime.today().strftime('%Y/%m/%d %H:%M:%S'),
                  'detailURL':url}
            db.update( {'date':"%s/%02d/%02d"%(year,month,date), 'time':6, 'place':'New %d'%floor},
                      ent, True )
            print ent


      #for enable in dateinfo:
      #   ent={'date':"%s/%02d/%02d"%(year,month,enable[0]),
      #         'time':6,
      #         'remain':enable[2],
      #         'used':0,
      #         'text':'',
      #         'place':'New %d'%enable[1],
      #         'savetime':datetime.today().strftime('%Y/%m/%d %H:%M:%S'),
      #         'detailURL':''}
      #   #db.update( {'date':d['date'].strftime("%Y/%m/%d"), 'time':i, 'place':'New %d'%floor},
      #   #      ent, True )
      #   print ent


