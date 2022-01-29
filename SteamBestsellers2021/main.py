from calendar import c
from re import S
from matplotlib.pyplot import legend
import pandas as pd
import plotly.express as px
from dataclasses import dataclass

@dataclass
class Chart:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.Data = dataframe
        self.SteamCategories = ['Platinum', 'Gold', 'Silver', 'Bronze']
        self.Titles = ['Games Monetization', 'Games Monetization in Categories', 'Release Date']
        self.Lables = ['Monetization', 'Number of Games', 'Release Date']

    def create_chart_with_monetization(self):
        chart_df = pd.DataFrame(DataOperations(self.Data).count_values_for_monetization(), 
                                columns=['Type', 'Cnt'])

        fig = px.bar(chart_df, x=chart_df.columns[0], y=chart_df.columns[1], color='Type',
                    color_discrete_sequence=px.colors.qualitative.Antique,
                    title=self.Titles[0],
                    labels= {
                        'Type' : self.Lables[0],
                        'Cnt'  : self.Lables[1],
                    })

        fig.show()
    
    def create_chart_with_monetization_in_groups(self):
        cnt = []
        
        for category in self.SteamCategories:
            data = DataOperations(self.Data.loc[self.Data['Category'] == category])

            monetization_cnt = data.count_values_for_monetization()

            cnt.extend(data.create_record_for_group(category, monetization_cnt))

        chart_df = pd.DataFrame(cnt, columns=['Category', 'Type', 'Cnt'])

        fig = px.bar(chart_df, x='Type', y='Cnt', facet_col='Category', color='Type',
                    title=self.Titles[1],
                    color_discrete_sequence=px.colors.qualitative.Antique,
                    labels= {
                        'Type' : self.Lables[0],
                        'Cnt'  : self.Lables[1],
                    })
        
        fig.show()
    
    def create_chart_with_premiere_date(self):
        chart_df = DataOperations(self.Data).count_premieres_per_year()
    
        fig = px.bar(chart_df, x='Year', y='Cnt', color='Year',
                    color_discrete_sequence=px.colors.qualitative.Antique,
                    title=self.Titles[2],
                    labels= {
                        'Year' : self.Lables[2],
                        'Cnt' : self.Lables[1]
                    })
        fig.update_layout(showlegend=False)

        fig.show()

@dataclass
class DataOperations(Chart):
    def __init__(self, dataframe: pd.DataFrame) -> None:
        super().__init__(dataframe)
        self.MonetizationTypes = ['IAP', 'DLC', 'Standalone']

    def count_values_for_monetization(self):
        cnt = []

        for i in range(0, 2):
            cnt.append(len(self.Data.loc[self.Data[self.MonetizationTypes[i]] == 'Yes']))

        self.__count_standalone_games(cnt)
        return zip(self.MonetizationTypes, cnt)
    
    def create_record_for_group(self, category, data):
        records = []

        for element in data:
            record = (category, element[0], element[1])

            records.append(record)
        
        return records
    
    def count_premieres_per_year(self):
        data = pd.DataFrame(self.__get_year_from_date(), columns=['Year'])
        cnt = data.value_counts().reset_index()
        cnt.rename(columns = {0 : 'Cnt'}, inplace = True)

        return cnt.sort_values(by='Year', ascending = False)

    def __get_year_from_date(self):
        premiere_dates = []
        
        for date in self.Data['Steam Release date']:
            premiere_dates.append(date[6:])
        
        return premiere_dates
    
    def __count_standalone_games(self, cnt: list):
        cnt.append(len(self.Data.loc[(self.Data[self.MonetizationTypes[0]] == 'No') & (self.Data[self.MonetizationTypes[1]] == 'No')]))

def main():
    analysis = Chart(pd.read_csv('data.csv'))

    analysis.create_chart_with_monetization()
    analysis.create_chart_with_monetization_in_groups()
    analysis.create_chart_with_premiere_date()

if __name__ == '__main__':
    main()