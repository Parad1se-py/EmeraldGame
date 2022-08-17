from csv import reader

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        terrain_map.extend(list(row) for row in reader(map, delimiter=','))
        return terrain_map
