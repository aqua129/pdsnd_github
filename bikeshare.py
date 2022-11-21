#start of program
import pandas as pd
import numpy as np
from collections import Counter

#Start of accessing data
CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}

def user_input():
    """asks user for input city, month and day"""

    print("\nHello, welcome to the Bikeshare Data.\n")

    city = input("Please enter a city you would like to filter by?\nChicago, New York City or Washington:\n")
    city = city.title()
    while (city != "Chicago") and (city != "New York City") and (city != "Washington"):
        city = input("Please enter a valid city. Chicago, New York City or Washington:\n")
        city = city.title()
    print("You entered: ", city)

    time_filter = input("\nWould you like to filter the data by month, day, both or not at all? Type 'none' for no filter:\n")

    while (time_filter != "month") and (time_filter != "day") and (time_filter != "both") and (time_filter != "none"):
        print("\nPlease enter a valid input\n")
        time_filter = input("Would you like to filter by month, day, both or not at all? Type 'none' for no filter:\n")

    #month filter
    while (time_filter == "month"):
        month = input("\nWhich month? January, February, March, April, May, or June?\n")
        month = month.title()
        while month not in ("January", "February", "March", "April", "May", "June"):
            month = input("Please enter a valid month. January, February, March, April, May, or June:\n")
            month = month.title()

            if month in ("January", "February", "March", "April", "May", "June"):
                day = "none"
                break
            day = "none"
            break
        if month in ("January", "February", "March", "April", "May", "June"):
            day = "none"
            break

    #day filter
    while (time_filter == "day"):
        day = input("\nWhich day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday?\n")
        day = day.title()
        while day not in ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"):
            day = input("\nPlease enter a valid day. Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday:\n")
            day = day.title()

            if day in ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"):
                month = "none"
                break
            month = "none"
            break
        if day in ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"):
            month = "none"
            break

    while time_filter == "both":
        month = input("\nWhich month? January, February, March, April, May, or June?\n")
        month = month.title()
        while month not in ("January", "February", "March", "April", "May", "June"):
            month = input("Please enter a valid month. January, February, March, April, May, or June:\n")
            month = month.title()
            if month in ("January", "February", "March", "April", "May", "June"):
                break
            #break
        if month in ("January", "February", "March", "April", "May", "June"):
            day = input("\nWhich day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday?\n")
            day = day.title()
            while day not in ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"):
                day = input("\nPlease enter a valid day. Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday:\n")
                day = day.title()
                if day in ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"):
                    break
                #break
            if day in ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"):
                break
            #break

    #no filter
    if time_filter == "none":
        day = "none"
        month = "none"

        print()
        print("No filter will be applied")

    return city, month, day
#End of city, day and month user input statements

def add_data(city, month, day):
    """
    loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of city to analyze
        (str) month - name of month to filter by, or 'none' for no filter
        (str) day - name of day to fillter by, or 'none for no filter
    Returns:
        df - Pandas dataframe containing city data filitered by month and day
    """
    #load data into dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert start time column to to_datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month/day/hr of week from Start Time to creat new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()#(locale = "English")
    df['hour'] = df['Start Time'].dt.hour

    #filter by month if applicable
    if month != "none":
        #use index of months list to get corresponding into
        months = ["January", "February", "March", "April", "May", "June"]
        month = months.index(month) + 1

        #filter by month to create new dataframe
        df = df[df['month'] == month]

    if day != "none":
        #filter by day of week to create new dataframe
        df = df[df["day_of_week"] == day.title()]
    return df

def popular_time_of_travel(df):
    """Calculates stats related to time"""

    mode_month = df['month'].mode()[0]
    mode_day = df['day_of_week'].mode()[0]
    mode_hour = df['hour'].mode()[0]

    print("\nMost popular month: ", mode_month)
    print("Most popular day of the week to travel: ", mode_day)
    print("Most popular hour to travel at: ", mode_hour)

def popular_station_and_trip(df):
    """Displays stats related to stations and trip duration"""

    #adapted common_route from following url to find .size()
    #https://www.geeksforgeeks.org/pandas-groupby-count-the-occurrences-of-each-combination/
    #adapted common_route to find ascending = False from following url
    #https://www.geeksforgeeks.org/sort-dataframe-according-to-row-frequency-in-pandas/

    mode_start_station = df["Start Station"].mode()[0]
    mode_end_station = df["End Station"].mode()[0]
    mode_common_trip = df.groupby(["Start Station", "End Station"]).size().reset_index(name = "Count").sort_values(["Count"], ascending = False)
    common_route = mode_common_trip.head(1)

    print("\nMost popular Starting Station is: ", mode_start_station)
    print("Most common End Station: ", mode_end_station)
    print("Most common route: \n", common_route)

def trip_duration(df):
    """Displays stats related to trip duration"""

    #adapted average_travel from following url
    #https://www.geeksforgeeks.org/find-average-list-python/#:~:text=In%20Python%20we%20can%20find,of%20elements%20in%20a%20list.

    total_travel = df["Trip Duration"].sum()
    average_travel = sum(df["Trip Duration"])/len(df["Trip Duration"])

    print("\nTotal travel time: ", total_travel)
    print("Average travel time: ", average_travel)

