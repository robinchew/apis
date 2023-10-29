import urllib.request
import urllib.parse
import json
import os
from datetime import timedelta, datetime
import pytz

# EVENTBRITE API SCRIPT

EVENTBRITE_API_BASE_URL = "https://www.eventbriteapi.com/v3/"

'''
# https://www.eventbrite.com/platform/api#/introduction/authentication/2.-(for-app-partners)-authorize-your-users
def get_oauth_token():
    # Get this working if using private token in header is not secure enough
    req = urllib.request.Request(,
        'https://www.eventbrite.com/oauth/token',
        data=urllib.parse.urlencode({
            grant_type=authorization_code,
            client_id
            client_secret,
            code
            redirect_uri
        }).encode(),
        headers={
            'content-type': 'application/x-www-form-urlencoded',
        })
def get_api_token(api_key):
    # Get this working if using private token in header is not secure enough
    req = urllib.request.Request('https://www.eventbrite.com/oauth/authorize?' + urllib.parse.urlencode({
        'response_type': 'token',
        'client_id': api_key,
        'redirect_uri': 'http://example.robin.au/eventbrite/redirect_uri',
    }))
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
'''

def get_organization(eventbrite_api_token):
    url = f"{EVENTBRITE_API_BASE_URL}users/me/organizations/"
    headers = {
        'Authorization': eventbrite_api_token
    }

    # Make the request
    req = urllib.request.Request(url, headers=headers)

     # Perform the GET request
    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')
    if resp.status != 200:
        return print(f"HTTP Error: {resp.status}")
    return data

