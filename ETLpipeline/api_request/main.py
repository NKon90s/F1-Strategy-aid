from . import api_request
from . import db_connector
from . import create_db
from . import insert_records

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
        year = 2025
        
        f1_request = api_request.APIrequest(year)
        # Inserting data into the created tables
        insert_table = insert_records.InsertRecords(conn)

        race_sessions = f1_request.fetch_race_sessions(year)

        qualifying_sessions = f1_request.fetch_q_sessions(year)
        quali_workload = [{"session_key" : session_key} for session_key in qualifying_sessions] 

        meeting_workload = [{"year": year}]
        session_workload = [{"session_key": session_key} for session_key in race_sessions]

        # Fetching data with the API--> inserting--> deletion to avoid Out of Memory crash of docker container
        meeting_data = f1_request.fetch_f1_data(endpoint='meetings',query_params_list=meeting_workload)
        insert_table.insert_meeting_data(conn, meeting_data)

        session_data = f1_request.fetch_f1_data(endpoint='sessions',query_params_list=session_workload)
        insert_table.insert_session_data(conn, session_data)

        q_session_data = f1_request.fetch_f1_data(endpoint='sessions',query_params_list=quali_workload)
        insert_table.insert_session_data(conn, q_session_data)
        del q_session_data

        drivers_data = f1_request.fetch_f1_data(endpoint='drivers',query_params_list=session_workload)
        insert_table.insert_drivers_data(conn, drivers_data)

        q_drivers_data = f1_request.fetch_f1_data(endpoint='drivers',query_params_list=quali_workload)
        insert_table.insert_drivers_data(conn, q_drivers_data)
        del q_drivers_data

        workload = [
            {
            "session_key": driver['session_key'], 
            "driver_number": driver['driver_number']
            }
            for driver in drivers_data
        ]
            
        interval_data = f1_request.fetch_f1_data(endpoint='intervals',query_params_list=workload)
        insert_table.insert_interval_data(conn, interval_data)
        del interval_data

        #### The current model does not utilize car_data. In future functionalities it can be used maybe
        #car_data = f1_request.fetch_f1_data(endpoint='car_data',query_params_list=workload)
        #insert_table.insert_car_data(conn, car_data)
        #del car_data 

        lap_data = f1_request.fetch_f1_data(endpoint='laps',query_params_list=workload)
        insert_table.insert_laps_data(conn, lap_data)
        del lap_data

        pit_data = f1_request.fetch_f1_data(endpoint='pit',query_params_list=workload)
        insert_table.insert_pit_data(conn, pit_data) 
        del pit_data 

        pos_data = f1_request.fetch_f1_data(endpoint='position',query_params_list=workload)
        insert_table.insert_position_data(conn, pos_data) 
        del pos_data 

        race_data = f1_request.fetch_f1_data(endpoint='race_control',query_params_list=session_workload)
        insert_table.insert_race_control_data(conn, race_data) 
        del race_data 

        grid_data = f1_request.fetch_f1_data(endpoint='starting_grid',query_params_list=quali_workload)
        insert_table.insert_starting_grid_data(conn, grid_data) 
        del grid_data 

        stint_data = f1_request.fetch_f1_data(endpoint='stints',query_params_list=workload)
        insert_table.insert_stint_data(conn, stint_data) 
        del stint_data

        weather_data = f1_request.fetch_f1_data(endpoint='weather',query_params_list=session_workload)
        insert_table.insert_weather_data(conn, weather_data)
        del weather_data 

        del meeting_data
        del session_data
        del drivers_data
     
    except Exception as e:
        print(f"ETL failed: {e}")
        raise
                
    finally:
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    create_database()
    data_to_db()
