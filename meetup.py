import urllib.request
import urllib.parse
import certifi
import ssl
import json
import os

MEETUP_BASE_URL = 'https://api.meetup.com/gql'

# Venue id for Bentley
BENTLEY_VENUE_ID = '27311786' 

# Social Coding Constants
SOCIAL_GROUP_ID = '37320082'
SOCIAL_GROUP_URL = 'social-coding'

def get_access_token(client_id, client_secret, redirect_uri, authorization_code):
    # Define the token endpoint URL
    token_url = 'https://secure.meetup.com/oauth2/access'

    # Create a dictionary with the request parameters
    token_params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': authorization_code,
    }

    # Encode the parameters in the application/x-www-form-urlencoded format
    data = urllib.parse.urlencode(token_params).encode('utf-8')

    # Use the certifi certificate bundle
    # Required as the redirect uri does not have a SSL cert
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Create a POST request
    req = urllib.request.Request(token_url, data=data)

    # Make the POST request to obtain the access token
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        data = resp.read().decode('utf-8')
        response_json = json.loads(data)
        access_token = response_json.get('access_token')
        token_type = response_json.get('token_type')
        expires_in = response_json.get('expires_in')
        refresh_token = response_json.get('refresh_token')
        
    if resp.status != 200:
        return print(f"HTTP Error: {resp.status} - {data}")
    return print(access_token, refresh_token)

def get_new_token(client_id, client_secret, refresh_token):
    # Define the token endpoint URL
    token_url = 'https://secure.meetup.com/oauth2/access'

    # Create a dictionary with the request parameters
    token_params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    # Encode the parameters in the application/x-www-form-urlencoded format
    data = urllib.parse.urlencode(token_params).encode('utf-8')

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Create a POST request
    req = urllib.request.Request(token_url, data=data)

    # Make the POST request to obtain the new access token
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        data = resp.read().decode('utf-8')
        response_json = json.loads(data)
        access_token = response_json.get('access_token')
        token_type = response_json.get('token_type')
        expires_in = response_json.get('expires_in')
        refresh_token = response_json.get('refresh_token')
            
    if resp.status != 200:
        print(f"HTTP Error: {resp.status} - {data}")
        return None
    
    return access_token, refresh_token

def get_group_id(access_token, urlname):
    # Define the GraphQL query for fetching a group by urlname
    query = '''
    query($urlname: String!) {
        groupByUrlname(urlname: $urlname) {
            id
        }
    }
    '''

    # Define the query variables
    variables = {
        "urlname": urlname
    }

    # Define the request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Create the request payload
    request_data = {
        'query': query,
        'variables': variables
    }

    data = json.dumps(request_data).encode('utf-8')

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Create the request
    req = urllib.request.Request(MEETUP_BASE_URL, data=data, headers=headers, method='POST')

    # Make the GraphQL request
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        resp_data = resp.read().decode('utf-8')
        result = json.loads(resp_data)
    if resp.status != 200:
        return print(f"HTTP Error: {resp.status} - {resp.data}")
    return print(result)

def get_event_by_id(access_token, event_id):
    # Define the GraphQL query
    query = '''
    query ($eventId: ID) {
        event(id: $eventId) {
            title
            description
            dateTime
            venue{
                name
                address
                city
                state
                country
            }
        }
    }
    '''

    # Define the GraphQL variables
    variables = json.dumps({'eventId': event_id})

    # Define the request data
    request_data = {
        'query': query,
        'variables': variables,
    }

    # Define the request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    data = json.dumps(request_data).encode('utf-8')

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Create the request
    req = urllib.request.Request(MEETUP_BASE_URL, data=data, headers=headers, method='POST')

    # Make the GraphQL request
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        resp_data = resp.read().decode('utf-8')
        result = json.loads(resp_data)
    if resp.status != 200:
        return print(f"HTTP Error: {resp.status} - {resp.data}")
    return print(result)
    
