import requests
from time import sleep
from termcolor import colored

suburb = input('Enter suburb name: ').lower()
state = input('Enter state as abbreviation (e.g. NSW): ').upper()
postcode = input('Postcode: ')
type = input('A for AstraZeneca (over 60), B for AstraZeneca (under 60), P for Pfizer, X for any: ')
if (type == 'A'):
  type = 'covid_vaccine-astrazeneca_60_plus%2C'
elif (type == 'B'):
  type = 'covid_vaccine-astrazeneca_under_60%2C'
elif (type == 'P'):
  type = 'covid_vaccine-pfizer%2C'
else:
  type = ''
dose = input('Enter 1 for Dose 1, or 2 for Dose 2: ')

while True:
  headers = dict(
      {'Accept':"application/au.com.hotdoc.v5"}
  )
  url = f"https://www.hotdoc.com.au/api/patient/search?entities=clinics&filters={type}covid_vaccine_dose-{dose}%2Ccovid_vaccine_availability-next_7_days&suburb={suburb}-{state}-{postcode}"
  response = requests.get(url=url, headers=headers)
  response = response.json()

  user_url = f"https://www.hotdoc.com.au/search?filters={type}covid_vaccine_dose-{dose}%2Ccovid_vaccine_availability-next_7_days&in={suburb}-{state}-{postcode}&purpose=covid-vaccine"  

  print(colored('Vaccines available in the next 7 days at', 'yellow'), colored(user_url, 'cyan', attrs=['underline']))
  print('')
  results = response["clinics"]
  for result in results:
    print(colored('Location:', 'white'), colored(result['name'], 'magenta'))
  # Sleep for 60 seconds because who knows what sort of limits we'll reach
  print('')
  print(colored("===== Wait 60 seconds for the next refresh =====", "red", attrs=['bold']))
  print('')
  sleep(60)