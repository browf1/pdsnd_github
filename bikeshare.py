import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!\n')
    print("You will be asked to enter the city, month and day you would like to view data for.\n")
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    # create city, month and day variables as empty strings
    city = ""
    month = ""
    day = ""
    
    # while loop checks if the city variable is in a list of acceptable names converted to lower case
    while city.lower() not in ["chicago", "new york city", "washington"]:
        city = str(input("Enter a city (Chicago, New York City or Washington): ")).lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    
    # while loop checks if the month variable is in a list of acceptable names converted to lower case
    while month.lower() not in ["january", "february", "march", "april", "may", "june", "july", "august", "september",
                                "october", "november", "december", "all"]:
        month = str(input("\nEnter a month (e.g. January, February etc). If you would like to select all months, enter \'all'): ")).lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    # while loop checks if the day variable is in a list of acceptable names converted to lower case
    while day.lower() not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
        day = str(input("\nEnter a day of the week (e.g Monday, Tuesday etc). If you would like to select all days, enter \'all': ")).lower()

    print("\nYou have entered: \ncity - {}\nmonth - {}\nday - {}\n\n".format(city, month, day))
   
    print('-'*40)
                       
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
    
    # load data file for the chosen city into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    
    try:
        # filter by month if applicable
        if month != 'all':
            # use the index of the months list to get the corresponding int index value
            months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
            month = months.index(month)+1

            # filter by month to create the new dataframe
            df = df[df["month"] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df["day_of_week"] == day.title()]
    
        return df
    
    except ValueError:
        print('Value Error returned - exiting the program.')

### Creating a function to display raw data to the user

def display_data(df):
    """
    
    Displays raw data from the loaded csv file to the user.
    
    Args:
        (pandas dataframe) df - the dataframe to be displayed
    Returns:
        Rows of the df in the terminal
        
    """
    
    # creating variables to be used in the proceedig loops
    display_decision = ""
    row_index = 0
    # determining the number of rows in the dataframe
    df_size = df.shape

    # adding a condition so a user is not asked if they wish to view data if none exists
    if df.empty == True:
            print("No data to display with the chosen filter.")
            display_decision = "No"
    else:
        print("Data is available to display.\n")
        while display_decision.title() not in ["Yes", "No"]:
            display_decision = input("Would you like to view raw data? Enter 'Yes' or 'No':\n")
    
    # loop to print 5 more rows of data only if the user selected Yes and there are rows remaining to print
    while display_decision.title() == "Yes" and df_size[0] > row_index:
        print(df.iloc[row_index:row_index + 5])
        row_index += 5
        display_decision = str(input("Would you like to view more raw data? Enter 'Yes' or 'No':\n"))

           
            
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # create new columns converting the start time into hour
    df['start_hour'] = df['Start Time'].dt.hour
    
    # try and except in case an empty dataframe is returned
    try:
        # TO DO: display the most common month
        mode_month = df['month'].mode()[0]
        print("Most common month: ", mode_month)

        # TO DO: display the most common day of week
        mode_day = df['day_of_week'].mode()[0]
        print("\nMost common day: ", mode_day)

        # TO DO: display the most common start hour
        mode_hour = df['start_hour'].mode()[0]
        print("\nMost common hour: ", mode_hour)
        
    except IndexError:
        print("IndexError occurred.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # try and except in case an empty dataframe is returned
    try:
        # TO DO: display most commonly used start station
        mode_start_station = df['Start Station'].mode()[0]
        print("Most common start station: ", mode_start_station)

        # TO DO: display most commonly used end station
        mode_end_station = df['End Station'].mode()[0]
        print("Most common end station: ", mode_end_station)

        # TO DO: display most frequent combination of start station and end station trip
        # concatenating the start and end stations around ' and ' and determing the most common combination
        df['combined_stations'] = df['Start Station'] + ' and ' + df['End Station']
        combined_stations = df['combined_stations'].mode()[0]
        print("\nMost common start and end station combination: ", combined_stations)
    
    except IndexError:
        print("IndexError occurred, skipping this part of the program.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    
    try:
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # TO DO: display total travel time
        total_travel_duration = df['Trip Duration'].sum()
        print("\nTotal travel time = ", total_travel_duration)

        # TO DO: display mean travel time
        mean_travel = df['Trip Duration'].mean()
        print("\nMean travel time = ", mean_travel)

    except IndexError:
        print("IndexError occurred.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("\nCount of each user type:\n", user_type_count)

    # try and except in case the dataframe does not have the appropriate columns
    try:    
        # TO DO: Display counts of gender
        gender_count = df['Gender'].value_counts()
        print("\nCount of each gender:\n", gender_count)

        # TO DO: Display earliest, most recent, and most common year of birth
        birth_year_min = df["Birth Year"].min()
        birth_year_max = df["Birth Year"].max()
        birth_year_mode = df["Birth Year"].mode()
        print("\nEarliest birth year: ", birth_year_min)
        print("\nLatest birth year: ", birth_year_max)
        print("\nMost common birth year: ", birth_year_mode)
    
    except KeyError:
        print("A KeyError occurred. Skipping this part of the program.")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
