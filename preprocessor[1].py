def preprocess(data):
    import re
    import pandas as pd
    # Define the regular expression pattern to extract the date, time, AM/PM, and message
    pattern = r'(\d{1,2}/\d{1,2}/\d{2}(?:\d{2})?), (\d{1,2}:\d{2}) (AM|PM) - ([\s\S]*?(?=\n\d{1,2}/|\Z))'
   # Extract the date, time, AM/PM, and message using the regular expression pattern
    matches = re.findall(pattern, data) 
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(matches, columns=['date', 'time', 'AM/PM', 'message'])
    # Split the message column into two parts based on the presence of a colon (":")
    df[['name', 'message']] = df['message'].str.split(': ', n=1, expand=True)
    # Drop any rows where the name is missing (i.e., group notifications)
    df.dropna(subset=['name'], inplace=True)    
    # Combine the date and time columns into a single datetime column
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'] + ' ' + df['AM/PM'], format='%m/%d/%y %I:%M %p')  
    # Drop the separate date, time, and AM/PM columns
    df.drop(columns=['date', 'time', 'AM/PM'], inplace=True)   
    # Reorder the remaining columns
    df = df[['datetime', 'name', 'message']]    
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['month_name']=df['datetime'].dt.month_name()
    df['day'] = df['datetime'].dt.day
    df['day_name']=df['datetime'].dt.day_name()
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour ==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period']=period

    # Drop the datetime column
    df.drop(columns=['datetime'], inplace=True)
    # convert the message column to string
    df['message'] = df['message'].astype(str)

    return df


