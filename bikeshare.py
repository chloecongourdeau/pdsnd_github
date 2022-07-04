import time
import pandas as pd
import numpy as np
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_data_entry(prompt, valid_entries):
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()

        while user_input not in valid_entries :
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        return user_input

    except:
        print('Seems like there is an issue with your input')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Please select the location for which you wish to see data: Chicago, New York City or Washington\n '
    city = check_data_entry(prompt_cities, valid_cities)

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Please select the month for which you wish to see data. Alternatively you can select all:\n '
    month = check_data_entry(prompt_month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Please select a day of the week. Alternatively you can select all\n '
    day = check_data_entry(prompt_day, valid_days)

    # get user validation of inputs
    print('-'*70)
    valid_response = ['yes','restart']
    validation = input("Awesome! The filter you have selected are as follows\n City: {}\n Month: {}\n Day of Week: {}\nIf this is not correct please type 'restart', if you would like to proceed type 'yes'\n".format(city,month,day)).lower()
    response = check_data_entry(validation,valid_response)
    while validation != 'yes':
        city, month, day = get_filters()
        df = load_data(city, month, day)
        break
    print('-'*70)
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        months=['january','february','march','april','may','june']
        month = month.index(month)+1

    # filter by month to create the new dataframe
        df = df[df['month']==month]
    if day != 'all':
        df = df[df['day_of_week']==day.title()]
    return df
    city, month,day = get_filters()
    df=load_data(city,month,day)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()

    #df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    print('\nCalculating The Most Frequent Times of Travel...\n')

    # display the most common month
    commun_month = df['month'].mode()[0]
    print('Most popular Month:', commun_month)

    # display the most common day of week
    commun_day = df['day_of_week'].mode()[0]
    print('Most popular day of the week:', commun_day)

    # display the most common start hour
    commun_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:',commun_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    commun_start_station = df['Start Station'].mode()[0]
    print('Most Popular start station:{}'.format (commun_start_station))

    # display most commonly used end station
    commun_end_station = df['End Station'].mode()[0]
    print('Most Popular end station:{}'.format (commun_end_station))

    # display most frequent combination of start station and end station trip
    df['station_combination']= df['Start Station'] + ' -> ' + df['End Station']
    popular_station_combination = df['station_combination'].mode()[0]
    print('Most popular combination of stations:', popular_station_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time'
    sum_travel_time = df['Trip Duration'].sum() / 60 / 60
    print('total travel time:', round(sum_travel_time), 'hours')

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean() / 60
    print('average travel time:', round(avg_travel_time), 'minutes')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print('User Types:',user_count)

    # Display counts of gender
    if city.lower() != 'washington':
        gender_count = df['Gender'].value_counts()
        print('Gender count:',gender_count)
    else:
        print("Gender count:no data")

    # Display earliest, most recent, and most common year of birth
    if city.lower() != 'washington':
        birth_year = df['Birth Year']
        print('Earliest birth year:\n',int(birth_year.max()))
        print('Most recent birth year\n',int(birth_year.min()))
        print('Most common year of birth\n', int(birth_year.mode()))
    else:
        print("Gender count: no data")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    """Ask user to see raw data in chunks of 5 rows until user objects """
    start_loc = 0
    end_loc = 5
    #First 5 lines inquiry
    raw_input_query = input("would you like to see 5 rows of individual trip data?\n").lower()
    while raw_input_query.lower() != 'no':
        pd.set_option('display.max_columns',200)
        print(df.iloc[0:5])
        #Next 5 lines inquriy
        view_next_five = input("would you like to see the next 5 rows of data?\n").lower()
        while view_next_five.lower() != 'no':
            start_loc += 5
            end_loc += 5
            pd.set_option('display.max_columns',200)
            print(df.iloc[start_loc:end_loc])
            view_next_five = input("would you like to see the next 5 rows of data?\n").lower()
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
