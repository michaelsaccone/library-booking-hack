import requests
import json
from person import Person
from datetime import date
import datetime

URL = 'https://api-public.timify.io/'
COMPANY_ID = '6049d1736cad5011a7118fad'
TOMORROW = date.today() + datetime.timedelta(days=1)

TIME = {
    '9': 540,
    '12': 760,
    '16': 980,
}

ERROR_RED = '\033[91m'

def get_daily_events(day=str(TOMORROW)):
    data = {
        "operationName": "getOnlineServiceAvailability",
        "variables": {
            "params": {
                "companyId": COMPANY_ID,
                "region": "EUROPE",
                "days": [
                    str(day)
                ],
                "serviceId": "6049d1a53a81a01166265422"
            },
            "timezone": "Europe/Rome",
        },
        "query": "query getOnlineServiceAvailability($params: OnlineServiceAvailabilityParams!, $timezone: Timezone, "
                 "$sessionId: ID, $metadata: Dynamic) {\n  getOnlineServiceAvailability(params: $params, "
                 "timezone: $timezone, sessionId: $sessionId, metadata: $metadata) {\n    dependencies {\n      "
                 "name\n      resourceIds\n    }\n    resources {\n      id\n      abbreviation\n      externalId\n   "
                 "   name\n      categoryId\n      avatarUrl\n      color\n      orderIndex\n    }\n    "
                 "resourceCategories {\n      id\n      name\n      orderIndex\n    }\n    slots {\n      day\n      "
                 "minutes\n    }\n    calendarEnd\n    calendarBegin\n    onDays\n    offDays\n    "
                 "allocationOffDays\n  }\n}\n "
    }

    return requests.post(URL, json.dumps(data)).json()['data']['getOnlineServiceAvailability']


def get_place_event(place_name):
    events = get_daily_events()['resources']
    place_event = filter(lambda x: x['name'].lower() == place_name.lower(), events)
    return list(place_event)[0]


#     Get Specific information for booking a place
#     Return the event_id and secret useful to use book_place function
def select_booking_event(place_id: str, day, time):
    data = {
        "operationName": "reserveOnlineService",
        "variables": {
            "params": {
                "companyId": COMPANY_ID,
                "region": "EUROPE",
                "serviceId": "6049d1a53a81a01166265422",
                "slot": {
                    "day": str(day),
                    "minute": str(time)
                },
                "selectedResourceIds": [
                    str(place_id)
                ]
            },
            "timezone": "Europe/Rome",
            "metadata": {}
        },
        "query": "mutation reserveOnlineService($params: OnlineServiceReservationParams!, $timezone: Timezone, "
                 "$sessionId: ID, $metadata: Dynamic) {\n  reserveOnlineService(params: $params, timezone: $timezone, "
                 "sessionId: $sessionId, metadata: $metadata) {\n    companyId\n    eventId\n    secret\n  }\n}\n "
    }

    response = requests.post(URL, json.dumps(data)).json()
    reservation_info = response['data']['reserveOnlineService']

    if reservation_info is None:
        raise Exception(ERROR_RED, "ERROR: cannot book for this date.\n place: " + str(place_id) + "\n day: " + str(day)
              + "\n time: " + str(time))

    return reservation_info


def book_place(person: Person, event_id, secret):
    data = {
        "operationName": "finaliseOnlineEventReservation",
        "variables": {
            "event": {
                "companyId": COMPANY_ID,
                "region": "EUROPE",
                "eventId": event_id,
                "secret": secret,
                "fields": [
                    {
                        "id": "6049d1736cad5011a7118fb8",
                        "type": "TEXT",
                        "value": person.name,
                        "valuesAdd": "",
                        "valuesRemove": ""
                    },
                    {
                        "id": "6049d1736cad5011a7118fb9",
                        "type": "TEXT",
                        "value": person.surname,
                        "valuesAdd": "",
                        "valuesRemove": ""
                    },
                    {
                        "id": "6049d1736cad5011a7118fba",
                        "type": "EMAIL",
                        "value": person.email,
                        "valuesAdd": "",
                        "valuesRemove": ""
                    },
                    {
                        "id": "6049d1736cad5011a7118fbb",
                        "type": "PHONE",
                        "value": "{\"number\":\"" + person.phone + "\",\"country\":\"IT\"}",
                        "valuesAdd": "",
                        "valuesRemove": ""
                    }
                ],
            },
            "metadata": {}
        },
        "query": "mutation finaliseOnlineEventReservation($event: EventReservationPayload!, $sessionId: ID, "
                 "$metadata: Dynamic, $externalCustomerId: ID) {\n  finaliseOnlineEventReservation(event: $event, "
                 "sessionId: $sessionId, metadata: $metadata, externalCustomerId: $externalCustomerId) {\n    id\n    "
                 "icsText\n  }\n}\n "
    }
    requests.post(URL, json.dumps(data))
    print("- - - - Booking Complete! - - - -")
    print(person)
    print("- - - - - - - - - - - - - - - - -")


def take_place(person: Person, place_id, day, time):
    event_info = select_booking_event(place_id, day, time)
    book_place(person, event_info['eventId'], event_info['secret'])


def take_place_all_day(person: Person, place_id, day=str(TOMORROW)):
    try:
        take_place(person, place_id, day, TIME['9'])
        take_place(person, place_id, day, TIME['12'])
        take_place(person, place_id, day, TIME['16'])
    except Exception:
        print(" - - - - - - - - - - - - - - - - - - - -")
        print(ERROR_RED, "\tError in booking: ")
        print(" Place ID: " + place_id)
        print("\t\tPerson: ")
        print(person)
        print(" day: " + day)
        print(" - - - - - - - - - - - - - - - - - - - -")


def take_every_place(day=str(TOMORROW)):
    events_id = get_daily_events(day)['dependencies'][0]['resourceIds']
    persons = Person.generate_random(len(events_id))
    for i, place_id in enumerate(events_id):
        take_place_all_day(persons[i], place_id, day)


def take_place_by_placename(place_name, person: Person, day=str(TOMORROW)):
    print(" Trying to book " + place_name + " for " + person.email)
    place = get_place_event(place_name)
    take_place_all_day(person, place['id'], str(day))
