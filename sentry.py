import teslapy
from datetime import datetime, timedelta
from time import sleep

def SentryOn(OnOff):
    with teslapy.Tesla('wooogamer@gmail.com', 'doWhatuwant2do!t') as tesla:
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
    with teslapy.Tesla('wooogamer@gmail.com', 'doWhatuwant2do!t') as tesla:
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

