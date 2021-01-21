import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA =  { 'Chicago': 'chicago.csv',
                  'New York City': 'new_york_city.csv',
                  'Washington': 'washington.csv' }
    
UserInputCityDict = {1: 'Chicago', 2: 'New York City' , 3: 'Washington'}
UserInputMonthDict = {'All': 'All', 'Jan': 'January', 'Feb': 'February', 
                          'Mar': 'March', 'Apr': 'April', 
                          'May': 'May', 'Jun': 'June'
                         }
UserInputDayDict = {'All': 'All','Mon': 'Monday', 'Tue': 'Tuesday' , 
                        'Wed': 'Wednesday',
                        'Thu': 'Thursday', 'Fri':'Friday', 
                        'Sat': 'Saturday', 'Sun': 'Sunday'}   

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week t1o filter by, or "all" to apply no day filter
    """       
#Get User input for city
    while True:  
         try:
             city_option = int(input("Please Enter '1' for Chicago[Default], '2' for New York City or '3' for Washington: "))
             break
         except ValueError:
             print('Sorry this is not a number. Please enter a valid number. I did not understand that.Please try again')
             continue           
                                                     
# get user input for month (all, jan, feb, ... december)
    while True:     
        try:   
            m_option = input("Please Enter 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun' or 'all'[Default]: ")
            break
        except ValueError:
          print('Sorry you typed {}, I did not understand that.Please try again'.format(m_option))
          continue 
          
# get user input for day of week (dow)(all, monday, tuesday, ... sunday)
    while True:
        try:            
            d_option = input("Please Enter 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' or 'all'[Default]: ")
            break
        except ValueError:
            print('Sorry you typed {}, I did not understand that.Please try again'.format(d_option))
            continue 
            
#Validate input    
    
    if  m_option in UserInputMonthDict:
#        print('Your Month of choice is {}'.format(UserInputMonthDict.get(m_option .title())))
        month = UserInputMonthDict.get( m_option .title())
    else:
        #Set it to a default
        month = 'All'   
    
    if d_option in UserInputDayDict:
#        print('Your Day of choice is {}'.format(UserInputDayDict.get(d_option.title())))
        day = UserInputDayDict.get(d_option.title())
    else:
        #Set it to a default
        day = 'All'   
       
    if city_option in UserInputCityDict:
 #       print('Your city of choice is {}'.format(UserInputCityDict.get(city_option)))
        city = UserInputCityDict.get(city_option)
    else:
        #Set it to a default
        city_option = 2 
        city = UserInputCityDict.get(city_option)
    
    #print("City: {}, Month: {}, Day: {}".format(city, month, day))
     
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    new_df = df.copy()
#    print('Before: ', df.size)
    #clean data - remove Nan
    new_df.dropna(subset=['Start Time','End Time'])
 
    # convert the Start Time column to datetime
    new_df['Start Time'] = pd.to_datetime(new_df['Start Time'])

    # create new date time columns from Start Time

    new_df['month'] = new_df['Start Time'].dt.month   
#    df['year'] = df['Start Time'].dt.year 
#    df['ST_Year'] = df['Start Time'].dt.strftime('%Y') 
    new_df['ST_Month'] = new_df['Start Time'].dt.strftime('%B')   
    new_df['Day_Of_Week'] = new_df['Start Time'].dt.strftime('%A') 

    
    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        new_df = new_df[new_df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        new_df = new_df[new_df['Day_Of_Week'] == day.title()]
#  print(df)

#    print('After: ', new_df.size)
  
    return new_df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    #1 Popular times of travel (i.e., occurs most often in the start time)

    most common month
    most common day of week
    most common hour of day
        
    """  

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month =  df['ST_Month'].mode()[0]
    print('Most popular Month:', popular_month)

    # display the most common day of week
    popular_dow =  df['Day_Of_Week'].mode()[0]
    print('Most popular day of week:', popular_dow)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    #2 Popular stations and trip
    #most common start station
    #most common end station
    #most common trip from start to end (i.e., most frequent combination of start station and end station)
    
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    
#    #clean data - remove Nan
    df.dropna(subset=['Start Station','End Station'])

    start_time = time.time()

    # display most commonly used start station
    popular_sstation = df['Start Station'].mode()[0]
    print('Most popular start station(s):',  popular_sstation)
    # display most commonly used end station
    popular_estation = df['End Station'].mode()[0]
    print('Most popular end station(s):',  popular_estation)

