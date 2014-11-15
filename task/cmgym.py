#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from libsport import getURLcontent,db
import subprocess
import xlrd

def parseCMgymMonSheet( sheet ):
   sheet.nrows sheet.ncols
   for crange in thesheet.merged_cells:
      rlo, rhi, clo, chi = crange
       for rowx in xrange(rlo, rhi):
          for colx in xrange(clo, chi):
             # cell (rlo, clo) (the top left one) will carry the data
               # and formatting info; the remainder will be recorded as
               # blank cells, but a renderer will apply the formatting info
               # for the top left cell (e.g. border, pattern) to all cells in
               # the range.

def parseCMgym( fname ):
   year = re.findall('gym_([0-9]*)',fname)[0]
   book = xlrd.open_workbook(fname,formatting_info=True)
   # check 課表
   sheet = book.sheet_by_name(u'課表')
   schedule = [ sh.col_values(2)[2+i*10:12+i*10] for i in range(5) ]
   # check 月活動
   for mon in range(1,12):
      shname = u'體%s-%d' %(year,mon)
      if shname in book.sheet_names():
         sheet = book.sheet_by_name(shname)
         parseCMgymMonSheet( sheet )

   #lines = content.split('\r')

   #enable = {}
   #for line in lines:
   #   for segment in re.findall( '\d+/\d+[^\(]*\([^\)]*\d+樓-\d+[^\)]*\)' , line ):
   #      rlt = re.findall( '(\d+)樓-(\d+)' , segment )
   #      if len(rlt)>0:
   #         print segment
   #         floor,nfield = int(rlt[0][0]),int(rlt[0][1])

   #         rlt=re.findall( '(\d+)/(\d+)' , segment )
   #         if len(rlt)>0:
   #            enable[int(rlt[0][1]),floor] = nfield 

   #         rlt=re.findall( '(\d+)/(\d+)-(\d+)' , segment )
   #         if len(rlt)>0: 
   #            for i in xrange(int(rlt[0][1]),int(rlt[0][2])+1):
   #               enable[i,floor] = nfield

   #         rlt=re.findall( '(\d+)/(\d+)~(\d+)' , segment )
   #         if len(rlt)>0: 
   #            for i in xrange(int(rlt[0][1]),int(rlt[0][2])+1):
   #               enable[i,floor] = nfield

   #         rlt=re.findall( '(\d+)/(\d+(、\d+)*)' , segment )
   #         if len(rlt)>0:
   #            for day in re.findall( '(\d+)', rlt[0][1] ):
   #               enable[int(day),floor] = nfield

   #         rlt=re.findall( '(\d+)/(\d+(\.\d+)*)' , segment )
   #         if len(rlt)>0:
   #            for day in re.findall( '(\d+)', rlt[0][1] ):
   #               enable[int(day),floor] = nfield

   #return enable

BASE_URL = 'http://www.mc.ntu.edu.tw/staff/studentaffair/area/'
if __name__ == "__main__":
   soup = BeautifulSoup(getURLcontent('http://www.mc.ntu.edu.tw/staff/studentaffair/area/area.htm'))
   lbd = lambda a: a.get('target','')=='main' and a.text.find('借用時間')!=-1
   for result in soup.findAll(lbd):
      fname = result.get('href')
      href = BASE_URL + fname 
      subprocess.check_call(["wget", "-O", fname, href]);

      parseCMgym(fname)

      #url = re.findall( '(shownews.aspx.bid=[0-9]*)' , str(result) )
      #url = "http://ntusportscenter.ntu.edu.tw/ntu/front/%s" %url[0]
      #year,month = re.findall( u'([0-9]*)年([0-9]*)月' , result.text )[0]
      #year = int(year); month = int(month)
      #if month < datetime.today().month:
      #   continue
      #ent={ 'date':'%s/%02d'%(year,month),
      #      'title':result.text.decode('UTF8'),
      #      'url':url,
      #      'savetime':datetime.today().strftime('%Y/%m/%d %H:%M:%S'),
      #      'place':'wakeup' }
      #db.update({'date':'%s/%02d'%(year,month)}, ent, True)
      ##print ent

      #content = getURLcontent(ent['url'])
      #dateinfo = parseWakeUp( content )
      #print dateinfo
      #for floor in [1,3]:
      #   for date in range(1,32):
      #      #print (date,floor)
      #      remain = dateinfo.get( (date,floor), 0 )
      #      text = '' if (date,floor) in dateinfo else '不開放'
      #      ent={'date':"%s/%02d/%02d"%(year,month,date),
      #            'time':6,
      #            'remain':remain,
      #            'used':0,
      #            'text':text,
      #            'place':'New %d'%floor,
      #            'savetime':datetime.today().strftime('%Y/%m/%d %H:%M:%S'),
      #            'detailURL':url}
      #      db.update( {'date':"%s/%02d/%02d"%(year,month,date), 'time':6, 'place':'New %d'%floor},
      #            ent, True )
      #      #print ent


      ##for enable in dateinfo:
      ##   ent={'date':"%s/%02d/%02d"%(year,month,enable[0]),
      ##         'time':6,
      ##         'remain':enable[2],
      ##         'used':0,
      ##         'text':'',
      ##         'place':'New %d'%enable[1],
      ##         'savetime':datetime.today().strftime('%Y/%m/%d %H:%M:%S'),
      ##         'detailURL':''}
      ##   #db.update( {'date':d['date'].strftime("%Y/%m/%d"), 'time':i, 'place':'New %d'%floor},
      ##   #      ent, True )
      ##   print ent



