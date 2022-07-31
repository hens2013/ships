from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
import requests

from counter.models import Point


def get_data_url(url):
    request = requests.get(url)
    request.close()
    return request


# function take list and return str
def list_str(data):
    return ', '.join(data)


def index(request):
    return render(request, 'counter/index.html', {})


def ships_page(request):
    return render(request, 'counter/ships_file.html')


def location_page(request):
    return render(request, 'counter/location_page.html')


# function which return ships that in the circle that is being created with the point and the radius
def ships_locations(request):
    if request.method == 'GET':
        response = None
        try:
            # get the data from the api and the points of the circle
            latitude_number = float(request.GET['latitude_number'])
            longitude_number = float(request.GET['longitude_number'])
            radios_number = float(request.GET['radios_number'])
            point_center = Point(x=latitude_number, y=longitude_number)

            # get the ships data from the url
            URL = 'https://run.mocky.io/v3/367bedbd-5bf6-4d55-a659-2eb6e4f733a2'
            response = get_data_url(URL)
            records = response.json()['records']
            ship_list = {}
            # for loop which goes on all the records and calculate the ship location if it in the circle of the given location
            for record in records:
                point1 = Point(x=record['position']['coordinates'][0], y=record['position']['coordinates'][1])
                ship = record['ship']
                # check if the ship record has name key
                if 'name' in ship.keys():
                    distance = point_center.calculate_distance(point1)
                    if distance <= radios_number:
                        ship_name = ship['name']
                        ship_list[ship_name] = distance
            if ship_list == {}:
                return HttpResponseNotFound('<h1> There are no ships </h1>')
            else:
                # sorted the ships according to the location
                ship_list_distance = dict(sorted(ship_list.items(), key=lambda item: item[1]))
                shis_commom_str = list_str(ship_list_distance.keys())
                context = {'value': shis_commom_str}

            return render(request, 'counter/ships_display.html', context)
        except requests.exceptions.Timeout:
            return HttpResponseNotFound('<h1>' + str(response.status_code) + '</h1>')
        except  requests.ConnectionError:
            return HttpResponseNotFound('<h1>502 Bad Gateway server error response code</h1>')
        except  Exception as e:
            return HttpResponseNotFound('<h1> ' + str(response.status_code) + '</h1>')


# function that get country name and return all the ships that went out from the country
def get_ships_data(request):
    if request.method == 'GET':
        response = None
        try:
            # get the data from the url
            URL = 'https://run.mocky.io/v3/367bedbd-5bf6-4d55-a659-2eb6e4f733a2'
            response = get_data_url(URL)
            data_dict = response.json()

            # get the country name from the api
            country_name = request.GET['country_name']

            # get the ships which left the input country
            ships_list = [record['ship']['name'] for record in data_dict['records'] if
                          record['ship']['country'] == country_name]
            if len(ships_list) == 0:
                raise HttpResponseNotFound('<h1>There are not ships</h1>')
            else:
                shis_commom_str = list_str(ships_list)
                context = {'value': shis_commom_str}

            return render(request, 'counter/ships_display.html', context)
        except requests.exceptions.Timeout:
            return HttpResponseNotFound('<h1>' + str(response.status_code) + '</h1>')
        except  requests.ConnectionError:
            return HttpResponseNotFound('<h1>502 Bad Gateway server error response code</h1>')
        except  Exception:
            return HttpResponseNotFound('<h1> ' + str(response.status_code) + '</h1>')