def create_venue(access_token, group_id, name, address, city, country, state=None):
    # Define the GraphQL mutation for creating a venue
    mutation = '''
    mutation($input: CreateVenueInput!) {
        createVenue(input: $input) {
            venue {
                id
            }
            errors {
                message
                code
                field
            }
        }
    }
    '''

    # Define the variables for the GraphQL mutation
    variables = {
        "input": {
            "groupId": group_id,
            "name": name,
            "address": address,
            "city": city,
            "country": country,
            "state": state if state else None
        }
    }

    # Construct the GraphQL request data
    request_data = {
        'query': mutation,
        'variables': variables
    }

    # Define the request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    data = json.dumps(request_data).encode('utf-8')

    # Use the certifi certificate bundle
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Create the request
    req = urllib.request.Request(MEETUP_BASE_URL, data=data, headers=headers, method='POST')

    # Make the GraphQL request to create the venue
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        resp_data = resp.read().decode('utf-8')
        result = json.loads(resp_data)
    
    if result.get('data', {}).get('createVenue', {}).get('venue') is not None:
        venue_id = result['data']['createVenue']['venue']['id']
        print(f"Venue created successfully with ID: {venue_id}")
        return venue_id
    else:
        errors = result.get('data', {}).get('createVenue', {}).get('errors', [])
        for error in errors:
            print(f"Error: {error['message']} (Code: {error['code']}, Field: {error['field']})")

def create_event(access_token, group_urlname, title, description, start_datetime, duration, location_id):
    # Define the GraphQL mutation for creating an event
    mutation = '''
    mutation($input: CreateEventInput!) {
        createEvent(input: $input) {
            event {
                id
            }
            errors {
                message
                code
                field
            }
        }
    }
    '''

    # Define the variables for the GraphQL mutation
    variables = {
        "input": {
            "groupUrlname": group_urlname,
            "title": title,
            "description": description,
            "startDateTime": start_datetime,
            "duration": duration,
            "venueId": location_id,
            "publishStatus": "DRAFT" # Can be changed to "PUBLISHED" 
        }
    }

    # Construct the GraphQL request data
    request_data = {
        "query": mutation,
        "variables": variables
    }

    # Define the request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = json.dumps(request_data).encode('utf-8')

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Create the request
    req = urllib.request.Request(MEETUP_BASE_URL, data=data, headers=headers, method='POST')

    # Make the GraphQL request
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        resp_data = resp.read().decode('utf-8')
        result = json.loads(resp_data)

    if result.get('data', {}).get('createEvent', {}).get('event') is not None:
        event_id = result['data']['createEvent']['event']['id']
        print(f"Event created successfully with ID: {event_id}")
        return event_id
    else:
        errors = result.get('data', {}).get('createEvent', {}).get('errors', [])
        for error in errors:
            print(f"Error: {error['message']} (Code: {error['code']}, Field: {error['field']})")

def publish_event(access_token, event_id):
    # Define the GraphQL mutation query
    mutation = """
    mutation($input: PublishEventDraftInput!) {
      publishEventDraft(input: $input) {
        event {
          id
        }
        errors {
          message
          code
          field
        }
      }
    }
    """

    # Define the variables for the mutation
    variables = {
        "input": {
            "eventId": event_id,
        }
    }

    # Create the GraphQL request payload
    request_data = {
        "query": mutation,
        "variables": variables
    }

    # Set the headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Encode the request_data as JSON
    data = json.dumps(request_data).encode("utf-8")

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Create a POST request
    req = urllib.request.Request(MEETUP_BASE_URL, data=data, headers=headers, method='POST')

    # Make the POST request to publish the event
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        resp_data = resp.read().decode('utf-8')
        result = json.loads(resp_data)
    
    if result.get('data', {}).get('publishEventDraft', {}).get('event') is not None:
        event_id = result['data']['publishEventDraft']['event']['id']
        print(f"Event published successfully with ID: {event_id}")
        return event_id
    else:
        errors = result.get('data', {}).get('publishEventDraft', {}).get('errors', [])
        for error in errors:
            print(f"Error: {error['message']} (Code: {error['code']}, Field: {error['field']})")

def announce_event(access_token, event_id):
    # Define the GraphQL mutation query
    mutation = """
    mutation($input: AnnounceEventInput!) {
      announceEvent(input: $input) {
        event {
          id
        }
        errors {
          message
          code
          field
        }
      }
    }
    """

    # Define the variables for the mutation
    variables = {
        "input": {
            "eventId": event_id,
        }
    }

    # Create the GraphQL request payload
    request_data = {
        "query": mutation,
        "variables": variables
    }

    # Set the headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Encode the request_data as JSON
    data = json.dumps(request_data).encode("utf-8")

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Create a POST request
    req = urllib.request.Request(MEETUP_BASE_URL, data=data, headers=headers, method='POST')

    # Make the POST request to publish the event
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        resp_data = resp.read().decode('utf-8')
        result = json.loads(resp_data)
    
    if result.get('data', {}).get('announceEvent', {}).get('event') is not None:
        event_id = result['data']['announceEvent']['event']['id']
        print(f"Event announced successfully with ID: {event_id}")
        return event_id
    else:
        errors = result.get('data', {}).get('announceEvent', {}).get('errors', [])
        for error in errors:
            print(f"Error: {error['message']} (Code: {error['code']}, Field: {error['field']})")
    
