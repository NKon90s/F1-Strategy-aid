import psycopg2
from psycopg2.extras import execute_values

class InsertRecords:
    def __init__(self, conn, session_data, meeting_data, drivers_data, interval_data, car_data, lap_data, pit_data,
                 pos_data, race_data, grid_data, stint_data, weather_data):
        
        self.conn = conn
        self.session_data = session_data
        self.meeting_data = meeting_data
        self.drivers_data = drivers_data
        self.interval_data = interval_data
        self.car_data = car_data
        self.lap_data = lap_data
        self.pit_data = pit_data
        self.pos_data = pos_data
        self.race_data = race_data
        self.grid_data = grid_data
        self.stint_data = stint_data
        self.weather_data = weather_data
        
    def insert_session_data(self, conn, session_data):
        try:
            cursor = conn.cursor()
            
            rows = [
                (
                session['session_key'],
                session['meeting_key'],
                session['date_start'],
                session['date_end'],
                session['circuit_key'],
                session['country_name'],
                session['location'],
                session['year'],
                session['session_type'],
                session['is_cancelled']
                )
                for session in session_data
            ]
            
            sql = """
                INSERT INTO dev.sessions(
                    session_key,
                    meeting_key,
                    date_start,
                    date_end,
                    circuit_key,
                    country_name,
                    location,
                    year,
                    session_type,
                    is_cancelled 
                ) VALUES %s
                ON CONFLICT (session_key)
                DO NOTHING;
            """
            execute_values(cursor, sql, rows)

            conn.commit() 
            print("Session data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert session data {e}")
            raise


    def insert_meeting_data(self, conn, meeting_data):
        try:
            cursor = conn.cursor()

            rows = [
                (
                meeting['meeting_key'],
                meeting['meeting_name'],
                meeting['meeting_official_name'],
                meeting['country_name'],
                meeting['country_code'],
                meeting['circuit_short_name'],
                meeting['location'],
                meeting['year'],
                meeting['date_start']
                )   
                for meeting in meeting_data
            ]

            sql = """
                INSERT INTO dev.meetings(
                    meeting_key,
                    meeting_name,
                    meeting_official_name,
                    country_name,
                    country_code,
                    circuit_short_name,
                    location,
                    year,
                    date_start
                ) VALUES %s
                ON CONFLICT (meeting_key)
                DO NOTHING;

            """ 
            execute_values(cursor, sql, rows)
            
            conn.commit()
            print("Meeting data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert meeting data {e}")
            raise


    def insert_drivers_data(self, conn, drivers_data):
        try:
            cursor = conn.cursor()
            
            rows = [(
                driver['session_key'],
                driver['driver_number'],
                driver['full_name'],
                driver['team_name'],
                driver['team_colour'],
                driver['name_acronym'],
                driver['country_code']   
                )
                for driver in drivers_data
            ]
            
            sql = """
                INSERT INTO dev.drivers(
                    session_key,
                    driver_number,
                    full_name,
                    team_name,
                    team_colour,
                    name_acronym,
                    country_code
                ) VALUES %s
                ON CONFLICT (session_key, driver_number)
                DO UPDATE SET
                    session_key = EXCLUDED.session_key,
                    driver_number = EXCLUDED.driver_number,
                    full_name = EXCLUDED.full_name,
                    team_name = EXCLUDED.team_name,
                    team_colour = EXCLUDED.team_colour,
                    name_acronym = EXCLUDED.name_acronym,
                    country_code = EXCLUDED.country_code; 

            """
            execute_values(cursor, sql, rows)

            conn.commit()
            print("Drivers data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Drivers data {e}")
            raise


    def insert_interval_data(self, conn, interval_data):
        try:
            cursor = conn.cursor()

            rows = [
                (
                interval['meeting_key'],
                interval['session_key'],
                interval['date'],
                interval['driver_number'],
                interval['gap_to_leader'],
                interval['interval']
                )
                for interval in interval_data
            ]

            sql = """
                INSERT INTO dev.interval_data(
                    meeting_key,
                    session_key,
                    date,
                    driver_number,
                    gap_to_leader,
                    interval
                ) VALUES %s
                ON CONFLICT (session_key, driver_number, date)
                DO NOTHING; 
            """
            execute_values(cursor, sql, rows)
            
            conn.commit()
            print("Interval data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Interval data {e}")
            raise
    
        
    def insert_car_data(self, conn, car_data):
        try:
            cursor = conn.cursor()

            rows = [
                (
                car['meeting_key'],
                car['session_key'],
                car['brake'],
                car['date'],
                car['driver_number'],
                car['drs'],
                car['n_gear'],
                car['rpm'],
                car['speed'],
                car['throttle']
                )
                for car in car_data
            ]

            sql = """
                INSERT INTO dev.car_data(
                    meeting_key,
                    session_key,
                    brake,
                    date,
                    driver_number,
                    drs, 
                    n_gear,
                    rpm,
                    speed,
                    throttle
                ) VALUES %s
                ON CONFLICT (session_key, driver_number, date)
                DO NOTHING; 
            """
            execute_values(cursor, sql, rows)

            conn.commit()
            print("Car data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Car data {e}")
            raise

    def insert_laps_data(self, conn, lap_data):
        try:
            cursor = conn.cursor()
            
            rows= [
                (
                lap['meeting_key'],
                lap['session_key'],
                lap['date_start'],
                lap['driver_number'],
                lap['duration_sector_1'],
                lap['duration_sector_2'],
                lap['duration_sector_3'],
                lap['i1_speed'],
                lap['i2_speed'],
                lap['is_pit_out_lap'],
                lap['lap_duration'],
                lap['lap_number'],
                lap['st_speed']
                )
                for lap in lap_data
            ]
            
            sql = """
                INSERT INTO dev.laps(
                    meeting_key,
                    session_key,
                    date_start,
                    driver_number,
                    duration_sector_1,
                    duration_sector_2,
                    duration_sector_3,
                    i1_speed,
                    i2_speed,
                    is_pit_out_lap,
                    lap_duration,
                    lap_number,
                    st_speed
                ) VALUES %s
                ON CONFLICT (session_key, driver_number, date_start)
                DO NOTHING; 
            """

            execute_values(cursor, sql, rows)
            conn.commit()
            print("Lap data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Lap data {e}")
            raise


    def insert_pit_data(self, conn, pit_data):
        try:
            cursor = conn.cursor()
            
            rows = [
                (
                pit['meeting_key'],
                pit['session_key'],
                pit['date'],
                pit['driver_number'],
                pit['lane_duration'],
                pit['lap_number'],
                pit['pit_duration'],
                pit['stop_duration']
                )
                for pit in pit_data
            ]
            
            sql = """
                INSERT INTO dev.pit(
                    meeting_key,
                    session_key,
                    date,
                    driver_number,
                    lane_duration,
                    lap_number,
                    pit_duration,
                    stop_duration
                ) VALUES %s
                ON CONFLICT (session_key, driver_number, date)
                DO NOTHING; 
            """
            execute_values(cursor, sql, rows)
            conn.commit()
            print("Pit data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Pit data {e}")
            raise


    def insert_position_data(self, conn, pos_data):
        try:
            cursor = conn.cursor()
            
            rows = [
                (
                pos['meeting_key'],
                pos['session_key'],
                pos['date'],
                pos['driver_number'],
                pos['position']
                )
                for pos in pos_data
            ]
            
            sql = """
                INSERT INTO dev.position(
                    meeting_key,
                    session_key,
                    date,
                    driver_number,
                    position
                ) VALUES %s
                ON CONFLICT (session_key, driver_number, date)
                DO NOTHING; 
            """
            execute_values(cursor, sql, rows)

            conn.commit()
            print("Position data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Position data {e}")
            raise



    def insert_race_control_data(self, conn, race_data):
        try:
            cursor = conn.cursor()

            rows = [
                (
                race['meeting_key'],
                race['session_key'],
                race['date'],
                race['driver_number'],
                race['category'],
                race['flag'],
                race['lap_number'],
                race['message'],
                race['qualifying_phase'],
                race['scope'],
                race['sector']
                )
                for race in race_data
            ]

            sql = """
                INSERT INTO dev.race_control(
                    meeting_key,
                    session_key,
                    date,
                    driver_number,
                    category,
                    flag,
                    lap_number,
                    message,
                    qualifying_phase,
                    scope,
                    sector
                ) VALUES %s
                ON CONFLICT (session_key, driver_number, date)
                DO NOTHING; 
            """
            execute_values(cursor, sql, rows)

            conn.commit()
            print("Race data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Race data {e}")
            raise


    def insert_starting_grid_data(self, conn, grid_data):
        try:
            cursor = conn.cursor()

            rows = [
                (
                grid['meeting_key'],
                grid['session_key'],
                grid['driver_number'],
                grid['lap_duration'],
                grid['position']
                )
                for grid in grid_data
            ]

            sql = """
                INSERT INTO dev.starting_grid(
                    meeting_key,
                    session_key,
                    driver_number,
                    lap_duration,
                    position
                ) VALUES %s
                ON CONFLICT (session_key)
                DO NOTHING; 
            """
            execute_values(cursor, sql, rows)

            conn.commit()
            print("Stint data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Stint data {e}")
            raise


    def insert_stint_data(self, conn, stint_data):
        try:
            cursor = conn.cursor()
            
            rows = [
                (
                stint['meeting_key'],
                stint['session_key'],
                stint['driver_number'],
                stint['compound'],
                stint['lap_end'],
                stint['lap_start'],
                stint['stint_number'],
                stint['tyre_age_at_start']
                )
                for stint in stint_data
            ]

            sql = """
                INSERT INTO dev.stints(
                    meeting_key,
                    session_key,
                    driver_number,
                    compound,
                    lap_end,
                    lap_start,
                    stint_number,
                    tyre_age_at_start
                ) VALUES %s
                ON CONFLICT (session_key, driver_number, stint_number)
                DO NOTHING; 
            """

            execute_values(cursor, sql, rows)

            conn.commit()
            print("Stint data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Stint data {e}")
            raise


    def insert_weather_data(self, conn, weather_data):
        try:
            cursor = conn.cursor()
            
            rows = [
                (
                weather['meeting_key'],
                weather['session_key'],
                weather['date'],
                weather['air_temperature'],
                weather['humidity'],
                weather['pressure'],
                weather['rainfall'],
                weather['track_temperature'],
                weather['wind_direction'],
                weather['wind_speed']
                )
                for weather in weather_data
            ]
            
            sql = """
                INSERT INTO dev.weather(
                    meeting_key,
                    session_key,
                    date,
                    air_temperature,
                    humidity,
                    pressure,
                    rainfall,
                    track_temperature,
                    wind_direction,
                    wind_speed 
                ) VALUES %s
                ON CONFLICT (session_key, date)
                DO NOTHING; 
            """
            execute_values(cursor, sql, rows)

            conn.commit()
            print("Weather data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Weather data {e}")
            raise

