import os
import flask
import requests
import pickle

import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from flask import Blueprint, redirect, url_for

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
WEB_CLIENT_SECRETS_FILE = "web_google_client.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://mail.google.com/']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'

g_oauth = Blueprint('g_oauth', __name__)


# To-Do:
# 1. Create function if pickle exists (maybe add it to serviceBuilder)
#   - Use this function separately within flaskMain to check if logged in
#   - It should redirect to / page after authorization
#   - if no (all things in serviceBuilder (can be another function), then go to authentication) and maybe flask message for now?
#      else just continue with all the functionality
# 2. Service builder should return service (keep it in google auth)


def authCheck(credsreturn=False):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

        return True

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

            return True

        else:
            print("into auth")

            # Go to authorize method to get credentials and come back to this step
            return redirect('/authorize')

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    if credsreturn:
        return creds

    return False


def authLogin(credsreturn=False):
    if authCheck() == False:
        return redirect('/authorize')

    if credsreturn:
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
            return creds

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

        return True

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            return True

        else:
            print("into auth")

            # Go to authorize method to get credentials and come back to this step
            return redirect('/authorize')

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    if credsreturn:
        return creds
    return


@g_oauth.route('/builder')
def serviceBuilder():
    print("in service")

    # global authlock
    # authlock = True

    creds = authCheck(credsreturn=True)

    service = build(
        API_SERVICE_NAME, API_VERSION, credentials=creds)

    authlock = False

    return service


@g_oauth.route('/authorize')
def authorize():
    print("in auth")

    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = Flow.from_client_secrets_file(
        WEB_CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for('g_oauth.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state
    print("into authorization")
    print(authorization_url)

    # return f'<a href="{authorization_url}" target="_blank">Link</a>'
    return redirect(authorization_url)


# make oauth2callback but open original "/" page?

@g_oauth.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = Flow.from_client_secrets_file(
        WEB_CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('g_oauth.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    creds = flow.credentials

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    # flask.session['credentials'] = credentials_to_dict(credentials)
    return service_builder()
    # return redirect(url_for('g_oauth.serviceBuilder'))


'''
@app.route('/revoke')
def revoke():
    if 'credentials' not in flask.session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
        params={'token': credentials.token},
        headers = {'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return('Credentials successfully revoked.' + print_index_table())
    else:
        return('An error occurred.' + print_index_table())


@app.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return ('Credentials have been cleared.<br><br>' +
        print_index_table())


def credentials_to_dict(credentials):
    return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def print_index_table():
    return ('<table>' +
          '<tr><td><a href="/test">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')

'''

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Specify a hostname and port that are set as a valid redirect URI
    # for your API project in the Google API Console.
    app.run('localhost', 8080, debug=True)