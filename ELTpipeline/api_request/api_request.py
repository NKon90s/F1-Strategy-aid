import requests
import time
from typing import Any
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
 
class APIrequest:

    def __init__(self, year):
        self.year = year
        

    def fetch_sessions(self,year: int): 
        """
        Fetches all the data from the sessions endpoint.

        :param year: The request will fetch all the session data from the specified year
        """

        sessions = []
        session_url = f"https://api.openf1.org/v1/sessions?year={year}"
        try:
            response = requests.get(session_url)
            response.raise_for_status()
            print(f"Fetching sessions for year {year} initiated successfully.")

            sessions.extend(response.json())

        except requests.exceptions.RequestException as e:
            print(f"An error occured: {e}")
            raise

        return sessions
    
  
    # Selecting only race sessions
    def fetch_race_sessions(self, year: int):
        """Fetches only the race sessions from all of the sessions if they are not cancelled"""

        session_key = self.fetch_sessions(year)
        race_sessions = [session for session in session_key if session["session_type"] == "Race" and not session["is_cancelled"]]
        return [session['session_key'] for session in race_sessions]
    


    def fetch_q_sessions(self, year: int):
        """Fetches only the qualifying sessions from all of the sessions if they are not cancelled"""
        session_key = self.fetch_sessions(year)
        q_sessions = [session for session in session_key if session["session_type"] == "Qualifying" and not session["is_cancelled"]]
        return [session["session_key"] for session in q_sessions]


    def create_safe_session(self):

        """Creates a requests session with integrated retry logic for 429 errors."""

        session = requests.Session()
        # Retries up to 5 times. wait = backoff_factor * (2 ** (retry_number - 1))
        retry_strategy = Retry(
            total=5,
            backoff_factor=1.5, 
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session
    
    

    # fetching car data from the API
    def fetch_f1_data(self, endpoint: str, query_params_list, req_per_window=25, window_seconds=10.0):
        """
        Fetches OpenF1 data chunk-by-chunk.
        
        :param endpoint: OpenF1 target endpoint (e.g., 'car_data', 'laps', 'location')
        :param query_params_list: List of dicts, each representing a single request's parameters
        :param req_per_window: Upper threshold under the 30-req limit (default 25)
        :param window_seconds: The 10-second rate limit block window
        """
        base_url = f"https://api.openf1.org/v1/{endpoint}"
        session = self.create_safe_session()
        all_responses = []

        # Calculate exact delay needed per request to stay under 30 req / 10 sec
        safe_delay = window_seconds / req_per_window  # ~0.4 seconds per call

        for index, params in enumerate(query_params_list):
            print(f"Request {index + 1}/{len(query_params_list)}: Filtering {endpoint} by {params}")
            
            start_time = time.time()
            
            try:
                response = session.get(base_url, params=params)
                response.raise_for_status()
                all_responses.extend(response.json())
            except requests.exceptions.RequestException as e:
                print(f"Failed pulling {endpoint} data for {params}: {e}")
                continue
            
            # Enforce rate regulation spacing
            elapsed = time.time() - start_time
            if elapsed < safe_delay:
                time.sleep(safe_delay - elapsed)
                
        return all_responses
 