def get_event_by_id(eventbrite_api_token, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/"
    headers = {
        'Authorization': eventbrite_api_token
    }

    # Make the request
    req = urllib.request.Request(url, headers=headers)

     # Perform the GET request
    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')

    if resp.status != 200:
        return print(f"HTTP Error: {resp.status}")

    return data

def get_events_by_organization(eventbrite_api_token, organization_id):
    url = f"{EVENTBRITE_API_BASE_URL}organizations/{organization_id}/events"
    headers = {
        'Authorization': eventbrite_api_token
    }

    # Make the request
    req = urllib.request.Request(url, headers=headers)

     # Perform the GET request
    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')
    if resp.status != 200:
        return print(f"HTTP Error: {resp.status}")
    return data

def create_event(eventbrite_api_token, organization_id ,event_details):
    url = f"{EVENTBRITE_API_BASE_URL}organizations/{organization_id}/events/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }
    event_details_bytes = event_details.encode('utf-8')

    req = urllib.request.Request(url, headers=headers, data=event_details_bytes, method='POST')

    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')

    if resp.status != 200:
        error_data = json.loads(data)
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    print({"message": "Event created successfully", "status_code": resp.status})
    return json.loads(data)

def update_event(eventbrite_api_token, event_id, event_details):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Make the POST request
    event_details_bytes = event_details.encode('utf-8')

    req = urllib.request.Request(url, headers=headers, data=event_details_bytes, method='POST')

    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')

    if resp.status != 200:
        error_data = json.loads(data)
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    print({"message": "Event updated successfully", "status_code": resp.status})
    return json.loads(data)

def delete_event(eventbrite_api_token, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Create a DELETE request using urllib.request
    req = urllib.request.Request(url, headers=headers, method='DELETE')

    # Perform the request
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
    if status_code != 200:
        error_data = json.loads(response.read().decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": status_code
        }

    # A successful DELETE request should return a 200 status code for Eventbrite
    return print({"message": "Event deleted successfully", "status_code": status_code})

def unpublish_event(eventbrite_api_token, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/unpublish/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }
    # Make the POST request
    req = urllib.request.Request(url, headers=headers, method='POST')

    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')

    if resp.status != 200:
        error_data = json.loads(data)
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    print({"message": "Event unpublished successfully", "status_code": resp.status})
    return json.loads(data)

def publish_event(eventbrite_api_token, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/publish/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Make the POST request
    req = urllib.request.Request(url, headers=headers, method='POST')

    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')

    if resp.status != 200:
        error_data = json.loads(data)
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    print({"message": "Event published successfully", "status_code": resp.status})
    return json.loads(data)

def create_ticket_class(eventbrite_api_token, event_id, ticket_details):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/ticket_classes/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    ticket_details_bytes = ticket_details.encode('utf-8')

    # Make the POST request
    req = urllib.request.Request(url, headers=headers, data=ticket_details_bytes, method='POST')

    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')

    if resp.status != 200:
        error_data = json.loads(data)
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    print({"message": "Ticket class created successfully", "status_code": resp.status})
    return json.loads(data)

def get_ticket_class_by_id(eventbrite_api_token, event_id, ticket_class_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/ticket_classes/{ticket_class_id}/"
    headers = {
    'Authorization': eventbrite_api_token,
    }

    # Make the request
    req = urllib.request.Request(url, headers=headers)

     # Perform the GET request
    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')

    if resp.status != 200:
        return print(f"HTTP Error: {resp.status}")

    return data

def update_ticket_class(eventbrite_api_token, event_id, ticket_class_id, ticket_details):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/ticket_classes/{ticket_class_id}/"
    headers = {
        'Authorization': eventbrite_api_token,
        'Content-Type': 'application/json'
    }

    ticket_details_bytes = ticket_details.encode('utf-8')

    # Make the POST request
    req = urllib.request.Request(url, headers=headers, data=ticket_details_bytes, method='POST')

    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')

    if resp.status != 200:
        error_data = json.loads(data)
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    print({"message": "Ticket class updated successfully", "status_code": resp.status})
    return json.loads(data)

def quick_create_event(eventbrite_api_token, organization_id, title, description, date_start, duration_hours, event_timezone='Australia/Perth', cost_cents=None, publish=False):

    # Create a timezone object for the specified timezone
    new_timezone = pytz.timezone(event_timezone)

    # Convert date_start to a timezone-aware datetime
    date_start = datetime.strptime(date_start, "%Y-%m-%dT%H:%M:%S")

    date_start = new_timezone.localize(date_start)

    # Calculate the end datetime based on duration_hours
    date_end = date_start + timedelta(hours=duration_hours)

    # Convert the start datetime to UTC
    utc_date_start = date_start.astimezone(pytz.utc)
    # Convert the end datetime to UTC
    utc_date_end = date_end.astimezone(pytz.utc)

    # Create the event details JSON
    event_detail = {
        "event": {
            "name": {
                "html": f"<p>{title}</p>"
            },
            "description": {
                "html": f"<p>{description}</p>"
            },
            "start": {
                "timezone": new_timezone.zone,
                "utc": utc_date_start.strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            "end": {
                "timezone": new_timezone.zone,
                "utc": utc_date_end.strftime("%Y-%m-%dT%H:%M:%SZ")

            },
            "currency": "AUD",
            "online_event": False,
            "organizer_id": "",
            "listed": True,
            "shareable": True,
            "invite_only": False,
            "show_remaining": True,
            "capacity": 100,
            "is_reserved_seating": False,
            "is_series": False,
            "show_pick_a_seat": False,
            "show_seatmap_thumbnail": False,
            "show_colors_in_seatmap_thumbnail": False,
            "locale": "en_AU"
        }
    }

    # Convert the event details to a JSON string
    event_detail_json = json.dumps(event_detail)

    # Create the event
    new_event = create_event(eventbrite_api_token, organization_id, event_detail_json)

    # Extract the event_id from the response
    event_id = new_event.get('id')

    # Create the ticket class details JSON
    ticket_detail = {
        "ticket_class":
        {
            "name": "API Test1",
            "donation": "false",
            "quantity_total": "100",
            "minimum_quantity": "1",
            "maximum_quantity": "10",
            "hidden": "false",
            "auto_hide": "false",
            "auto_hide_before": "",
            "auto_hide_after": "",
            "sales_channels": ["online","atd"],
            "hide_sale_dates": "false",
            "delivery_methods": ["electronic"],
            "include_fee": "false",
            "sales_start": date_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sales_end": date_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            **({"cost": f"AUD,{cost_cents}", "free": "false"} if cost_cents is not None else {'free': "true"}),
        }
    }

    # Convert the ticket class details to a JSON string
    ticket_detail_json = json.dumps(ticket_detail)

    # Create the ticket class
    new_tickets = create_ticket_class( eventbrite_api_token, event_id, ticket_detail_json)

    if publish:
        publish_event(eventbrite_api_token, event_id)
    return new_event, new_tickets

if __name__ == "__main__":

    # Retrieve the values of an environment variables
    eventbrite_api_token = os.environ['EVENTBRITE_API_TOKEN']
    organization_id = os.environ['EVENTBRITE_ORGANIZATION_ID']
    publish = os.environ.get("PUBLISH")

    print(quick_create_event(eventbrite_api_token, organization_id, "API-TEST-617", "API-TEST-DESCRIPTION-9", "2023-11-12T14:00:00", 2, 'Australia/Perth', 2000, publish))

    # TO PUBLISH AN EVENT
    # 1. CREATE AN EVENT
    # 2. CREATE A TICKET CLASS TO EVENT
    # 3. PUBLISH EVENT
