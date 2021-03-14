import Main as main


class UserInfo:

    @classmethod
    def createFromFile(cls, userName):
        row = main.dataframe.loc[main.dataframe['User'] == userName]
        cls.name = userName
        cls.timeStamp = "timeStamp"  # get timestamp from row
        cls.allTime = 0  # get all time posts from row
        cls.year = 0  # get yearly posts from row
        cls.month = 0  # get monthy posts from row
        cls.week = 0  # get weekly posts by
        cls.streak = 0  # get streak from row

    @classmethod
    def createNew(cls, userName, timeStamp, allTime, year, month, week, streak):
        cls.name = userName
        cls.timeStamp = timeStamp
        cls.allTime = allTime
        cls.year = year
        cls.month = month
        cls.week = week
        cls.streak = streak

    def writeToFile(self):
        pass

    def addPost(self):
        pass

    def checkStreak(self):
        pass
