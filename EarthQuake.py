import pandas as pd
import logging
import calendar
import requests
import datetime
import os
import matplotlib.pyplot
import urllib.request
import json
from optparse import OptionParser


class EarthQuake():
    def __init__(self):
        self.readOpts()
        self.setLogging()
        self.TotalCount = 0
        #self.CountURL = "https://earthquake.usgs.gov/fdsnws/event/1/count?starttime=2016-01-01&endtime=2016-01-31"
        self.pageRequestURL = "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?"

    def readOpts(self):
        parser = OptionParser(usage='usage: %prog [options]')
        parser.add_option("-y", "--Year", dest="Year", help="Year")
        parser.add_option("-m", "--Month", dest="Month", help="Month")

        (options,args) = parser.parse_args()
        if not options.Year:
            parser.error("Please provide Year")
        else:
            options.Year = int(options.Year)

        if options.Month:
            options.Month = int(options.Month)

        self.options = options

        
    def setLogging(self):
        # create logger
        logFile = '%s\Earthquake_%s.log'%(os.getcwd(),datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        self.logger = logging.getLogger(logFile)            
        self.logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s',datefmt="%Y-%m-%d %H:%M:%S")

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)
        self.logger.info('Log file name : %s' %(logFile))
        
    def getData(self):
        queryStr = "starttime=%s&endtime=%s" %(self.startDate,self.endDate)
        URL = self.pageRequestURL + queryStr
        self.logger.info("Extracting data from %s" %(URL))

        response = urllib.request.urlopen(URL)
        data = json.loads(response.read())
        TotalCount = data['metadata']['count']
        self.TotalCount+=TotalCount
        
        if TotalCount>0:
            df = pd.json_normalize(data['features'])
            
            return df
        else:
            return pd.DataFrame()

    def processDatabyMonth(self):
        if not self.options.Month:
            self.logger.info("Started processing for Year : %s" % (self.options.Year))
            now = datetime.datetime.now()
            if self.options.Year==now.year:
                monthRng = now.month+1
            else:
                monthRng = 13
            
            for month in range(1,monthRng):
                self.getDate(self.options.Year,month)
                df = self.getData()
                #print(df.head(5))
                if month == 1:
                    if len(df) > 0:
                        self.df = df 
                else:
                    if len(df)> 0:
                        self.df = pd.concat([self.df, df])
                    
        else:
            self.logger.info("Started processing for Year : %s and Month %s" %(self.options.Year,self.options.Month))
            self.getDate(self.options.Year,self.options.Month)
            self.df = self.getData()
        
    def getDate(self,year,month):
        monthStr = ("0" + str(month))[-2:]
        self.startDate = "%s-%s-01" % (year,monthStr)
        self.endDate = "%s-%s-%s" %(year, monthStr, str(calendar.monthrange(year,month)[1]))

    def ChkDataFromDf(self):
        if len(self.df) == self.TotalCount:
            self.logger.info("Length of datframe matches with the count provided by URL")
            
    def Visualzation(self):
        print(self.df.head(10))
        #self.df is final dataframe
        pass

if __name__ == "__main__":
    obj = EarthQuake()
    obj.processDatabyMonth()
    obj.ChkDataFromDf()
    obj.logger.info("Total RecordCount : %s " %(str(obj.TotalCount)))
    obj.Visualzation()
    
