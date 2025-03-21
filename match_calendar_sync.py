import requests
import json
import re
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from datetime import datetime, timedelta







# SECTION: functions
def get_calendar_service():
    """Authenticates the Google Calendar API"""

    # JSON path with service account credentials
    SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")

    # Scope required to modify Google Calendar
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=credentials)

    return service

def create_event(summary, local, date, start_time, end_time):
    """Create an event in Google Calendar"""

    event = { 
        "summary": summary,
        "location": local,
        "start": {
            "dateTime": f"{date}T{start_time}:00",
            "timeZone": "America/Sao_Paulo",
        },
        "end": {
            "dateTime": f"{date}T{end_time}:00",
            "timeZone": "America/Sao_Paulo",
        },
    }

    # call google calendar service
    service = get_calendar_service()
    service.events().insert(calendarId="user_email@hotmail.com", body=event).execute()

def processing_matches():
    """Select the games you need"""
    
    # Load JSON from the file
    with open("jogos2.json", "r", encoding="utf-8") as file:
        date = json.load(file)

    # List for storing extracted data
    matches_date = []
    for match in date.get("future", []):
        match_info = match.get("match", {})

        # Extract the desired information
        first_team = match_info.get("firstContestant", {}).get("popularName", "N/A")

        location = "N/A"  # Default value if you can't find it
        if match_info and match_info.get("location") is not None:
            location = match_info["location"].get("popularName", "N/A")

        second_team = match_info.get("secondContestant", {}).get("popularName", "N/A")
        start_date = match_info.get("startDate", "N/A")
        start_hour = match_info.get("startHour", "N/A")

        # Add to data array
        matches_date.append([first_team, location, second_team, start_date, start_hour])

    # Create a DataFrame with the collected data
    df = pd.DataFrame(matches_date, columns=["Time Casa", "Local", "Time Visitante", "date", "Hora"])

    return df

def collect_matches():
    """Collect the team's matches of the year"""

    url = "https://ge.globo.com/futebol/times/corinthians/agenda-de-jogos-do-corinthians/#/proximos-jogos"

    # Send the request and capture the response
    response = requests.get(url, headers=response.headers)
    print(response.status_code)

    if response.status_code == 200:
        with open("resposta_request.txt", "w", encoding="utf-8") as file:
            file.write(response.text)

    future_matches = '"future":['
    final = ',"now"'
    if future_matches in response.text:
        print('future_matches encontrada')

        # Using regex to capture everything between “future”: [ and up to “], ”now”
        match = re.search(r'(' + re.escape(future_matches) + r'.*?' + re.escape(final) + r')', response.text, re.DOTALL)

        if match:
            extracted_text = match.group(1)
            extracted_text = extracted_text.replace(final, '')
            extracted_text = '{' + extracted_text + '}'

            try:
                json_date = json.loads(extracted_text)
                print("JSON successfully converted!")

                with open("jogos2.json", "w", encoding="utf-8") as json_file:
                    json.dump(json_date, json_file, ensure_ascii=False, indent=4)

                status_json = {'ok': json_date}
                return status_json

            except json.JSONDecodeError as e:
                print(f"Error converting to JSON: {e}")
                status_json = {'error':e}

        else:
            error_msg = 'no pattern found in the answer'
            print(error_msg)
            status_json = {'error':error_msg}
    else:
        error_msg = 'json not found in request'
        print(error_msg)
        status_json = {'error':error_msg}

        # TODO: se na primeira tentativa nao conseguir, executar codigo de novo

    return status_json

