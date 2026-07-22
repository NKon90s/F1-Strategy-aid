import psycopg2
  
class CreateDB:
    def __init__(self, conn):
        self.conn = conn

    def create_table_sessions(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.sessions(
                        
                    session_key INT PRIMARY KEY,
                    meeting_key INT NOT NULL,
                    date_start TIMESTAMP NOT NULL,
                    date_end TIMESTAMP,
                    entry_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    circuit_key INT,
                    country_name VARCHAR,
                    location VARCHAR,
                    year INT,
                    session_type VARCHAR,
                    is_cancelled BOOL,
                        
                    CONSTRAINT fk_meeting
                        FOREIGN KEY (meeting_key)
                        REFERENCES dev.meetings(meeting_key)
            
                );
            """
            )
            conn.commit()
            print("Sessions Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Sessions table {e}")
            raise


    def create_table_meetings(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.meetings(
                    
                    meeting_key INT PRIMARY KEY,
                    meeting_name TEXT,
                    meeting_official_name TEXT,
                    country_name TEXT,
                    country_code TEXT,
                    circuit_short_name TEXT,
                    location TEXT,
                    year INT,
                    date_start TIMESTAMP
            
                );
            """
            )
            conn.commit()
            print("Meetings Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Mettings table {e}")
            raise

    def create_table_drivers(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.drivers(
                    
                    session_key INT,
                    driver_number INT,
                    full_name TEXT,
                    team_name TEXT,
                    team_colour TEXT,
                    name_acronym TEXT,
                    country_code TEXT,
                    
                    PRIMARY KEY (session_key, driver_number)                       
                );
            """
            )
            conn.commit()   
            print("Drivers Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Drivers table {e}")
            raise


    def create_table_intervals(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.interval_data(
                    
                    id BIGSERIAL PRIMARY KEY,
                    meeting_key INT NOT NULL,
                    session_key INT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    entry_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    driver_number INT NOT NULL,
                    gap_to_leader TEXT,
                    interval TEXT,
                    
                    CONSTRAINT fk_session
                        FOREIGN KEY (session_key)
                        REFERENCES dev.sessions(session_key),

                    CONSTRAINT fk_driver
                        FOREIGN KEY (session_key, driver_number)
                        REFERENCES dev.drivers(session_key, driver_number),
                        
                    CONSTRAINT uq_interval
                        UNIQUE (session_key, driver_number, date)
                );
            """
            )
            conn.commit()
            print("Intervals Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Intervals table {e}")
            raise


    def create_table_car_data(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.car_data(
                    
                    id BIGSERIAL PRIMARY KEY,
                    meeting_key INT NOT NULL,
                    session_key INT NOT NULL,
                    brake INT,
                    date TIMESTAMP,
                    entry_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    driver_number INT NOT NULL,
                    drs INT, 
                    n_gear INT,
                    rpm INT,
                    speed INT,
                    throttle INT,
                    
                    CONSTRAINT fk_session
                        FOREIGN KEY (session_key)
                        REFERENCES dev.sessions(session_key),

                    CONSTRAINT fk_driver
                        FOREIGN KEY (session_key, driver_number)
                        REFERENCES dev.drivers(session_key, driver_number),
                    
                    CONSTRAINT fk_meeting
                        FOREIGN KEY (meeting_key)
                        REFERENCES dev.meetings(meeting_key),
                        
                    CONSTRAINT uq_car_data
                        UNIQUE (session_key, driver_number, date)
                );
            """
            )
            conn.commit()
            print("Car Data Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Car Data table {e}")
            raise



    def create_table_laps(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.laps(
                    
                    id BIGSERIAL PRIMARY KEY,
                    meeting_key INT NOT NULL,
                    session_key INT NOT NULL,
                    date_start TIMESTAMP,
                    entry_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    driver_number INT NOT NULL,
                    duration_sector_1 NUMERIC,
                    duration_sector_2 NUMERIC,
                    duration_sector_3 NUMERIC,
                    i1_speed INT,
                    i2_speed INT,
                    is_pit_out_lap BOOL,
                    lap_duration NUMERIC,
                    lap_number INT,
                    st_speed INT,
                    
                    CONSTRAINT fk_session
                        FOREIGN KEY (session_key)
                        REFERENCES dev.sessions(session_key),

                    CONSTRAINT fk_driver
                        FOREIGN KEY (session_key, driver_number)
                        REFERENCES dev.drivers(session_key, driver_number),
                    
                    CONSTRAINT fk_meeting
                        FOREIGN KEY (meeting_key)
                        REFERENCES dev.meetings(meeting_key),
                        
                    CONSTRAINT uq_laps 
                        UNIQUE (session_key, driver_number, date_start)
                );
            """
            )
            conn.commit()
            print("Laps Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Laps table {e}")
            raise


    def create_table_pit(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.pit(
                    
                    id BIGSERIAL PRIMARY KEY,
                    meeting_key INT NOT NULL,
                    session_key INT NOT NULL,
                    date TIMESTAMP,
                    entry_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    driver_number INT NOT NULL,
                    lane_duration NUMERIC,
                    lap_number INT,
                    pit_duration NUMERIC,
                    stop_duration NUMERIC,
                    
                    CONSTRAINT fk_session
                        FOREIGN KEY (session_key)
                        REFERENCES dev.sessions(session_key),

                    CONSTRAINT fk_driver
                        FOREIGN KEY (session_key, driver_number)
                        REFERENCES dev.drivers(session_key, driver_number),
                    
                    CONSTRAINT fk_meeting
                        FOREIGN KEY (meeting_key)
                        REFERENCES dev.meetings(meeting_key),
                        
                    CONSTRAINT uq_pit
                        UNIQUE (session_key, driver_number, date)
                );
            """
            )
            conn.commit()
            print("Pit Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Pit table {e}")
            raise


    def create_table_position(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.position(
                    
                    id BIGSERIAL PRIMARY KEY,
                    meeting_key INT NOT NULL,
                    session_key INT NOT NULL,
                    date TIMESTAMP,
                    entry_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    driver_number INT NOT NULL,
                    position INT,
                    
                    CONSTRAINT fk_session
                        FOREIGN KEY (session_key)
                        REFERENCES dev.sessions(session_key),

                    CONSTRAINT fk_driver
                        FOREIGN KEY (session_key, driver_number)
                        REFERENCES dev.drivers(session_key, driver_number),
                    
                    CONSTRAINT fk_meeting
                        FOREIGN KEY (meeting_key)
                        REFERENCES dev.meetings(meeting_key),
                        
                    CONSTRAINT uq_position
                        UNIQUE (session_key, driver_number, date)
                );
            """
            )
            conn.commit()
            print("Position Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Position table {e}")
            raise

    def create_table_race_control(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.race_control(
                    
                    id BIGSERIAL PRIMARY KEY,
                    meeting_key INT NOT NULL,
                    session_key INT NOT NULL,
                    date TIMESTAMP,
                    entry_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    driver_number INT,
                    category VARCHAR,
                    flag VARCHAR,
                    lap_number INT,
                    message VARCHAR,
                    qualifying_phase INT,
                    scope VARCHAR,
                    sector INT,
                    
                    CONSTRAINT fk_session
                        FOREIGN KEY (session_key)
                        REFERENCES dev.sessions(session_key),

                    CONSTRAINT fk_driver
                        FOREIGN KEY (session_key, driver_number)
                        REFERENCES dev.drivers(session_key, driver_number),
                    
                    CONSTRAINT fk_meeting
                        FOREIGN KEY (meeting_key)
                        REFERENCES dev.meetings(meeting_key),
                        
                    CONSTRAINT uq_race_control
                        UNIQUE (session_key, driver_number, date)
                );
            """
            )
            conn.commit()
            print("Race Control Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Race Control table {e}")
            raise


    def create_table_starting_grid(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.starting_grid(
                    
                    id BIGSERIAL PRIMARY KEY,
                    meeting_key INT NOT NULL,
                    session_key INT NOT NULL,
                    entry_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    driver_number INT NOT NULL,
                    lap_duration NUMERIC,
                    position INT,
                    
                    CONSTRAINT fk_session
                        FOREIGN KEY (session_key)
                        REFERENCES dev.sessions(session_key),

                    CONSTRAINT fk_driver
                        FOREIGN KEY (session_key, driver_number)
                        REFERENCES dev.drivers(session_key, driver_number),
                    
                    CONSTRAINT fk_meeting
                        FOREIGN KEY (meeting_key)
                        REFERENCES dev.meetings(meeting_key)
                );
            """
            )
            conn.commit()
            print("Starting Grid Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Starting Grid table {e}")
            raise


    def create_table_stints(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.stints(
                    
                    id BIGSERIAL PRIMARY KEY,
                    meeting_key INT NOT NULL,
                    session_key INT NOT NULL,
                    entry_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    driver_number INT NOT NULL,
                    compound VARCHAR,
                    lap_end INT,
                    lap_start INT,
                    stint_number INT,
                    tyre_age_at_start INT,
                    
                    CONSTRAINT fk_session
                        FOREIGN KEY (session_key)
                        REFERENCES dev.sessions(session_key),

                    CONSTRAINT fk_driver
                        FOREIGN KEY (session_key, driver_number)
                        REFERENCES dev.drivers(session_key, driver_number),
                    
                    CONSTRAINT fk_meeting
                        FOREIGN KEY (meeting_key)
                        REFERENCES dev.meetings(meeting_key),
                        
                    CONSTRAINT uq_car_stints
                        UNIQUE (session_key, driver_number, stint_number)
                );
            """
            )
            conn.commit()
            print("Stints Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Stints table {e}")
            raise


    def create_table_weather(self, conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.weather(
                    
                    id BIGSERIAL PRIMARY KEY,
                    meeting_key INT NOT NULL,
                    session_key INT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    entry_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    air_temperature NUMERIC,
                    humidity NUMERIC,
                    pressure NUMERIC,
                    rainfall INT,
                    track_temperature NUMERIC,
                    wind_direction INT,
                    wind_speed NUMERIC,
                        
                    CONSTRAINT fk_session
                        FOREIGN KEY (session_key)
                        REFERENCES dev.sessions(session_key),
                    
                    CONSTRAINT fk_meeting
                        FOREIGN KEY (meeting_key)
                        REFERENCES dev.meetings(meeting_key),
                        
                    CONSTRAINT uq_weather
                        UNIQUE (session_key, date)
                );
            """
            )
            conn.commit()
            print("Weather Table was created")
        except psycopg2.Error as e:
            print(f"Failed to create Weather table {e}")
            raise

 
