import requests
from time import sleep
from termcolor import colored

# Get info from user
# HotDoc uses dashes (-) for spaces, so we replace if they exist
# Also uses lowercase for location names.
suburb = input('Enter suburb name: ').lower().replace(" ", "-")
state = input('Enter state as abbreviation (e.g. NSW): ').upper()
postcode = input('Postcode: ')
type = input('A for AstraZeneca, P for Pfizer, X for any: ').upper()
if (type == 'A'):
  type = input('Are you over 60? [y/n]: ').upper()
  if (type =='Y'):
    type = 'covid_vaccine-astrazeneca_60_plus%2C'
  elif (type == 'N'):
    type = 'covid_vaccine-astrazeneca_under_60%2C'
elif (type == 'P'):
  type = 'covid_vaccine-pfizer%2C'
else:
  type = ''
dose = input('First or second dose? Enter [1] or [2]: ')

# Loop through API
while True:
  # We need this header to get a [200] SUCCESS. Otherwise it 404's.
  # Let's pretend we're actually using the HotDoc website!
  headers = dict(
      {'Accept':"application/au.com.hotdoc.v5"}
  )
  
  # Input user info to API call
  url = f"https://www.hotdoc.com.au/api/patient/search?entities=clinics&filters={type}covid_vaccine_dose-{dose}%2Ccovid_vaccine_availability-next_7_days&suburb={suburb}-{state}-{postcode}"
  response = requests.get(url=url, headers=headers)
  response = response.json()
  
  # URL user can go to is different to API URL, so we make one.
  user_url = f"https://www.hotdoc.com.au/search?filters={type}covid_vaccine_dose-{dose}%2Ccovid_vaccine_availability-next_7_days&in={suburb}-{state}-{postcode}&purpose=covid-vaccine"  

  print(colored('Vaccines available in the next 7 days at', 'yellow'), colored(user_url, 'cyan', attrs=['underline']))
  print('')
  
  # Every clinic
  results = response["clinics"]
  for result in results:
    # Print the name of each clinic to the console.
    print(colored('Location:', 'white'), colored(result['name'], 'magenta'))
    
  # Sleep for 60 seconds because who knows what sort of limits we'll reach
  print('')
  print(colored("===== Wait 60 seconds for the next refresh =====", "red", attrs=['bold']))
  print('')
  sleep(60)
