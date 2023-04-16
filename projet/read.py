file_name = "metro.txt"

stations = {}
time_between_stations = {}

with open(file_name, "r", encoding="utf-8") as file:
    for row in file:
        elements = row.split()

        if elements[0] == "V":
            station_number = int(elements[1])
            station_name = " ".join(elements[2:])
            stations[station_number] = station_name

        elif elements[0] == "E":
            station_number_one = int(elements[1])
            station_number_two = int(elements[2])
            time_seconds = int(elements[3])
            time_between_stations[(station_number_one, station_number_two)] = time_seconds



