import psycopg2


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
            cursor.execute("""
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
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_key)
                DO NOTHING;
            """,(
                session_data['session_key'],
                session_data['meeting_key'],
                session_data['date_start'],
                session_data['date_end'],
                session_data['circuit_key'],
                session_data['country_name'],
                session_data['location'],
                session_data['year'],
                session_data['session_type'],
                session_data['is_cancelled']
            ))
            conn.commit() 
            print("Session data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert session data {e}")
            raise


    def insert_session_data(self, conn, meeting_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
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
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (meeting_key)
                DO NOTHING;

            """,(
                meeting_data['meeting_key'],
                meeting_data['meeting_name'],
                meeting_data['meeting_official_name'],
                meeting_data['country_name'],
                meeting_data['country_code'],
                meeting_data['circuit_short_name'],
                meeting_data['location'],
                meeting_data['year'],
                meeting_data['date_start']
            ))
            conn.commit()
            print("Meeting data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert meeting data {e}")
            raise


    def insert_drivers_data(self, conn, drivers_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dev.drivers(
                    session_key,
                    driver_number,
                    full_name,
                    team_name,
                    team_colour,
                    name_acronym,
                    country_code
                ) VALUES(%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_key, driver_number)
                DO UPDATE SET
                    session_key = EXCLUDED.session_key,
                    driver_number = EXCLUDED.driver_number,
                    full_name = EXCLUDED.full_name,
                    team_name = EXCLUDED.team_name,
                    team_colour = EXCLUDED.team_colour,
                    name_acronym = EXCLUDED.name_acronym,
                    country_code = EXCLUDED.country_code; 

            """,(
                drivers_data['session_key'],
                drivers_data['driver_number'],
                drivers_data['full_name'],
                drivers_data['team_name'],
                drivers_data['team_colour'],
                drivers_data['name_acronym'],
                drivers_data['country_code']
                
            ))
            conn.commit()
            print("Drivers data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Drivers data {e}")
            raise

    def insert_interval_data(self, conn, interval_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dev.interval_data(
                    meeting_key,
                    session_key,
                    date,
                    driver_number,
                    gap_to_leader,
                    interval
                ) VALUES(%s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_key, driver_number, date)
                DO NOTHING; 
            """,(
                interval_data['meeting_key'],
                interval_data['session_key'],
                interval_data['date'],
                interval_data['driver_number'],
                interval_data['gap_to_leader'],
                interval_data['interval']
                
            ))
            conn.commit()
            print("Interval data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Interval data {e}")
            raise
    
        
    def insert_car_data(self, conn, car_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
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
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_key, driver_number, date)
                DO NOTHING; 
            """,(
                car_data['meeting_key'],
                car_data['session_key'],
                car_data['brake'],
                car_data['date'],
                car_data['driver_number'],
                car_data['drs'],
                car_data['n_gear'],
                car_data['rpm'],
                car_data['speed'],
                car_data['throttle']
            ))
            conn.commit()
            print("Car data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Car data {e}")
            raise

    def insert_laps_data(self, conn, lap_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
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
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_key, driver_number, date_start)
                DO NOTHING; 
            """,(
                lap_data['meeting_key'],
                lap_data['session_key'],
                lap_data['date_start'],
                lap_data['driver_number'],
                lap_data['duration_sector_1'],
                lap_data['duration_sector_2'],
                lap_data['duration_sector_3'],
                lap_data['i1_speed'],
                lap_data['i2_speed'],
                lap_data['is_pit_out_lap'],
                lap_data['lap_duration'],
                lap_data['lap_number'],
                lap_data['st_speed']
            ))
            conn.commit()
            print("Lap data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Lap data {e}")
            raise


    def insert_pit_data(self, conn, pit_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dev.pit(
                    meeting_key,
                    session_key,
                    date,
                    driver_number,
                    lane_duration,
                    lap_number,
                    pit_duration,
                    stop_duration
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_key, driver_number, date)
                DO NOTHING; 
            """,(
                pit_data['meeting_key'],
                pit_data['session_key'],
                pit_data['date'],
                pit_data['driver_number'],
                pit_data['lane_duration'],
                pit_data['lap_number'],
                pit_data['pit_duration'],
                pit_data['stop_duration']
            ))
            conn.commit()
            print("Pit data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Pit data {e}")
            raise


    def insert_position_data(self, conn, pos_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dev.position(
                    meeting_key,
                    session_key,
                    date,
                    driver_number,
                    position
                ) VALUES(%s, %s, %s, %s, %s)
                ON CONFLICT (session_key)
                DO NOTHING; 
            """,(
                pos_data['meeting_key'],
                pos_data['session_key'],
                pos_data['date'],
                pos_data['driver_number'],
                pos_data['position']
            ))
            conn.commit()
            print("Position data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Position data {e}")
            raise



    def insert_race_control_data(self, conn, race_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
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
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_key, driver_number, date)
                DO NOTHING; 
            """,(
                race_data['meeting_key'],
                race_data['session_key'],
                race_data['date'],
                race_data['driver_number'],
                race_data['category'],
                race_data['flag'],
                race_data['lap_number'],
                race_data['message'],
                race_data['qualifying_phase'],
                race_data['scope'],
                race_data['sector']
            ))
            conn.commit()
            print("Race data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Race data {e}")
            raise


    def insert_starting_grid_data(self, conn, grid_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dev.starting_grid(
                    meeting_key,
                    session_key,
                    driver_number,
                    lap_duration,
                    position
                ) VALUES(%s, %s, %s, %s, %s)
                ON CONFLICT (session_key)
                DO NOTHING; 
            """,(
                grid_data['meeting_key'],
                grid_data['session_key'],
                grid_data['driver_number'],
                grid_data['lap_duration'],
                grid_data['position']
            ))
            conn.commit()
            print("Stint data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Stint data {e}")
            raise


    def insert_stint_data(self, conn, stint_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dev.stints(
                    meeting_key,
                    session_key,
                    driver_number,
                    compound,
                    lap_end,
                    lap_start,
                    stint_number,
                    tyre_age_at_start
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_key, driver_number, stint_number)
                DO NOTHING; 
            """,(
                stint_data['meeting_key'],
                stint_data['session_key'],
                stint_data['driver_number'],
                stint_data['compound'],
                stint_data['lap_end'],
                stint_data['lap_start'],
                stint_data['stint_number'],
                stint_data['tyre_age_at_start']
            ))
            conn.commit()
            print("Stint data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Stint data {e}")
            raise


    def insert_weather_data(self, conn, weather_data):
        try:
            cursor = conn.cursor()
            cursor.execute("""
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
                ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_key, date)
                DO NOTHING; 
            """,(
                weather_data['meeting_key'],
                weather_data['session_key'],
                weather_data['date'],
                weather_data['air_temperature'],
                weather_data['humidity'],
                weather_data['pressure'],
                weather_data['rainfall'],
                weather_data['track_temperature'],
                weather_data['wind_direction'],
                weather_data['wind_speed']
            ))
            conn.commit()
            print("Weather data inserted successfully")
        except psycopg2.Error as e:
            print(f"Failed to insert Weather data {e}")
            raise

