import requests
import time
import warnings
from datetime import datetime, timedelta
import pytz
import re

warnings.filterwarnings("ignore")

BASE_URL = "https://ae1hvrltv01:4341/api/v6.1.0.36/hubs"
hub_url = ""
USERNAME = "user_name"
PASSWORD = "********"
TOKEN_URL = f"https://ae1hvrltv01:4341/auth/v1/password"


def generate_login_token():
    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }

    response = requests.post(TOKEN_URL, json=payload, verify=False)
    if response.status_code == 200:
        global token
        token = response.json().get("access_token")
    else:
        print(f"Failed to log in. Status Code: {response.status_code}, Error: {response.text}")

    global headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def get_hvr_hubs():
    """Fetch all hubs from HVR"""
    url = f"{BASE_URL}"
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            hubs = response.json()
            for hub in hubs:
				print(hub)
            return hubs.keys()
        else:
            print(f"Failed to fetch Hubs. Status Code: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print(f"Error fetching Hubs: {e}")
        return None

def get_hvr_jobs():
    """Fetch all jobs from HVR."""
    url = f"{hub_url}/jobs"
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            jobs = response.json()
            return jobs
        else:
            print(f"Failed to fetch jobs. Status Code: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return None
    
def get_hvr_channel_tables():
    """Fetch all Tables from HVR."""
    for channel in channels.keys():
        url = f"{hub_url}/definition/channels/{channel}/tables"
        tables = []
        try:
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                channel_details = response.json()
                for table in channel_details.keys():
                    tables.append(table)
                channels[channel]['tables'] = tables
            else:
                print(f"Failed to fetch channel_details. Status Code: {response.status_code}, Error: {response.text}")
        except Exception as e:
            print(f"Error fetching channel_details: {e}")
            return None

def get_hvr_channels(jobs):
    try:
        if jobs:
            for chan in jobs.keys():
                channel = chan.split("-")[0]
                if channel not in channels.keys():
                    channels[channel] = {}
        else:
            print("No Jobs found to get channels or an error occurred.")
        del channels["hvrstats"]
    except Exception as e:
        print(f"Error in fetching channels: {e}")

def get_hvr_job_status(jobs):
    if jobs:
        label = {'activate': 'activate', 'cap': 'capture', 'integ': 'integrate', 'refr': 'refresh'}
        for channel in channels.keys():
            channels[channel]['jobs'] = {'activate': '', 'capture': '', 'integrate': '', 'refresh': ''}
            for job, status in jobs.items():
                vals = job.split("-")
                if len(vals) > 1:
                    val = vals[1]
                    if (channel in job) and (val in label.keys()):
                        channels[channel]['jobs'][label[val]] = status['state']

def get_hvr_locations():
    for channel in channels.keys():
        url = f"{hub_url}/query/channels/{channel}/locs"
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            activate = response.json()
            channels[channel]['locs'] = activate

def get_hvr_compare_event_logs():
    url = f"{hub_url}/events"
    query = {'type': 'Compare', 'ev_tstamp_begin': formatted_time}
    response = requests.get(url, query, headers=headers, verify=False)
    if response.status_code == 200:
        activate = response.json()
        for event_id in activate:
            url = f"{hub_url}/events/{event_id}/log"
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                event_log = response.text
                lines = event_log.splitlines()
                for line in lines:
                    if "differ by" in line or 'is different in' in line:
                        identifier = line.split(":")[4].strip().split()[-1]
                        parts = line.split(":")
                        last_part = parts[-1].strip()                                
                        if "This row-wise compare took" in last_part:
                            last_part = last_part.split("This row-wise compare took")[0].strip()
                        elif "This bulk compare took" in last_part:
                            last_part = last_part.split("This bulk compare took")[0].strip()


def get_hvr_job_duration():
    url = f"{hub_url}/events"
    query = {'ev_tstamp_begin': formatted_time}
    response = requests.get(url, query, headers=headers, verify=False)
    if response.status_code == 200:
        activate = response.json()
        for event_id in activate:
            url = f"{hub_url}/events/{event_id}/log"
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                event_log = response.text
                lines = event_log.splitlines()
                for line in lines:
                    if "completed. (elapsed=" in line:
                        elapsed_time = line.split("elapsed=")[1].split("s")[0]
                        if 'h' in elapsed_time:
                            hours, minutes_seconds = elapsed_time.split("h")
                            minutes, seconds = minutes_seconds.split("m")
                            total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
                        elif 'm' in elapsed_time:
                            minutes, seconds = elapsed_time.split("m")
                            total_seconds = int(minutes) * 60 + float(seconds)
                        elif '.' in elapsed_time:
                            total_seconds = elapsed_time
                        identifier = line.split(":")[4].strip().split()[-1]
						

def main():
	generate_login_token()
	hubs = get_hvr_hubs()
	global channels
	channels = {}
	global hub_url
	global formatted_time
	for hub in hubs:
		hub_url = f"{BASE_URL}/{hub}"
		now = datetime.now(pytz.utc)
		one_hour_before = (now - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
		formatted_time = one_hour_before.strftime('%Y-%m-%dT%H:%M:%S.') + str(one_hour_before.microsecond // 1000).zfill(3) + 'Z'
		jobs = get_hvr_jobs()
		get_hvr_channels(jobs)
		get_hvr_job_status(jobs)
		get_hvr_channel_tables()
		get_hvr_locations()
		get_hvr_compare_event_logs()
		get_hvr_job_duration()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in Main Script: {e}")
    finally:
        print("Stopped")