#Group & Count
    new_df  = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Number_Trips')   
#Sort & get largest count
    new_df = new_df.sort_values(by ='Number_Trips' , ascending=False).head(1)
#getvalues

    Start_Station = new_df['Start Station'].values[0]
    End_Station = new_df['End Station'].values[0]
    Num_Trips = new_df['Number_Trips'].values[0]
    print('Most frequent combination(s) with \'{} \' Trips'.format(Num_Trips))
    print('     From :',   Start_Station)
    print('       To :',   End_Station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    #3 Trip duration
    #total travel time
    #average travel time
    """
    
    print('\nCalculating Trip Duration...\n')
    

    start_time = time.time()

    # display total travel time
    Total_Time_Secs = df['Trip Duration'].sum()
    Total_Time_Simpler = datetime.timedelta(seconds = int(Total_Time_Secs))
    print('Total Travel Time (Days, HH:MM:SS): ', Total_Time_Simpler)

    # display mean travel time
    Mean_Time_Secs = df['Trip Duration'].mean()
    Mean_Time_Simpler = datetime.timedelta(seconds = int(Mean_Time_Secs))
    print('Mean Travel Time (Days, HH:MM:SS): ', Mean_Time_Simpler)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    
    """Displays statistics on bikeshare users.
    
    #4 User info

    counts of each user type
    counts of each gender (only available for NYC and Chicago)
    earliest, most recent, most common year of birth (only available for NYC and Chicago)
    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of User Types\n', format(df['User Type'].value_counts(dropna=False)))
   

    if  'Gender' in df.columns:
        # Display counts of gender
        print('\nBreakdown of Gender\n', format(df['Gender'].value_counts(dropna=False)))

#Group by clean data and remove nan, sort by start time and get most recent BY, do not assume order of csv

    if 'Birth Year' in df.columns:       
        print('\nEarliest Birth Year: {}'.format(int(df['Birth Year'].min())))     
        print('Common Birth Year: {}'.format((int(df['Birth Year'].mode()[0]))))       
        new_df = df.copy()
        new_df = new_df.dropna(subset=['Birth Year'])
        new_df = new_df.sort_values(by=['Start Time'],ascending=False).reset_index().head(1)
        print('Most recent Birth Year: ',  new_df['Birth Year'].to_numpy())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def view_five(df):
    #
    """Display 5 rows of aw data if user input = y/yes and restart program if user wishes
    
    If User Wishes to stop they press N
    
    
    """
        
        view_rawdata = input('Would you like to view 5 rows of individual trip data? Enter (y)es or (n)o[Default]: ').lower()
        start_loc = 0  
        
        while True:
            try:                            
                if ((view_rawdata in ( 'y', 'yes')) and (start_loc <= len(df))):
                    print(df.iloc[start_loc:start_loc+5])
                    start_loc += 5
                    view_rawdata = input('Do you wish to continue? (y) or (n) to discontinue: ').lower()                 
                elif (view_rawdata in ('n', 'no')):                                               
                    break
                else:
                    print('Sorry I did not understand that.')
                    view_rawdata = input('Do you wish to continue? (y) or (n) to discontinue: ').lower()         
            except ValueError:
                print('Sorry I did not understand that.')
                view_rawdata = input('Do you wish to continue? (y) or (n) to discontinue: ').lower()         
                continue
            except KeyError:
                break
            
        #restart program, if user wants
        
        restart = input('Would you like to rerun with varying parameters? Enter (y)es or (n)o[Default]: ')
        
        if restart.lower() != 'y':
            return


def main():

    print('\nWelcome to the Bikeshare statistics portal')
    
    while True:
        city, month, day = get_filters() 
        print('\n')
        print('-'*75)
        print('Calculating time stats for | City: {} | Month: {} | Day: {}'.format(city, month, day))
        #clean data defore data analysis
        print('-'*75)
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_five(df)
        


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
