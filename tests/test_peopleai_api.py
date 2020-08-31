import httpretty
from utils.fs import in_temp_dir

from peopleai_api import PeopleAIClient


@httpretty.activate
def test_peopleai_api():
    # Auth
    httpretty.register_uri(
        httpretty.POST, 'https://api.people.ai/auth/v1/tokens',
        body='{"access_token": "shiny-token", "expires_in": 600}')

    # Start
    httpretty.register_uri(
        httpretty.POST, 'https://api.people.ai/pull/v1/export/activities/jobs',
        body='{"job_id": 123}')

    # Check
    httpretty.register_uri(
        httpretty.GET, 'https://api.people.ai/pull/v1/export/activities/jobs/123',
        body='{"state": "Completed"}')

    # Download
    httpretty.register_uri(
        httpretty.GET, 'https://api.people.ai/pull/v1/export/activities/jobs/123/data',
        body='{"campaigns":[]}\n{"crm_status":{"matched_to":"account","pushed":false}}')

    client = PeopleAIClient('<api_key>', '<api_secret>')

    job_id = client.start_activities_export(start_date='2020-08-06', end_date='2020-08-06', activity_type='all',
                                            output_format='JSONLines', export_type='delta')

    state = client.check_activities_export(job_id, until_completed=True, delay=0.1)
    assert state == 'Completed'

    with in_temp_dir():
        client.download_activities_export(job_id, 'export.json')
        content = open('export.json').read()
        assert content == '{"campaigns":[]}\n{"crm_status":{"matched_to":"account","pushed":false}}'
