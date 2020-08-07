peopleai-api
============

Python library to download `activities from People.ai's REST API
<https://help.people.ai/hc/en-us/articles/360042406653-Activity-APIs-Resources>`_

.. code-block:: python

    from peopleai_api import PeopleAIClient

    client = PeopleAIClient('<api_key>', '<api_secret>')

    job_id = client.start_activities_export(start_date='2020-08-06', end_date='2020-08-06', activity_type='all',
                                            output_format='JSONLines', export_type='delta')
    client.check_activities_export(job_id, until_completed=True)
    client.download_activities_export(job_id, '/tmp/peopleai-export.json')

Links & Contact Info
====================

| PyPI Package: https://pypi.org/project/peopleai-api/
| GitHub Source: https://github.com/maxzheng/peopleai-api
| Report Issues/Bugs: https://github.com/maxzheng/peopleai-api/issues
|
| Connect: https://www.linkedin.com/in/maxzheng
| Contact: maxzheng.os @t gmail.com
