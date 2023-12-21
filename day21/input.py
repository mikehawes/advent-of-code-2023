from day21.farm import FarmMap, farm_from_list_of_lists


def read_farm_map_from_file(input_file) -> FarmMap:
    with open(input_file, 'r') as file:
        return farm_from_list_of_lists(list(map(lambda line: list(line.strip()), file)))