def list_events():
    """Lists the Google Calendar events created by the script"""

    # Sets the time interval for searching events from 2025
    time_min = "2025-01-01T00:00:00Z"  # Início de 2025
    time_max = "2025-12-31T23:59:59Z"  # Fim de 2025

    service = get_calendar_service()

    # Request for events in the specified period
    events = service.events().list(
        calendarId="user_email@hotmail.com", #Calendar ID (same as used to create events)
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,  # Sorts recurring events correctly
        orderBy="startTime"
    ).execute()
    
    # List for storing data
    events_list = []
    if "items" in events:
        for event in events["items"]:
            events_list.append({
                "Título": event.get("summary", "Sem título"),
                "Data Início": event["start"].get("dateTime", "Sem data"),
                "Data Fim": event["end"].get("dateTime", "Sem data"),
                "Local": event.get("location", "Sem local"),
                "ID": event.get("id", "Sem ID")
            })
        df_events = pd.DataFrame(events_list)
    else:
        print("No event found for 2025.")
        return pd.DataFrame()
    
    df_calendario = df_events[df_events['Título'].str.contains("Corinthians")]
    
    return df_calendario

def update_event(titulo_event, id_event, site_time):
    """Updates the date and time of the event in Google Calendar """

    # Checks if site_time is a string and converts it if necessary
    if isinstance(site_time, str):
        site_time = datetime.strptime(site_time, "%Y-%m-%dT%H:%M:%S%z")
    hora_site_str = site_time.strftime("%Y-%m-%dT%H:%M:%S%z")
    novo_date_fim = (site_time + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S%z")

    event_atualizado = {
        "summary": titulo_event,
        "start": {"dateTime": hora_site_str, "timeZone": "America/Sao_Paulo"},
        "end": {"dateTime": novo_date_fim, "timeZone": "America/Sao_Paulo"},
    }
    
    service = get_calendar_service()
    try:
        service.events().update(
            calendarId="user_email@hotmail.com",
            eventId=id_event,
            body=event_atualizado
        ).execute()
        print(f"event updated, new timetable: {site_time}\n\n")
    except Exception as error:
        print(f"error when updating event{id_event}: {error}\n\n")

def update_calendar(df):
    """Analyze events: access calendar, create/update events"""

    df_site = df[df['Time Casa'] == 'Corinthians']

    df_calendario = list_events()

    with pd.ExcelWriter("dados_corinthians.xlsx") as writer:
        df_site.to_excel(writer, sheet_name="Jogos_Site", index=False)
        df_calendario.to_excel(writer, sheet_name="events_Calendario", index=False)
    print("Data exported to 'dados_corinthians.xlsx'.")

    for _, row in df_site.iterrows():
        time_casa = row["Time Casa"]
        time_visitante = row["Time Visitante"]
        date_jogo = row["date"]
        site_time = row["Hora"]
        summary_jogo = f"{time_casa} x {time_visitante}"

        # Check if the game is already on the calendar
        match = df_calendario[df_calendario["Título"] == summary_jogo]
        if not match.empty:

            # The match is already on the calendar
            if pd.notna(site_time) and site_time.strip():

                print(f"update event: {summary_jogo} ({date_jogo} {site_time})")
                id_event = match.iloc[0]["ID"]
                full_site_time = f"{date_jogo}T{site_time}-03:00"  # format: YYYY-MM-DDTHH:MM:SS+00:00
                full_site_datetime = datetime.strptime(full_site_time, "%Y-%m-%dT%H:%M:%S%z")

                update_event(summary_jogo, id_event, full_site_datetime) 
        else:
            # Game not on the calendar
            local = row["Local"]
            start_time = "09:00" if pd.isna(site_time) or not site_time.strip() else site_time[:5]
            end_time = (datetime.strptime(start_time, "%H:%M") + timedelta(hours=1)).strftime("%H:%M")
            
            print(f"Creating events: {summary_jogo} ({date_jogo} {start_time})")
            create_event(summary_jogo, local, date_jogo, start_time, end_time)







# SECTION: main
def calendar_analysis():

    # access games via web scrapping
    request_json = collect_matches()
    print(request_json)

    # processing collected data
    if 'ok' not in request_json:
        print("error: No json found in the request. Trying again...")
        request_json = collect_matches()
        print(request_json)

    elif 'ok' in request_json and request_json['ok']:
        df = processing_matches()
        update_calendar(df)
            
    else:
        print("Error accessing data. Could not continue.")


calendar_analysis()
