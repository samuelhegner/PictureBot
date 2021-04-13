from datetime import datetime, timedelta, time



class UserInfo:

    def __init__(self, userName, timeStamp, allTime, year, month, week, streak):
        self.userName = userName
        self.timeStamp = timeStamp
        self.allTime = allTime
        self.year = year
        self.month = month
        self.week = week
        self.streak = streak


    def addPost(self):  #add to alltime, yearly, monthly and weekly stats
        self.timeStamp = int(datetime.now().timestamp())
        self.allTime += 1
        self.year += 1
        self.month += 1
        self.week += 1
        self.addToStreak()


    def dailyCheck(self):  #reset the daily
        if self.postedToday():
            self.timeStamp = 0
            return
        else:
            self.takeFromStreak()
        self.timeStamp = 0 #sets the time stamp to 0, to allow for posting on turning of new day!



    def resetWeeklyStats(self):
        self.week = 0
    
    def resetMonthlyStats(self):
        self.month = 0

    def resetYearlyStats(self):
        self.year = 0


    def addToStreak(self):
        if self.streak < 0:
            self.streak = 0
        self.streak += 1
    

    def takeFromStreak(self):
        if self.streak > 0:
            self.streak = 0
        self.streak -= 1


    def postedToday(self):
        now = int(datetime.now().timestamp())
        postedHoursAgo =  int((now - self.timeStamp)/60/60)
        return postedHoursAgo < 24
    

    def printUserInfo(self):
        print(self.__dict__)
