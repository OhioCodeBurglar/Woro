from plyer import notification
import datetime
import os

real_initial = datetime.datetime.now()
real_hour, real_minute, real_second = map(int, real_time.strftime('%H:%M:%S').split(':'))

initial_time = datetime.datetime.strptime("17:00:00", '%H:%M:%S')

while True:
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%H:%M:%S')

    current_hour, current_minute, current_second = map(int, formatted_time.split(':'))
    initial_hour, initial_minute, initial_second = map(int, initial_time.strftime('%H:%M:%S').split(':'))
    
    hour_used = current_hour - real_hour
    minutes_used = current_minute - real_minute
    if hour_used > 3:
        notification.notify( 
    ¦   ¦   title='Take a break!',
    ¦   ¦   message='You have used the computer for over 3 hours consecutivly, go to drink water, eat, or anything else, but take a break',
    ¦   ¦   timeout=20
    ¦   )
    if minutes_used = 245:
        notification.notify(
    ¦   ¦   title='To much computer, in 15 minutes, computer is beggining countdown',
    ¦   ¦   message='You have used the computer alsmost 5 hours, consecutivly, remidner when 2 minutes left',
    ¦   ¦   timeout=20
    ¦   )
    if minutes_used = 258:
        notification.notify(
    ¦   ¦   title='To much computer, in 2 minutes, computer is beggining countdown',
    ¦   ¦   message='You have used the computer alsmost 5 hours, consecutivly, final reminder when 1 minute is left',
    ¦   ¦   timeout=20
    ¦   ) 
    if minutes_used = 259:
        notification.notify(
    ¦   ¦   title='To much computer, in 1 minutes, computer is beggining countdown',
    ¦   ¦   message='You have used the computer alsmost 5 hours, consecutivly, be aware, safe everything NOW',
    ¦   ¦   timeout=20
    ¦   )
    if minutes_used = 300:
        os.system(“shutdown /s /t 1”)


    if (current_hour, current_minute, current_second) == (initial_hour, initial_minute, initial_second):
        notification.notify(
            title='Program!',
            message='Start programming now, connect laptop and use nvim',
            timeout=20
        )

    


