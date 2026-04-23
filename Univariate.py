import pandas as pd
import numpy as np

class Univariate():
    def quanQual(self, dataset):
        quan=[]
        qual=[]
        
        for columnName in dataset.columns:
            # print(columnName)
            if (dataset[columnName].dtype=='O'):
                    # print("qual")
                qual.append(columnName)
            else:
                    # print("quan")
                quan.append(columnName)
        return quan,qual

    
    def freqTable(self, columnName, dataset):
        freqTable=pd.DataFrame(columns=["Unique_Values", "Frequency", "Relative_Frequency", "CumSum"])
        freqTable["Unique_Values"]=dataset[columnName].value_counts().index
        freqTable["Frequency"]=dataset[columnName].value_counts().values
        freqTable["Relative_Frequency"]=(freqTable["Frequency"]/103)
        freqTable["CumSum"]=freqTable["Relative_Frequency"].cumsum()
        return freqTable

    
    
    def Univariate(self, quan, dataset):
        descriptive=pd.DataFrame(index=["Null_count", "NonNull_count","Total_count","Mean", "Median", "Mode", "Q1:25%", "Q2:50%", 
                                    "Q3:75%", "99%", "Q4:100%", "IQR", "1.5rule", "Lesser", "Greater", "Min", "Max",
                                       "kurtosis", "skew", "var", "std"], columns=quan)
        for columnName in quan:
            descriptive[columnName]["Null_count"]=dataset[columnName].isnull().sum()
            descriptive[columnName]["NonNull_count"]=dataset[columnName].count()
            descriptive[columnName]["Total_count"]=len(dataset[columnName])
            descriptive[columnName]["Mean"]=dataset[columnName].mean()
            descriptive[columnName]["Median"]=dataset[columnName].median()
            descriptive[columnName]["Mode"]=dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"]=dataset.describe()[columnName]["25%"]
            descriptive[columnName]["Q2:50%"]=dataset.describe()[columnName]["50%"]
            descriptive[columnName]["Q3:75%"]=dataset.describe()[columnName]["75%"]
            descriptive[columnName]["99%"]=np.percentile(dataset[columnName],99)
            descriptive[columnName]["Q4:100%"]=dataset.describe()[columnName]["max"]
            descriptive[columnName]["IQR"]=descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5rule"]=1.5*descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"]=descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Greater"]=descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Min"]=dataset[columnName].min()
            descriptive[columnName]["Max"]=dataset[columnName].max()
            descriptive[columnName]["kurtosis"]=dataset[columnName].kurtosis()
            descriptive[columnName]["skew"]=dataset[columnName].skew()
            descriptive[columnName]["var"]=dataset[columnName].var()
            descriptive[columnName]["std"]=dataset[columnName].std()
        return descriptive

    
    
    def outlier_columnNames(self, quan, descriptive):
        lesser=[]
        greater=[]
        
        for columnName in quan:
            if(descriptive[columnName]["Min"]<descriptive[columnName]["Lesser"]):
                lesser.append(columnName) 
            if(descriptive[columnName]["Max"]>descriptive[columnName]["Greater"]):
                greater.append(columnName)
        return lesser, greater

    
    
    def replacing_outlier(self, dataset, lesser, greater, descriptive):
        for columnName in lesser:
            dataset.loc[dataset[columnName] < descriptive[columnName]["Lesser"], columnName] = descriptive[columnName]["Lesser"]
        for columnName in greater:
            dataset.loc[dataset[columnName] > descriptive[columnName]["Greater"], columnName] = descriptive[columnName]["Greater"]
        return dataset