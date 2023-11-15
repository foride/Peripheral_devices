import pynmea2
from time import sleep
import serial
import webbrowser
import io


def open_google_maps(latitude, longitude):

    maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude}, {longitude}"
    webbrowser.open(maps_url)


print("Wpisz nazwe portu odpowiedzialnego za odbior danych z GPS: ")
port_name = input()
gps = serial.Serial(port_name, 9600, parity='N', stopbits=1, bytesize=8, xonxoff=True, timeout=5)

while True:

    nmea_sentence = io.TextIOWrapper(io.BufferedRWPair(gps, gps))

    while 1:
        sleep(1)
        try:
            line = nmea_sentence.readline()
            data = pynmea2.parse(line)
            data_string = str(data)

            if data_string[0:6] == "$GPGGA":
                latitude = f"{data.lat[0:2]}°{data.lat[2:8]}’ {data.lat_dir}"
                longitude = f"{data.lon[0:3]}°{data.lon[3:9]}’ {data.lon_dir}"

                print(f"Godzina odczytu pozycji w czasie: {data.timestamp} UTC\n"
                      f"Szerokosc geograficzna: {latitude}\n"
                      f"Dlugosc geograficzna: {longitude}\n"
                      f"Jakosc modyfikacji: {data.gps_qual}\n"
                      f"Ilosc widzianych sateli: {data.num_sats}\n"
                      f"Pozioma konstelacja pozycji: {data.horizontal_dil}\n"
                      f"Wzgledna wysokosc nad poziomem morza: {data.altitude} {data.altitude_units}\n"
                      f"Wysokość geoidy: {data.geo_sep} {data.geo_sep_units}\n"
                      f"Czas w sekundach od ostatniej aktualizacji DGPS: {data.age_gps_data}\n"
                      f"Numer ID stacji DGPS: {data.ref_station_id}\n")

                variable = input()
                if variable == "1":
                    open_google_maps(latitude, longitude)

        except serial.SerialException as e:
            print('Device error: {}'.format(e))
            break
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))

            continue
