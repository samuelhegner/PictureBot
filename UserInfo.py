import time
import timedelta

class UserInfo:
    def __init__(self, userName, timeStamp, allTime, year, month, week, streak):
        self.userName = userName
        self.timeStamp = timeStamp
        self.allTime = allTime
        self.year = year
        self.month = month
        self.week = week
        self.streak = streak

    def addPost(self): #add to alltime, yearly, monthly and weekly stats
        self.timeStamp = int(time.time())
        self.allTime += 1
        self.year += 1
        self.month += 1
        self.week += 1
        self.setStreak(1)

    def setStreak(self, toAdd): #set the streak
        self.streak += toAdd #temp add, actual code to come!!
        
    def postedToday(self): #bool to check if the user posted this day
        dayAgo = time.time - timedelta(hours=24)
        return (dayAgo <= self.timeStamp <= time.time)

    def printUserInfo(self):
        print(self.__dict__)