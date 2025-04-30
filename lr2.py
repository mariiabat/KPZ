import pandas as pd 
from pandas import DataFrame 
from datetime import datetime as dt 
try:
    data_frame = pd.read_csv('lr2.csv')
except FileNotFoundError:
    columns = ['years', 'month', 'day', 'hour', 'minute', 'second']
    data_frame = DataFrame(columns=['years', 'month', 'day', 'hour', 'minute', 'second'])
current_time = dt.now()
new_row = pd.DataFrame({'years': [current_time.year],'month': [current_time.month],'day': [current_time.day],'hour': [current_time.hour],'minute': [current_time.minute],'second': [current_time.second]})
data_frame = pd.concat([data_frame,new_row], ignore_index=True)
data_frame.to_csv("lr2.csv")
