from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# Create your views here.


def get_html_content(request):
    
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content


def home(request):

    result = None
    if 'city' in request.GET:
        # Fetch the HTML content from Google using get_html_content function
        html_content = get_html_content(request)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        result = dict()
        # Extract the region from the parsed HTML content
        try:

            result['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
            # Extract the current temperature from the parsed HTML content
            result['temp_now'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
            # Extract the current day and hour, and the current weather condition from the parsed HTML content
            result['dayhour'], result['weather_now'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split('\n')
        
        except:
            pass
    # Render the home.html template with the result dictionary as context
    return render(request, 'core/home.html', {'result': result})