def upload_img(access_token, image_filename):
    # Define the GraphQL mutation for uploading an image
    mutation = '''
    mutation($input: ImageUploadInput!) {
        uploadImage(input: $input) {
            uploadUrl
            image {
                id
                baseUrl
                preview
            }
            imagePath
        }
    }
    '''

    # Define the variables for the GraphQL mutation
    variables = {
        "input": {
            "groupId": SOCIAL_GROUP_ID,
            "photoType": "GROUP_PHOTO",
            "fileName": image_filename,
            "contentType": "JPEG"
        }
    }

    # Construct the GraphQL request data
    request_data = {
        'query': mutation,
        'variables': variables
    }

    # Define the request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    data = json.dumps(request_data).encode('utf-8')

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Create the request
    req = urllib.request.Request(MEETUP_BASE_URL, data=data, headers=headers, method='POST')

    # Make the GraphQL request to upload the image
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        resp_data = resp.read().decode('utf-8')
        result = json.loads(resp_data)

    if resp.status != 200:
        print(f"HTTP Error: {resp.status}")
    else:
        upload_url = result.get('data', {}).get('uploadImage', {}).get('uploadUrl')
        image_id = result.get('data', {}).get('uploadImage', {}).get('image', {}).get('id')
        image_base_url = result.get('data', {}).get('uploadImage', {}).get('image', {}).get('baseUrl')
        print(f"Image uploaded successfully with ID: {image_id}")
        print(f"base URL: {image_base_url}")
        print(f"Upload URL: {upload_url}")
        return upload_url, image_id
    
    print(result)

def add_img_event(access_token, event_id, img_id):
    # Define the GraphQL mutation query
    mutation = """
    mutation($input: EditEventInput!) {
      editEvent(input: $input) {
        event {
          id
        }
        errors {
          message
          code
          field
        }
      }
    }
    """

    # Define the variables for the mutation
    variables = {
        "input": {
            "eventId": event_id,
            "featuredPhotoId": img_id
        }
    }

    # Create the GraphQL request payload
    request_data = {
        "query": mutation,
        "variables": variables
    }

    # Set the headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Encode the request_data as JSON
    data = json.dumps(request_data).encode("utf-8")

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Create a POST request
    req = urllib.request.Request(MEETUP_BASE_URL, data=data, headers=headers, method='POST')

    # Make the POST request to publish the event
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        resp_data = resp.read().decode('utf-8')
        result = json.loads(resp_data)
    
    if result.get('data', {}).get('editEvent', {}).get('event') is not None:
        event_id = result['data']['editEvent']['event']['id']
        print(f"Event edited successfully with ID: {event_id}")
        return event_id
    else:
        errors = result.get('data', {}).get('editEvent', {}).get('errors', [])
        for error in errors:
            print(f"Error: {error['message']} (Code: {error['code']}, Field: {error['field']})")

def quick_create_event(client_id, client_secret, redirect_uri, authorization_code, title, description, start_datetime, duration ):

    # Get an access token to perform methods
    access_token, refresh_token = get_access_token(client_id, client_secret, redirect_uri, authorization_code)
 
    new_event_id = create_event(access_token, SOCIAL_GROUP_URL, title, description, start_datetime, duration, BENTLEY_VENUE_ID)

    publish_event(access_token, new_event_id)
    # announce_event(access_token, new_event_id)

if __name__ == "__main__":

    # Retrieve the values of an environment variables
    meetup_client_id = os.environ['MEETUP_CLIENT_ID']
    meetup_client_secret = os.environ['MEETUP_CLIENT_SECRET']
    meetup_auth_code = os.environ['MEETUP_AUTH_CODE']
    redirect_uri = 'http://localhost:8888/account-setup'

    # Format for duration is as follows ISO 8601 : PT1H30M
    # Format for start: 2023-11-20T17:00 takes the group's location as a reference for timezone

    quick_create_event(meetup_client_id, meetup_client_secret, redirect_uri, meetup_auth_code, "TEST API", "Testing API", "2023-11-20T17:00", "PT1H30M")


