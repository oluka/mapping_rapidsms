import re
    
class Person(object):
    def __init__(self,  uniqueid=None,tags=None, weight=None, date=None):
        self.tags = tags
        self.uniqueid = uniqueid
        self.date = date
        self.weight = weight

class util(object):
   @staticmethod   
   def get_good_date(date):
        delimiters = r"[./\\-]+"
        Allsect=re.split(delimiters,date)            
        year = Allsect[2]
        day = Allsect[0]
        month = Allsect[1]         
        if len(year) < 4 : 
               year = "20%s" % year        
        if len(month) < 2:
               month = "0%s" % month
        if len(day) < 2:
               day = "0%s" % day         
        newdate = "%s-%s-%s" % (year,month,day )
        return newdate
        
