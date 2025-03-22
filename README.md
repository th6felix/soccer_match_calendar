<div align="center">
  <h1 align="center"> ⚽ Soccer match calendar ⚽ </h1>
  <p> Automation to collect data on soccer matches on a sports website, process this information and add it to Google Calendar events. </p>

  <br>
</div>


## ⚙️ How it works
This automation performs the following steps:

1. **Data collection**  
   - Collection of information on soccer matches on the website for any team during the year, with the ability to customize the search for different teams
     
     #### Technology: Web Scraping (Requests)
  
2. **Data processing**  
   - Conversion of match dates and times into the desired format.
   - Filter the matches of the day.
     
      #### Technology: Pandas
    
3. **API integration**  
   - Configuring api access data.
   - Creating and updating events in Google Calendar with the games collected.
     
     #### Technology: Google Calendar API

4. **Automatic execution**  
   - The script is set to run automatically after 45 minutes when the PC is switched on
   
     #### Technology: Windows Task Scheduler

<br>

## 🛠️ How to configure

1. **Install the Dependencies**  
   ```bash
   pip install beautifulsoup4 requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas

2. **Set up your Google Service Account**
    - Create a service account in Google Cloud Console.
    - Download the service account credentials and place the JSON file in the project folder.
    - Give the service account permissions to add events to your calendar.

3. **Change the code for your soccer team**
    - BR: change time in the url of the source site (Globo Esporte)
    - other countries: adjust url and processing logic

4. **Configuring the Task Scheduler (Windows)**
    - Open the “Task Scheduler” in Windows.
    - Create a new task to run the Python script automatically
    - Configure “triggers”.

<br>

 <img>![image](https://github.com/user-attachments/assets/3912def4-eb96-417a-b324-6599d11a499d)

