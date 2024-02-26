from datetime import datetime
import os

def get_timestamp() -> str:
    timestamp = datetime.now().strftime('%H:%M:%S on %d %b %Y')
    return timestamp

def clear_screen() -> None:
    '''clears the terminal'''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_to_screen_and_wait(message: str) -> None:
    '''clear terminal and print message to screen.'''
    clear_screen()
    print(f'{message}\n')  # get user's attention!
    input('(press enter to close this window)') # force user to acknowledge by closing window

def today_is_weekday() -> bool:
    '''crude mechanism for determining if today is a weekday.'''
    today = datetime.now().strftime('%a')
    weekend = ['Sat', 'Sun']
    if today not in weekend:
        return True
    else:
        return False