def user_info(df, city):
    """Displays stats related to stations and trip duration"""

    #adapted code for common_dob from following url to see how .astype() worked
    #https://stackoverflow.com/questions/51865367/cannot-convert-the-series-to-class-int

    #adapted code for earliest_birth and recent_birth from following url to see how min and max worked on lists
    #https://stackoverflow.com/questions/3499026/find-a-minimum-value-in-an-array-of-floats

    #used following url to learn counter and how to import it
    #https://stackabuse.com/count-number-of-word-occurrences-in-list-python/

    if city == "Chicago" or city == "New York City":
        df_gender_counts = Counter(df["Gender"])
        df_user_type_counts = Counter(df["User Type"])

        gender_female = df_gender_counts["Female"]
        gender_male = df_gender_counts["Male"]

        earliest_birth = min(df["Birth Year"].dropna())
        recent_birth = max(df["Birth Year"].dropna())
        common_dob = df["Birth Year"].dropna().astype(str).mode()[0]

        customer_count = df_user_type_counts["Customer"]
        subscriber_count = df_user_type_counts["Subscriber"]

        print("\nNumber of female users: ", gender_female)
        print("Number of male users: ", gender_male)
        print("Earliest birth year: ", earliest_birth)
        print("Most recent birth year: ", recent_birth)
        print("Most common birth year: ", common_dob)
        print("Number of Customers: ", customer_count)
        print("Number of Subscribers: ", subscriber_count)

    if city == "Washington":
        df_user_type_counts = Counter(df["User Type"])

        print("No gender or birth year data is available\n")

        customer_count = df_user_type_counts["Customer"]
        subscriber_count = df_user_type_counts["Subscriber"]

        print("\nNumber of Customers: ", customer_count)
        print("Number of Subscribers: ", subscriber_count)

def raw_data(df):
    """Asks user if they'd like to see raw data from the csv file"""
    row_num = 0
    while True:
        raw_data = input("Would you like to view raw data? Type 'Yes' for yes, 'No' for no.\n")
        raw_data = raw_data.title()
        if raw_data == "Yes":
            print(df.iloc[row_num : row_num + 5])
            row_num = row_num + 5
        elif raw_data == "No":
            break
        else:
            print("Please enter valid input\n")

#main function
def main():
    while True:
        city, month, day = user_input()
        df = add_data(city, month, day)

        popular_time_of_travel(df)
        popular_station_and_trip(df)
        trip_duration(df)
        user_info(df, city)
        raw_data(df)

        #restart program prompt
        restart_program = input("\nWould you like to start over? Type 'Yes' for yes or 'No' for no.\n").title()
        while restart_program not in ("Yes", "No"):
            restart_program = input("Please enter Yes or No. Would you like to start over?\n")
            restart_program = restart_program.title()
            if restart_program in ("Yes", "No"):
                break
        if restart_program == "No":
            break
        elif restart_program == "Yes":
            continue

if __name__ == "__main__":
        main()


#References
# https://stackoverflow.com/questions/60214194/error-in-reading-stock-data-datetimeproperties-object-has-no-attribute-week
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
# https://stackoverflow.com/questions/60339049/weekday-name-from-a-pandas-dataframe-date-object
# https://stackoverflow.com/questions/25146121/extracting-just-month-and-year-separately-from-pandas-datetime-column
# https://www.freecodecamp.org/news/typeerror-cannot-unpack-non-iterable-nonetype-object-how-to-fix-in-python/#:~:text=This%20is%20a%20process%20known,a%20set%20of%20individual%20variables.
# https://www.geeksforgeeks.org/how-to-fix-keyerror-in-pandas/#:~:text=Pandas%20KeyError%20occurs%20when%20we,after%20the%20column%2Frow%20name.
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.mode.html
# https://realpython.com/python-while-loop/
# https://stackoverflow.com/questions/14594522/how-to-break-out-of-while-loop-in-python
# http://net-informations.com/python/iq/global.htm
# https://www.geeksforgeeks.org/find-average-list-python/#:~:text=In%20Python%20we%20can%20find,of%20elements%20in%20a%20list.
# https://stackoverflow.com/questions/51865367/cannot-convert-the-series-to-class-int
# https://stackabuse.com/count-number-of-word-occurrences-in-list-python/
# https://www.geeksforgeeks.org/python-pandas-series-dt-day_name/
# https://www.w3resource.com/pandas/series/series-dt-day_name.php#:~:text=The%20dt.,the%20DateTimeIndex%20with%20specified%20locale.
# https://stackoverflow.com/questions/3499026/find-a-minimum-value-in-an-array-of-floats
# https://www.geeksforgeeks.org/pandas-groupby-count-the-occurrences-of-each-combination/
# https://stackoverflow.com/questions/63229237/finding-the-most-frequent-combination-in-dataframe
# https://pandas.pydata.org/docs/reference/api/pandas.Series.count.html
# https://stackoverflow.com/questions/13130574/what-does-bound-method-error-mean-when-i-call-a-function
