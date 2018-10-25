
from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import webbrowser
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def gmailapi():

    store = file.Storage('token.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, sto    re)
    service = build('calendar', 'v3', http=creds.authorize(Http()))


    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    f = open('helloworld.html', 'w')
    if not events:
        message="""<html>
         <head></head>
         <body><p> No upcoming events found</p></body>
         </html>"""
        print('No upcoming events found.')

    strthtml="""<html>
         <head></head>
         <body>"""

    f.write(strthtml)

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))

        message = """<p>""" + start + """  """ + event['summary'] + """</p></br>"""

        f.write(message)
        print(start)
        print(event['summary'])

    endhtml="""</body>
         </html>"""
    f.write(endhtml)
    f.close()

    webbrowser.open_new_tab('helloworld.html')

if __name__ == '__main__':
    gmailapi()