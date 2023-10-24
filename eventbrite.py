import urllib3
import json
import os

# EVENTBRITE API SCRIPT

EVENTBRITE_API_BASE_URL = "https://www.eventbriteapi.com/v3/"

# Examples
example_event_details = {
"event": {
    "name": {
        "html": f"<p>API TEST</p>"
        },
    "description": {
        "html": f"<p>API TEST DESC</p>"
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
    "online_event": False,
    "organizer_id": "",
    "listed": False,
    "shareable": False,
    "invite_only": False,
    "show_remaining": True,
    "password": "12345",
    "capacity": 100,
    "is_reserved_seating": False,
    "is_series": False,
    "show_pick_a_seat": False,
    "show_seatmap_thumbnail": False,
    "show_colors_in_seatmap_thumbnail": False,
    "locale": "en_AU"
    }
}

paid_ticket_details = {
"ticket_class": 
    {
    "name": "API Test1",
    "free": "false",
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
    "sales_start": "2023-11-09T08:00:00Z",
    "sales_end": "2023-11-11T03:00:00Z",
    "cost": "AUD,2000",
    }
}

free_ticket_details = {
"ticket_class": 
    {
    "name": "API Test1",
    "free": "false",
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
    "sales_start": "2023-11-09T08:00:00Z",
    "sales_end": "2023-11-11T03:00:00Z",
    }
}

def get_organization(http, eventbrite_api_token):
    url = f"{EVENTBRITE_API_BASE_URL}users/me/organizations/"
    headers = {
        'Authorization': eventbrite_api_token
    }

    # Make the GET request
    resp = http.request('GET', url, headers=headers)

    # Check the status code to ensure a successful request
    if resp.status != 200:
        print(f"HTTP Error: {resp.status}")
        
    data = resp.data.decode('utf-8')
    print(data)
    return data

def get_event_by_id(http,eventbrite_api_token, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/"
    headers = {
        'Authorization': eventbrite_api_token
    }

    # Make the GET request
    resp = http.request('GET', url, headers=headers)

    # Check the status code to ensure a successful request
    if resp.status != 200:
        print(f"HTTP Error: {resp.status}")
        
    data = resp.data.decode('utf-8')
    print(data)
    return data

def get_events_by_organization(http,eventbrite_api_token, organization_id):
    url = f"{EVENTBRITE_API_BASE_URL}organizations/{organization_id}/events"
    headers = {
        'Authorization': eventbrite_api_token
    }

    # Make the GET request
    resp = http.request('GET', url, headers=headers)

    # Check the status code to ensure a successful request
    if resp.status != 200:
        print(f"HTTP Error: {resp.status}")
    data = resp.data.decode('utf-8')
    print(data)
        
def create_event(http, eventbrite_api_token, organization_id ,event_details):
    url = f"{EVENTBRITE_API_BASE_URL}organizations/{organization_id}/events/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Make the POST request
    resp = http.request('POST', url, headers=headers, body=event_details)


    # Check the status code to ensure a successful request
    if resp.status != 200:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    data = resp.data.decode('utf-8')
    print(data)
    return json.loads(data)


def update_event(http, eventbrite_api_token, event_id, event_details):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Make the POST request
    resp = http.request('POST', url, headers=headers, body=event_details)

    # Check the status code to ensure a successful request
    if resp.status != 200:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    data = resp.data.decode('utf-8')
    return json.loads(data)

def delete_event(http, eventbrite_api_token, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Make the DELETE request
    resp = http.request('DELETE', url, headers=headers)

    if resp.status != 200:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    
    # A successful DELETE request should return a 200 status code for Eventbrite
    return print({"message": "Event deleted successfully", "status_code": resp.status})

def unpublish_event(http, eventbrite_api_token, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/unpublish/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }
    # Make the POST request
    resp = http.request('POST', url, headers=headers)

    # Check the status code to ensure a successful request

    if resp.status != 200:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
            }
    data = resp.data.decode('utf-8')
    return {"message": "Event unpublished successfully", "status_code": resp.status}, json.loads(data)
    
def publish_event(http, eventbrite_api_token, event_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/publish/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Make the POST request
    resp = http.request('POST', url, headers=headers)

    if resp.status != 200:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
            }
    data = resp.data.decode('utf-8')
    print({"message": "Event: {} published successfully".format(event_id), "status_code": resp.status})
    return json.loads(data)

def create_ticket_class(http, eventbrite_api_token, event_id, ticket_details):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/ticket_classes/"
    headers = {
    'Authorization': eventbrite_api_token,
    'Content-Type': 'application/json'
    }

    # Make the POST request
    resp = http.request('POST', url, headers=headers, body=ticket_details)
    
    # Check the status code to ensure a successful request


    if resp.status != 200:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
            }

    data = resp.data.decode('utf-8')
    return json.loads(data)
    
def get_ticket_class_by_id(http, eventbrite_api_token, event_id, ticket_class_id):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/ticket_classes/{ticket_class_id}/"
    headers = {
    'Authorization': eventbrite_api_token,
    }

    # Make the GET request
    resp = http.request('GET', url, headers=headers)

    # Check the status code to ensure a successful request
    if resp.status != 200:
        print(f"HTTP Error: {resp.status}")

    data = resp.data.decode('utf-8')
    print(data)
    return data

def update_ticket_class(http, eventbrite_api_token, event_id, ticket_class_id, ticket_details):
    url = f"{EVENTBRITE_API_BASE_URL}events/{event_id}/ticket_classes/{ticket_class_id}/"
    headers = {
        'Authorization': eventbrite_api_token,
        'Content-Type': 'application/json'
    }
    
    # Make the POST request
    resp = http.request('POST', url, headers=headers, body=ticket_details)
    
    if resp.status != 200:
        error_data = json.loads(resp.data.decode('utf-8'))
        error_detail = error_data.get('error_detail', {})
        return {
            "error": error_data.get('error', 'Unknown Error'),
            "error_description": error_data.get('error_description', 'An error occurred'),
            "error_detail": error_detail,
            "status_code": resp.status
        }
    data = resp.data.decode('utf-8')
    return json.loads(data)

def quick_create_event(http, eventbrite_api_token, organization_id, title, description, cost_cents=None, publish=True):
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
                "timezone": "UTC",
                "utc": "2023-11-12T02:00:00Z"
            },
            "end": {
                "timezone": "UTC",
                "utc": "2023-11-30T02:00:00Z"
            },
            "currency": "AUD",
            "online_event": False,
            "organizer_id": "",
            "listed": False,
            "shareable": False,
            "invite_only": False,
            "show_remaining": True,
            "password": "12345",
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
    new_event = create_event(http,eventbrite_api_token, organization_id, event_detail_json)

    # Extract the event_id from the response
    event_id = new_event['id']

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
            "sales_start": "2023-11-09T08:00:00Z",
            "sales_end": "2023-11-11T03:00:00Z",
            **({"cost": f"AUD,{cost_cents}", "free": "false"} if cost_cents is not None else {'free': "true"}),
        }
    }

    # Convert the ticket class details to a JSON string
    ticket_detail_json = json.dumps(ticket_detail)

    # Create the ticket class
    new_tickets = create_ticket_class(http, eventbrite_api_token, event_id, ticket_detail_json)
    if publish:
        publish_event(http,eventbrite_api_token, event_id)
    return new_event, new_tickets

if __name__ == "__main__":

    # Retrieve the values of an environment variables
    eventbrite_api_token = os.environ.get('EVENTBRITE_API_TOKEN')
    organization_id = os.environ.get('EVENTBRITE_ORGANIZATION_ID')

    # Create a PoolManager object
    http = urllib3.PoolManager()

    # quick_create_event(http, eventbrite_api_token, organization_id, "API-TEST-01", "API-TEST-DESCRIPTION", 2000, True)

    # TO PUBLISH AN EVENT
    # 1. CREATE AN EVENT
    # 2. CREATE A TICKET CLASS TO EVENT
    # 3. PUBLISH EVENT

    # create_event(http, organization_id, event_details)
    # create_ticket_class(http, event_id, example_free_ticket_class)
    # create_ticket_class(http, event_id, example_paid_ticket_class)
    # publish_event(http, event_id)

    
    


