import teslapy
from datetime import datetime, timedelta
from time import sleep

email = 'wooogamer@gmail.com'
password = 'doWhatuwant2do!t'

def get_passcode():
    return raw_input('Passcode: ')

def select_factor(factors):
    print('-'*80)
    print('ID Name')
    for i, factor in enumerate(factors):
        print('{:2} {}'.format(i, factor['name']))
    print('-'*80)
    idx = int(raw_input('Select factor: '))
    print('-'*80)
    return factors[idx]

def getAccess(email, password):
    with teslapy.Tesla(email, password, get_passcode, select_factor) as tesla:
        return tesla

def SentryOn(OnOff):
    tesla = getAccess(email, password)
    tesla.fetch_token()
    vehicles = tesla.vehicle_list()
    vehicles[0].sync_wake_up()
    try:
        if OnOff: 
            vehicles[0].command('SET_SENTRY_MODE', on='true')
            nowtime = datetime.now()
            nowstr = nowtime.strftime('%H:%M:%S')
            print("TURN ON ", nowstr)
        else:
            vehicles[0].command('SET_SENTRY_MODE', on='false')
            nowtime = datetime.now()
            nowstr = nowtime.strftime('%H:%M:%S')
            print("TURN OFF", nowstr)
    except teslapy.HTTPError as e:
        print(e)
        sleep(30)
        SentryOn(OnOff)
    print(vehicles[0].get_vehicle_summary())
def getStatus():
    tesla = getAccess(email, password)
    tesla.fetch_token()
    vehicles = tesla.vehicle_list()
    vehicles[0].sync_wake_up()
    return vehicles[0].get_vehicle_summary()
    

def SentryRoutine(duration, period):
    SentryOn(True)
    
    starttime = datetime.now()
    delta4on = timedelta(hours=period)
    delta4off = timedelta(hours=duration)
    nexttime = starttime + delta4off
    nextontime = starttime + delta4on

    nowstr = starttime.strftime('%H:%M:%S')
    offstr = nexttime.strftime('%H:%M:%S')
    onstr = nextontime.strftime('%H:%M:%S')
    
    print("startTime ", nowstr)
    print("OffTime ",offstr)
    print("NextOnTime ", onstr)
    turnon = False
    while True:
         if nexttime < datetime.now():
             SentryOn(turnon)
             turnon = not turnon
             if turnon:
                 nexttime += delta4on
             else:
                 nexttime += delta4off

