import api_request
import db_connector
import create_db
import insert_records

# meetings -> sessions -> drivers-> the rest
 
def data_to_db():

    # establishing the connection to the DB and creating the tables
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

        year = 2023

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
    data_to_db()
