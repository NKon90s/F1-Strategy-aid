import api_request
import db_connector
import create_db
import insert_records

# meetings -> sessions -> drivers-> the rest

def create_database():
    conn = db_connector.connect_to_db()
    try:
        create_table = create_db.CreateDB(conn)
        create_table.create_table_meetings(conn)
        create_table.create_table_sessions(conn)
        create_table.create_table_drivers(conn)
        create_table.create_table_intervals(conn)
        create_table.create_table_car_data(conn)
        create_table.create_table_laps(conn)
        create_table.create_table_pit(conn)
        create_table.create_table_position(conn)
        create_table.create_table_race_control(conn)
        create_table.create_table_starting_grid(conn)
        create_table.create_table_stints(conn)
        create_table.create_table_weather(conn)

    except Exception as e:
        print(f"ETL failed: {e}")
        raise
            
    finally:
        conn.close()
        print("Database connection closed.")
 
def data_to_db():

    # establishing the connection to the DB
    conn = db_connector.connect_to_db()
    try:
        year = 2023
        """
        f1_request = api_request.APIrequest(year)

        race_sessions = f1_request.fetch_race_sessions(year)
            

        meeting_workload = [{"year": year}]
        session_workload = [{"session_key": session_key} for session_key in race_sessions]

        # Fetching data with the API
        meeting_data = f1_request.fetch_f1_data(endpoint='meetings',query_params_list=meeting_workload)
        session_data = f1_request.fetch_f1_data(endpoint='sessions',query_params_list=session_workload)
        drivers_data = f1_request.fetch_f1_data(endpoint='drivers',query_params_list=session_workload)

        workload = [
            {
            "session_key": driver['session_key'], 
            "driver_number": driver['driver_number']
            }
            for driver in drivers_data
        ]
           
        interval_data = f1_request.fetch_f1_data(endpoint='intervals',query_params_list=workload)
        car_data = f1_request.fetch_f1_data(endpoint='car_data',query_params_list=workload)
        lap_data = f1_request.fetch_f1_data(endpoint='laps',query_params_list=workload)
        pit_data = f1_request.fetch_f1_data(endpoint='pit',query_params_list=workload)
        pos_data = f1_request.fetch_f1_data(endpoint='position',query_params_list=workload)
        race_data = f1_request.fetch_f1_data(endpoint='race_control',query_params_list=session_workload)
        grid_data = f1_request.fetch_f1_data(endpoint='starting_grid',query_params_list=workload)
        stint_data = f1_request.fetch_f1_data(endpoint='stints',query_params_list=workload)
        weather_data = f1_request.fetch_f1_data(endpoint='weather',query_params_list=session_workload)
        """

        meeting_data=[
            {
                "circuit_key": 61,
                "circuit_info_url": "https://api.multiviewer.app/api/v1/circuits/61/2026",
                "circuit_image": "https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/Singapore%20carbon.png",
                "circuit_short_name": "Singapore",
                "circuit_type": "Temporary - Street",
                "country_code": "SGP",
                "country_flag": "https://media.formula1.com/content/dam/fom-website/2018-redesign-assets/Flags%2016x9/singapore-flag.png",
                "country_key": 157,
                "country_name": "Singapore",
                "date_end": "2026-10-11T14:00:00+00:00",
                "date_start": "2026-10-09T09:30:00+00:00",
                "gmt_offset": "08:00:00",
                "is_cancelled": False,
                "location": "Marina Bay",
                "meeting_key": 1219,
                "meeting_name": "Singapore Grand Prix",
                "meeting_official_name": "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2026",
                "year": 2023
            }
            ]
        session_data=[
            {
                "circuit_key": 7,
                "circuit_short_name": "Spa-Francorchamps",
                "country_code": "BEL",
                "country_key": 157,
                "country_name": "Belgium",
                "date_end": "2023-07-29T15:35:00+00:00",
                "date_start": "2023-07-29T15:05:00+00:00",
                "gmt_offset": "02:00:00",
                "is_cancelled": False,
                "location": "Spa-Francorchamps",
                "meeting_key": 1219,
                "session_key": 9158,
                "session_name": "Sprint Qualifying",
                "session_type": "Sprint Qualifying",
                "year": 2023
            }
            ]
        drivers_data=[
                {
                    "broadcast_name": "M VERSTAPPEN",
                    "driver_number": 1,
                    "first_name": "Max",
                    "full_name": "Max VERSTAPPEN",
                    "headshot_url": "https://www.formula1.com/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/1col/image.png",
                    "last_name": "Verstappen",
                    "meeting_key": 1219,
                    "name_acronym": "VER",
                    "session_key": 9158,
                    "team_colour": "3671C6",
                    "team_name": "Red Bull Racing"
                }
            ]
        interval_data = [
            {
                "date": "2023-09-17T13:31:02.395000+00:00",
                "driver_number": 1,
                "gap_to_leader": 41.019,
                "interval": 0.003,
                "meeting_key": 1219,
                "session_key": 9158
            }
            ]
        car_data = [
            {
                "brake": 0,
                "date": "2023-09-15T13:08:19.923000+00:00",
                "driver_number": 1,
                "drs": 12,
                "meeting_key": 1219,
                "n_gear": 8,
                "rpm": 11141,
                "session_key": 9158,
                "speed": 315,
                "throttle": 99
            }]
        lap_data = [
            {
                "date_start": "2023-09-16T13:59:07.606000+00:00",
                "driver_number": 1,
                "duration_sector_1": 26.966,
                "duration_sector_2": 38.657,
                "duration_sector_3": 26.12,
                "i1_speed": 307,
                "i2_speed": 277,
                "is_pit_out_lap": False,
                "lap_duration": 91.743,
                "lap_number": 8,
                "meeting_key": 1219,
                "segments_sector_1": [2049, 2049, 2049, 2051, 2049, 2051, 2049, 2049],
                "segments_sector_2": [2049, 2049, 2049, 2049, 2049, 2049, 2049, 2049],
                "segments_sector_3": [2048, 2048, 2048, 2048, 2048, 2064, 2064, 2064],
                "session_key": 9158,
                "st_speed": 298
            }
        ]
        pit_data = [
            {
                "date": "2025-10-26T20:46:37.358000+00:00",
                "driver_number": 1,
                "lane_duration": 22.215,
                "lap_number": 31,
                "meeting_key": 1219,
                "pit_duration": 22.215,
                "session_key": 9158,
                "stop_duration": 2.2
            }]
        pos_data = [
            {
                "date": "2023-08-26T09:30:47.199000+00:00",
                "driver_number": 1,
                "meeting_key": 1219,
                "position": 2,
                "session_key": 9158
            }]
        race_data = [
            {
                "category": "Flag",
                "date": "2023-06-04T14:21:01+00:00",
                "driver_number": 1,
                "flag": "BLACK AND WHITE",
                "lap_number": 59,
                "meeting_key": 1219,
                "message": "BLACK AND WHITE FLAG FOR CAR 1 (VER) - TRACK LIMITS",
                "qualifying_phase": None,
                "scope": "Driver",
                "sector": 1,
                "session_key": 9158
            }
            ]
        grid_data = [
            {
                "position": 1,
                "driver_number": 1,
                "lap_duration": 76.732,
                "meeting_key": 1219,
                "session_key": 9158
            }]
        stint_data = [
            {
                "compound": "SOFT",
                "driver_number": 1,
                "lap_end": 20,
                "lap_start": 1,
                "meeting_key": 1219,
                "session_key": 9158,
                "stint_number": 1,
                "tyre_age_at_start": 3
            }]
        weather_data = [
            {
                "air_temperature": 27.8,
                "date": "2023-05-07T18:42:25.233000+00:00",
                "humidity": 58,
                "meeting_key": 1219,
                "pressure": 1018.7,
                "rainfall": 0,
                "session_key": 9158,
                "track_temperature": 52.5,
                "wind_direction": 136,
                "wind_speed": 2.4
            }
            ]

        # Inserting data into the created tables
        insert_table = insert_records.InsertRecords(conn, session_data, meeting_data, drivers_data, interval_data, car_data, lap_data, pit_data,
                        pos_data, race_data, grid_data, stint_data, weather_data)
            
        insert_table.insert_meeting_data(conn, meeting_data)
        insert_table.insert_session_data(conn, session_data)
        insert_table.insert_drivers_data(conn, drivers_data)
        insert_table.insert_interval_data(conn, interval_data)
        insert_table.insert_car_data(conn, car_data)
        insert_table.insert_laps_data(conn, lap_data)
        insert_table.insert_pit_data(conn, pit_data)
        insert_table.insert_position_data(conn, pos_data)
        insert_table.insert_race_control_data(conn, race_data)
        insert_table.insert_starting_grid_data(conn, grid_data)
        insert_table.insert_stint_data(conn, stint_data)
        insert_table.insert_weather_data(conn, weather_data)

    except Exception as e:
        print(f"ETL failed: {e}")
        raise
                
    finally:
        conn.close()
        print("Database connection closed.")
   
    
if __name__ == "__main__":
    create_database()
    data_to_db()
