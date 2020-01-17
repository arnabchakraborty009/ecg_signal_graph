import glob


def read_data_files():
    data = {}
    data_files = glob.glob("data/*.txt")
    for file in data_files:
        lead = file.split("\\")[1].split('.')[0]
        file_data_arr = read_from_data_file(file)
        data[lead] = file_data_arr
    return data


def read_from_data_file(file_name):
    x = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            x.append(float(line))
    return x


def find_gain(data, start, end, hr):
    keys = data.keys()
    max_value = []
    min_value = []
    data_arr = []
    for key in keys:
        ecg_data = data[key]
        ecg_data_for_min_max = list(filter(lambda a: a is not None, ecg_data))
        if len(ecg_data_for_min_max) > 0:
            max_value.append(max(ecg_data_for_min_max))
            min_value.append(min(ecg_data_for_min_max))
        else:
            continue

        try:
            data_arr.append({"data": ecg_data, "startDate": start, "endDate": end, "stream": key, "hr": hr})
        except Exception as e:
            print('Could not generate ECG Graph')
            raise e

    overall_max = max(max_value)
    overall_min = min(min_value)

    displacement = (overall_max - overall_min) / 25  # per div
    mid_of_displacement = displacement / 2

    # find gain
    disp_160mmmv = 1 / 160
    disp_80mmmv = 1 / 80
    disp_40mmmv = 1 / 40
    disp_20mmmv = 1 / 20
    disp_10mmmv = 1 / 10
    disp_5mmmv = 1 / 5
    disp_2_5mmmv = 1 / 2.5
    disp_1_25mmmv = 1 / 1.25

    mv_per_mm = '5'
    if displacement < disp_160mmmv:
        mv_per_mm = '160'
        dist = disp_160mmmv * 12.5
    elif displacement < disp_80mmmv:
        mv_per_mm = '80'
        dist = disp_80mmmv * 12.5
    elif displacement < disp_40mmmv:
        mv_per_mm = '40'
        dist = disp_40mmmv * 12.5
    elif displacement < disp_20mmmv:
        mv_per_mm = '20'
        dist = disp_20mmmv * 12.5
    elif displacement < disp_10mmmv:
        mv_per_mm = '10'
        dist = disp_10mmmv * 12.5
    elif displacement < disp_5mmmv:
        mv_per_mm = '5'
        dist = disp_5mmmv * 12.5
    elif displacement < disp_2_5mmmv:
        mv_per_mm = '2.5'
        dist = disp_2_5mmmv * 12.5
    elif displacement < disp_1_25mmmv:
        mv_per_mm = '1.25'
        dist = disp_1_25mmmv * 12.5

    overall_min = mid_of_displacement - dist
    overall_max = mid_of_displacement + dist

    lower = overall_min
    upper = overall_max

    return data_arr, lower, upper, mv_per_mm
