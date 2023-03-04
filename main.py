#!/usr/local/bin/python3

from person import Person
import sys
import villa_brunati_booking_system as booksystem

GREEN = '\033[92m'


def intro_message():
    print(GREEN, """
     _                _            
    | |              | |            
    | |__   __ _  ___| | _____ _ __ 
    | '_ \ / _` |/ __| |/ / _ \ '__|
    | | | | (_| | (__|   <  __/ |   
    |_| |_|\__,_|\___|_|\_\___|_|   
                                    """)
    print(GREEN, "\tVilla brunati Cracking Tool! \n \t\t\t By MJS ")


#  Our personas to book places for ourselves
MICHAEL = Person('Michael', 'Saccone', 'michael.jason.saccone@gmail.com', '+393332576212')
MAHIR = Person('Mahir', 'Alani', 'mahiralani24@gmail.com', '+393516878076')
ANDREA = Person('Andrea', 'Stefanelli', 'stefanelliandrea28@gmail.com', '+393881647767')


def take_for_us(day):
    booksystem.take_place_by_placename('Sala Filosofia1', MICHAEL, day)
    booksystem.take_place_by_placename('Sala Filosofia 2', MAHIR, day)
    booksystem.take_place_by_placename('Sala Scienze 2', ANDREA, day)


def take_all(day):
    booksystem.take_every_place(day)


def run():
    intro_message()
    handle_input_args()


def handle_input_args():
    if len(sys.argv) == 1:
        print_help()
    else:
        day = str(booksystem.TOMORROW)
        #  User can specify day
        if len(sys.argv) == 3:
            day = sys.argv[2]
        match (sys.argv[1]):
            case "-a" | "--all":
                take_all(day)
            case "-u" | "--us":
                take_for_us(day)
            case "-au" | "--all-us":
                take_for_us(day)
                take_all(day)
            case _:
                print_help()


def print_help():
    print(" Usage: " + sys.argv[0] + " <arg> [<day>]\n")
    print(" <arg>:")
    print("-a --all:  Occupy all places for tomorrow")
    print("-u --us:  Occupy default places for us")
    print("-au --all-us:  Occupy default places for us + all other places")
    print("-h --help:  See this guide")
    print()
    print(" <day>:  If you do not specify the day, default is tomorrow: " + str(booksystem.TOMORROW))


if __name__ == '__main__':
    run()
