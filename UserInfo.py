import Main as main


class UserInfo:

    @classmethod
    def createFromFile(cls, userName):
        row = main.dataframe.loc[main.dataframe['User'] == userName]
        timeStamp = "timeStamp"  # get timestamp from row
        allTime = 0  # get all time posts from row
        year = 0  # get yearly posts from row
        month = 0  # get monthy posts from row
        week = 0  # get weekly posts by
        streak = 0  # get streak from row
        return cls(userName, timeStamp, allTime, year, month, week, streak)

    @classmethod
    def createNew(cls, userName, timeStamp, allTime, year, month, week, streak):
        return cls(userName, timeStamp, allTime, year, month, week, streak)

    def __init__(self, userName, timeStamp, allTime, year, month, week, streak):
        self.userName = userName
        self.timeStamp = timeStamp
        self.allTime = allTime
        self.year = year
        self.month = month
        self.week = week
        self.streak = streak

    def writeToFile(self): #
        pass

    def addPost(self): #add to alltime, yearly, monthly and weekly stats
        pass

    def setStreak(self, postedToday): #set the streak, based on whether the used posted a picture today
        pass

    def postedToday(self): #bool to check if the user posted this day
        pass