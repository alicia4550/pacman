# Import pandas
import pandas as pd
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

class LevelData():

    def __init__(self):
        # Load the xlsx file
        excel_data = pd.read_excel(dir_path + "/LevelSpecs.xlsx", engine='openpyxl')
        # Read the values of the file in the dataframe
        self.data = pd.DataFrame(excel_data)
        # Print the content
        # print("The content of the file is:\n", self.data)

LevelData()