import urllib3
import json
import os

# EVENTBRITE API SCRIPT

# Retrieve the values of an environment variables
eventbrite_api_token = os.environ.get('EVENTBRITE_API_TOKEN')
organization_id = os.environ.get('EVENTBRITE_ORGANISATION_ID')
event_id = os.environ.get('EVENTBRITE_EVENT_ID')
ticket_class_id = os.environ.get('EVENTBRITE_TICKET_CLASS_ID')

EVENTBRITE_API_BASE_URL = "https://www.eventbriteapi.com/v3/"

# Examples
event_details = """
  {
    "event": {
      "name": {
        "html": "<p>Api test 2</p>"
      },
      "description": {
        "html": "<p>Api test 3</p>"
      },
      "start": {
        "timezone": "UTC",
        "utc": "2023-11-12T02:00:00Z"
      },
      "end": {
        "timezone": "UTC",
        "utc": "2023-11-30T02:00:00Z"
      },
      "currency": "AUD",
      "online_event": false,
      "organizer_id": "",
      "listed": false,
      "shareable": false,
      "invite_only": false,
      "show_remaining": true,
      "password": "12345",
      "capacity": 100,
      "is_reserved_seating": false,
      "is_series": false,
      "show_pick_a_seat": false,
      "show_seatmap_thumbnail": false,
      "show_colors_in_seatmap_thumbnail": false,
      "locale": "en_AU"
    }
  }
"""

example_paid_ticket_class = """
{
    "ticket_class": {
      "name": "API Test2",
      "free": false,
      "donation": false,
      "quantity_total": "100",
      "minimum_quantity": "1",
      "maximum_quantity": "10",
      "cost": "AUD,2000",
      "hidden": false,
      "auto_hide": false,
      "auto_hide_before": "",
      "auto_hide_after": "",
      "sales_channels": ["online","atd"],
      "hide_sale_dates": false,
      "delivery_methods": ["electronic"],
      "include_fee": false,
      "sales_start": "2023-11-09T08:00:00Z",
      "sales_end": "2023-11-11T03:00:00Z"
    }
}
"""

example_free_ticket_class = """
{
    "ticket_class": {
      "name": "API Test0",
      "free": true,
      "donation": false,
      "quantity_total": "100",
      "minimum_quantity": "1",
      "maximum_quantity": "10",
      "hidden": false,
      "auto_hide": false,
      "auto_hide_before": "",
      "auto_hide_after": "",
      "sales_channels": ["online","atd"],
      "hide_sale_dates": false,
      "delivery_methods": ["electronic"],
      "include_fee": false,
      "sales_start": "2023-11-09T08:00:00Z",
      "sales_end": "2023-11-11T03:00:00Z"
    }
}
"""

def get_organization(http):
    url = f"{EVENTBRITE_API_BASE_URL}users/me/organizations/"
    headers = {
        'Authorization': eventbrite_api_token
    }

    # Make the GET request
    resp = http.request('GET', url, headers=headers)

    # Check the status code to ensure a successful request
    if resp.status == 200:
        data = resp.data.decode('utf-8')
        print(data)
    else:
        print(f"HTTP Error: {resp.status}")

