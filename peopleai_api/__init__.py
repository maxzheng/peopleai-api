import json
import time

import requests


class DidNotCompleteError(Exception):
    """ Raised if a job did not complete successfully """


class PeopleAIClient:
    AUTH_PATH = '/auth/v1/tokens'
    EXPORT_ACTIVITIES_PATH = '/pull/v1/export/activities/jobs'

    def __init__(self, api_key, api_secret, api_endpoint='https://api.people.ai'):
        """
        :param str api_key: Public identifier for the API key
        :param str api_secret: Secret only known to the application and authorization server
        :param str api_endpoint: People.ai API endpoint
        """
        #: Public identifier for the API key
        self.api_key = api_key

        #: Secret only known to the application and authorization server
        self.api_secret = api_secret

        #: People.ai API endpoint
        self.api_endpoint = api_endpoint

        #: JWT token for OAuth
        self.access_token = None

        #: Number of seconds before the access token expires
        self.token_expires_in = 0

    def _request(self, method, path, params=None):
        """
        Send a request to the given path with the given params

        :param str method: Method for the request: GET, OPTIONS, HEAD, POST, PUT, PATCH, or DELETE.
        :param str path: Post to path
        :param dict params: Parameters to post
        :return: JSON result
        """
        if self.token_expires_in < 10:
            auth_data = {'grant_type': 'client_credentials', 'client_id': self.api_key,
                         'client_secret': self.api_secret}
            r = requests.post(self.api_endpoint + self.AUTH_PATH, data=auth_data).json()
            self.access_token = r['access_token']
            self.token_expires_in = r['expires_in']

        headers = {'Authorization': f'Bearer {self.access_token}'}
        resp = requests.request(method, self.api_endpoint + path, json=params, headers=headers)

        try:
            return resp.json()

        except json.decoder.JSONDecodeError:  # When output_format = JSONLines
            return resp.text

    def get(self, path, params=None):
        """
        Send a GET request to the given path with the given params

        :param str path: Path to get
        :param dict params: Parameters to get
        :return: JSON result
        """
        return self._request('GET', path, params=params)

    def post(self, path, params=None):
        """
        Send a POST request to the given path with the given params

        :param str path: Path to post
        :param dict params: Parameters to post
        :return: JSON result
        """
        return self._request('POST', path, params=params)

    def start_activities_export(self, **params):
        """
        Start an export job for activities

        :param dict params: Export parameters:

            start_date: Start date of your data retrieval, starting at 0:00 AM UTC of that day
                        Acceptable values follow “yyyy-MM-dd” format
            end_date: End date of your data retrieval, ending at 11:59 PM UTC of that day
                      Acceptable values follow “yyyy-MM-dd” format
            activity_type: Activity types to include in the export.
                           Acceptable values are:
                               "email": Returns only emails
                               "meeting": Returns only meetings
                               "call": Returns only calls
                               "all": Returns all activity types
            output_format: Output data structure.
                           Acceptable values are:
                               "JSON": Single JSON object
                               "JSONLines": Each line is its own JSON object
            export_type: Acceptable values are:
                             "snapshot": All activities with an activity date between the start_date and end_date
                                         parameters. This export type is meant to build a base of historical
                                         activities.
                             "delta": All activities that were processed between the start_date and end_date
                                      parameters. This export type is meant for recurring jobs to capture updates
                                      in calendar events and pick up new users’ data.
        :return: Job Id
        """
        r = self.post(self.EXPORT_ACTIVITIES_PATH, params=params)
        return r['job_id']

    def check_activities_export(self, job_id, until_completed=False, delay=60):
        """
        Check the status of the export

        :param int job_id: Job ID to check the status for
        :param bool until_completed: Keep checking until the job is completed. If it failed or cancelled, an exception
                                     will be raised.
        :param int delay: Number of seconds to wait before checking again if until_completed is True
        :raises DidNotCompleteError: If the job status becomes Canceled or Failed
        """
        while True:
            status = self.get(self.EXPORT_ACTIVITIES_PATH + '/' + str(job_id))

            if not until_completed or status['state'] == 'Completed':
                break

            if status['state'] in ['Canceled', 'Failed']:
                raise DidNotCompleteError('Job state is ' + status['state'])

            time.sleep(delay)

        return status['state']

    def download_activities_export(self, job_id, dest):
        """
        Download the export

        :param int job_id: Job ID to download data for
        :param str dest: Destination file to save data to.
        """
        data = self.get(self.EXPORT_ACTIVITIES_PATH + '/' + str(job_id) + '/data')
        with open(dest, 'w') as fp:
            fp.write(data)
        print('Saved to', dest)
