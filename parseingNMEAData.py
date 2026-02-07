import folium
import random
# Sample NMEA sentence for testing - GPGGA format contains GPS fix data
NMEAsentence = "$GPGGA,123519,3335.2017,N,10152.5167,W,1,08,0.9,545.4,M,46.9,M,,*47"
  # Remove the first character (the '$')



class GPSData:
    def __init__(self):
        # Initialize latitude and longitude as None until parsed
        self.latitude = None
        self.longitude = None
        # Initialize timestamp as None until parsed
        self.timestamp = None

    def parse_gpgga(self, nmea_sentence):
        """
        Parse a GPGGA NMEA sentence to extract latitude, longitude, and timestamp.
        GPGGA format: $GPGGA,time,lat,lat_dir,lon,lon_dir,quality,sats,hdop,alt,alt_unit,geoid,geoid_unit,dgps_age,dgps_id*checksum
        """
        
        # Remove the leading '$' character from the NMEA sentence
        senstence = nmea_sentence[1:]
        # Split the sentence by commas to get individual fields
        fields = senstence.split(',')

        # Extract timestamp from field[1] (format: HHMMSS or HHMMSS.sss)
        time_raw = fields[1]
        # Parse hours, minutes, and seconds from the timestamp
        if len(time_raw) >= 6:
            hours = time_raw[0:2]
            minutes = time_raw[2:4]
            seconds = time_raw[4:6]
            # Check if there are decimal seconds
            if '.' in time_raw:
                decimal_seconds = time_raw[6:]
                self.timestamp = f"{hours}:{minutes}:{seconds}{decimal_seconds}"
            else:
                self.timestamp = f"{hours}:{minutes}:{seconds}"
        else:
            self.timestamp = None

        # Extract latitude data (format: DDMM.MMMM where DD is degrees, MM.MMMM is minutes)
        latitude_raw = float(fields[2])
        latitude_direction = fields[3]  # 'N' for North, 'S' for South
        # Extract longitude data (format: DDDMM.MMMM where DDD is degrees, MM.MMMM is minutes)
        longitude_raw = float(fields[4])
        longitude_direction = fields[5]  # 'E' for East, 'W' for West

        # Convert latitude from DDMM.MMMM format to decimal degrees
        latitude_degrees = int(latitude_raw / 100)  # Extract the degrees portion
        latitude_minutes = latitude_raw - (latitude_degrees * 100)  # Extract the minutes portion
        latitude = latitude_degrees + (latitude_minutes / 60)  # Convert to decimal degrees
        # If Southern hemisphere, make latitude negative
        if latitude_direction == 'S':
            latitude = -latitude
        
        # Convert longitude from DDDMM.MMMM format to decimal degrees
        longitude_degrees = int(longitude_raw / 100)  # Extract the degrees portion
        longitude_minutes = longitude_raw - (longitude_degrees * 100)  # Extract the minutes portion
        longitude = longitude_degrees + (longitude_minutes / 60)  # Convert to decimal degrees
        # If Western hemisphere, make longitude negative
        if longitude_direction == 'W':
            longitude = -longitude
        
        # Store the converted coordinates in the object
        self.latitude = latitude
        self.longitude = longitude

    def google_maps_link(self):
        """
        Generate a Google Maps search link using the parsed GPS coordinates.
        Returns None if coordinates haven't been parsed yet.
        """
        # Check if coordinates have been parsed
        if self.latitude is None or self.longitude is None:
            return None
        # Return a Google Maps search URL with the coordinates
        return f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"
    
    def save_to_file(self, file_path):
        """
        Save the parsed GPS data (timestamp, latitude, longitude) to a text file.
        Each entry is saved on a new line in the format: timestamp,latitude,longitude
        """
        if self.latitude is None or self.longitude is None:
            print("No GPS data to save.")
            return 
        
        try:
            with open(file_path, 'a') as file:
                file.write(f"{self.timestamp},{self.latitude},{self.longitude}\n")
                print("GPS data saved successfully") 
        except Exception as e:
            print(f"Error saving GPS data to file: {e}")

class GPSMapsHandler:
    def __init__(self):
        self.coordinates = []
        
    def load_gps_data(self,file_path):
        """
        read the parsed GPS data (timestamp, latitude, longitude) to a text file.\
        """
        try:
            with open(file_path, 'r') as file:
                coordinates = []
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        timestamp, latitude, longitude = parts
                        coordinates.append((timestamp, float(latitude), float(longitude)))
                return coordinates
        except Exception as e:
            print(f"Error loading GPS data from file: {e}")
            return []
    def create_map(self):
        folium_map = folium.Map(location=[self.coordinates[0][1], self.coordinates[0][2]], zoom_start=12)
        path_coordinates = [(coord[1], coord[2]) for coord in self.coordinates]
        folium.PolyLine(locations = path_coordinates, color='blue').add_to(folium_map)
        for each in self.coordinates:
            folium.Marker(location=[each[1], each[2]]).add_to(folium_map)
        folium_map.save(r'C:\ECE-3332\GPSmap.html')
# Create a GPSData object
gps = GPSData()
# Parse the sample NMEA sentence
gps.parse_gpgga(NMEAsentence)
# Print the parsed timestamp (UTC time)
#print(f"Timestamp: {gps.timestamp}")
# Print the parsed latitude and longitude in decimal degrees
print(gps.latitude, gps.longitude)
# Print the Google Maps link for the location
#print(gps.google_maps_link())
# Save the parsed GPS data to a file
for i in range(100):
    gps.latitude += random.uniform(-0.001, 0.001)  # Simulate slight changes in latitude
    gps.longitude += random.uniform(-0.001, 0.001)  # Simulate slight changes in longitude
    gps.save_to_file(r'C:\ECE-3332\GPSdata.txt')

# Load GPS data from file and create a map
maps_handler = GPSMapsHandler()
maps_handler.coordinates = maps_handler.load_gps_data(r'C:\ECE-3332\GPSdata.txt')
maps_handler.create_map()