def get_event_by_id(http, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/"
    headers = {
        'Authorization': eventbrite_api_token
    }

    # Make the GET request
    resp = http.request('GET', url, headers=headers)

    # Check the status code to ensure a successful request
    if resp.status == 200:
        data = resp.data.decode('utf-8')
        print(data)
    else:
        print(f"HTTP Error: {resp.status}")

def get_events_by_organization(http, organization_id):
    url = f"{EVENTBRITE_API_BASE_URL}organizations/{organization_id}/events"
    headers = {
        'Authorization': eventbrite_api_token
    }

    # Make the GET request
    resp = http.request('GET', url, headers=headers)

    # Check the status code to ensure a successful request
    if resp.status == 200:
        data = resp.data.decode('utf-8')
        print(data)
    else:
        print(f"HTTP Error: {resp.status}")

def create_event(http, organization_id ,event_details):
    url = f"{EVENTBRITE_API_BASE_URL}organizations/{organization_id}/events/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    try:
        # Make the POST request
        resp = http.request('POST', url, headers=headers, body=event_details)
        # Check the status code to ensure a successful request
        if resp.status == 200:
            data = resp.data.decode('utf-8')
            print(data)
            return json.loads(data)
        elif resp.status == 400:
            error_data = json.loads(resp.data.decode('utf-8'))
            error_detail = error_data.get('error_detail', {})
            return {
                "error": error_data.get('error', 'Unknown Error'),
                "error_description": error_data.get('error_description', 'An error occurred'),
                "error_detail": error_detail,
                "status_code": resp.status
            }
        else:
            print(f"HTTP Error: {resp.status}")
            return None
    except urllib3.exceptions.HTTPError as e:
        return {
            "error": "HTTP Error",
            "error_description": str(e),
            "status_code": e.code
        }

def update_event(http, event_id, event_details):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    try:
        # Make the POST request
        resp = http.request('POST', url, headers=headers, body=event_details)
        # Check the status code to ensure a successful request
        if resp.status == 200:
            data = resp.data.decode('utf-8')
            return json.loads(data)
        elif resp.status == 400:
            error_data = json.loads(resp.data.decode('utf-8'))
            error_detail = error_data.get('error_detail', {})
            return {
                "error": error_data.get('error', 'Unknown Error'),
                "error_description": error_data.get('error_description', 'An error occurred'),
                "error_detail": error_detail,
                "status_code": resp.status
            }
        else:
            print(f"HTTP Error: {resp.status}")
            return None
    except urllib3.exceptions.HTTPError as e:
        return {
            "error": "HTTP Error",
            "error_description": str(e),
            "status_code": e.code
        }

def delete_event(http, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Make the DELETE request
    resp = http.request('DELETE', url, headers=headers)
    # Check the status code to ensure a successful request
    if resp.status == 200:
        # A successful DELETE request should return a 200 status code for Eventbrite
        return {"message": "Event deleted successfully", "status_code": resp.status}
    elif resp.status == 400:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    else:
        print(f"HTTP Error: {resp.status}")
        return None

def unpublish_event(http, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/unpublish/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }
    # Make the POST request
    resp = http.request('POST', url, headers=headers)

    # Check the status code to ensure a successful request
    if resp.status == 200:
        data = resp.data.decode('utf-8')
        return json.loads(data)
    elif resp.status == 400:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
            }
    else:
        print(f"HTTP Error: {resp.status}")
        return None
    
def publish_event(http, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/publish/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Make the POST request
    resp = http.request('POST', url, headers=headers)

    # Check the status code to ensure a successful request
    if resp.status == 200:
        data = resp.data.decode('utf-8')
        return json.loads(data)
    elif resp.status == 400:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
            }
    else:
        print(f"HTTP Error: {resp.status}")
        return None

def create_ticket_class(http, event_id, ticket_details):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/ticket_classes/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Make the POST request
    resp = http.request('POST', url, headers=headers, body=ticket_details)
    
    # Check the status code to ensure a successful request
    if resp.status == 200:
        data = resp.data.decode('utf-8')
        return json.loads(data)
    elif resp.status == 400:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
            }
    else:
        print(f"HTTP Error: {resp.status}")
        return None
    
def get_ticket_class_by_id(http, event_id, ticket_class_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/ticket_classes/{ticket_class_id}/"
    headers = {
    'Authorization': eventbrite_api_token,
    }

    # Make the GET request
    resp = http.request('GET', url, headers=headers)

    # Check the status code to ensure a successful request
    if resp.status == 200:
        data = resp.data.decode('utf-8')
        print(data)
    else:
        print(f"HTTP Error: {resp.status}")

def update_ticket_class(http, event_id, ticket_class_id, ticket_details):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/ticket_classes/{ticket_class_id}/"
    headers = {
        'Authorization': eventbrite_api_token,
        'Content-Type': 'application/json'
    }
    
    # Make the POST request
    resp = http.request('POST', url, headers=headers, body=ticket_details)
    
    # Check the status code to ensure a successful request
    if resp.status == 200:
        data = resp.data.decode('utf-8')
        return json.loads(data)
    elif resp.status == 400:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    else:
        print(f"HTTP Error: {resp.status}")
        return None

if __name__ == "__main__":
    # Create a PoolManager object
    http = urllib3.PoolManager()

    # TO PUBLISH AN EVENT
    # 1. CREATE AN EVENT
    # 2. CREATE A TICKET CLASS TO EVENT
    # 3. PUBLISH EVENT

    # create_event(http, organization_id, event_details)
    # create_ticket_class(http, event_id, example_free_ticket_class)
    # create_ticket_class(http, event_id, example_paid_ticket_class)
    # publish_event(http, event_id)

    
    


