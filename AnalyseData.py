from matplotlib.collections import BrokenBarHCollection
import pandas as pd


class Analyse:
    def __init__(self, path="dataset/Placement_Data.csv"):
        self.df = pd.read_csv(path)
        self.cleanData()

    def cleanData(self):
        self.df.drop(['sl_no', 'ssc_b', 'hsc_b'], axis=1, inplace=True)
        self.df['salary'].fillna(value=0, inplace=True)

    def getCategoryCount(self, name):
        return self.df.groupby(name).count()['salary']

    def getDataframe(self):
        return self.df

    def getPlacedDataframe(self):
        return self.df[self.df['status'] == 'Placed']
    
    def getNotPlacedDataframe(self):
        return self.df[self.df['status'] == 'Not Placed']

    def getPlacementByField(self):
        return self.df[self.df['status'] == 'Placed'].groupby('hsc_s').count()['salary'], self.df[self.df['status'] == 'Not Placed'].groupby('hsc_s').count()['salary']

    def getPlacementBySpec(self):
        return self.df[self.df['status'] == 'Placed'].groupby('specialisation').count()['salary'], self.df[self.df['status'] == 'Not Placed'].groupby('specialisation').count()['salary']

    def getExpPlaced(self, exp):
        return self.df[self.df['workex'] == exp].groupby('status').count()['salary']