import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
    
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    The following cleaning needs to be done:
    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    df = pd.read_csv('university_towns.txt', sep = '\t', header = None, names = ['State', 'RegionName'])
    df['State'] = df['State'].str.split(r'\(').str[0]
    df['State'] = df['State'].str.split(r'\[').str[0]
    
    for index, state in enumerate(df['State']):
        if state in states.values():
            df['State'].iloc[index] = state
        else:
            df['RegionName'].iloc[index] = state
            df['State'].iloc[index] = np.nan
    df['State'] = df['State'].fillna(method = 'ffill')
    df['RegionName'] = df['RegionName'].str.split(r'\s+$').str[0]
    
    df = df.dropna()
    df.reset_index(inplace = True)    
    df.drop('index', axis = 1, inplace = True)
    
    return df

get_list_of_university_towns()

def get_recession_start():
    
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3
    A recession is defined as starting with 
    two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
    q(n) > q(n+1) > q(n+2) < q(n+3) < q(n+4)
    '''
    
    df = pd.read_excel('gdplev.xls', parse_cols = 'E,G', skiprows = 219)
    df.columns = ['Quarter', 'GDP']
    
    for i, value in enumerate(df['GDP'][:-5]): 
        if (
            (value > df['GDP'].iloc[i + 1]) 
            and (df['GDP'].iloc[i + 1] > df['GDP'].iloc[i + 2]) 
            and (df['GDP'].iloc[i + 2] > df['GDP'].iloc[i + 3])
            and (df['GDP'].iloc[i + 3] < df['GDP'].iloc[i + 4])
            and (df['GDP'].iloc[i + 4] < df['GDP'].iloc[i + 5])
            ):
            recessionStarts = df[df['GDP'] == value]['Quarter'] 
    return recessionStarts.tolist()[0]

get_recession_start()

def get_recession_end():
    
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3
    A recession is defined as starting with 
    two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
    '''
    
    df = pd.read_excel('gdplev.xls', parse_cols = 'E,G', skiprows = 219)
    df.columns = ['Quarter', 'GDP']
    
    
    for i, value in enumerate(df['GDP'][:-5]):
        if (
            (value > df['GDP'].iloc[i + 1]) 
            and (df['GDP'].iloc[i + 1] > df['GDP'].iloc[i + 2]) 
            and (df['GDP'].iloc[i + 2] > df['GDP'].iloc[i + 3])
            and (df['GDP'].iloc[i + 3] < df['GDP'].iloc[i + 4])
            and (df['GDP'].iloc[i + 4] < df['GDP'].iloc[i + 5])
            ):
            recessionEnd = df[df['GDP'] == df['GDP'].iloc[i + 5]]['Quarter']
    return recessionEnd.tolist()[0]

get_recession_end()

def get_recession_bottom():
    
    df = pd.read_excel('gdplev.xls', parse_cols = 'E,G', skiprows = 219)
    df.columns = ['Quarter', 'GDP']
    for i, value in enumerate(df['GDP'][:-5]):
        if (
            (value > df['GDP'].iloc[i + 1]) 
            and (df['GDP'].iloc[i + 1] > df['GDP'].iloc[i + 2]) 
            and (df['GDP'].iloc[i + 2] > df['GDP'].iloc[i + 3])
            and (df['GDP'].iloc[i + 3] < df['GDP'].iloc[i + 4])
            and (df['GDP'].iloc[i + 4] < df['GDP'].iloc[i + 5])
            ):
            bottom = min(value, df['GDP'].iloc[i + 1], df['GDP'].iloc[i + 2], df['GDP'].iloc[i + 3], df['GDP'].iloc[i + 4])
            recessionBottom = df[df['GDP'] == bottom]['Quarter']
    return recessionBottom.tolist()[0]

get_recession_bottom()

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    keep = [1,2]
    for i in range(51, 251):
        keep.append(i)
    df = pd.read_csv('City_Zhvi_AllHomes.csv', sep = ',', usecols=keep)
    df['State'].replace(states, inplace = True) 
    df.set_index(['State', 'RegionName'], inplace = True)
    
    df_quarter = (df.groupby(pd.PeriodIndex(df.columns, freq='Q'), axis=1)
                  .mean()
                  .rename(columns=lambda c: str(c).lower()))
    return df_quarter

convert_housing_data_to_quarters()

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    start = '2008q2'
    bottom = '2009q2'
    end = '2009q4'

    uni_towns = get_list_of_university_towns()
    uni_towns['isUni'] = True
    house_prices = convert_housing_data_to_quarters()
    house_prices['ratio'] = ((house_prices[bottom] - house_prices[start])/house_prices[start])
    house_prices.reset_index(inplace = True)
    
    df = pd.merge(uni_towns, house_prices, how='outer', on = ['State', 'RegionName'])
    df['isUni'] = df['isUni'].fillna(False)
    
    u = df[df['isUni'] == True]
    nu = df[df['isUni'] == False]
    s, p = ttest_ind(u['ratio'],nu['ratio'],nan_policy = 'omit')
    
    different = True if p < 0.01 else False
    better = 'university town' if u['ratio'].mean() > nu['ratio'].mean() else 'non-university town'
    return (different, p, better)

run_ttest()




