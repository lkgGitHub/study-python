head = ['Length', 'Interface', 'xDR ID', 'RAT', 'IMSI', 'IMEI', 'MSISDN', 'Local Province', 'Local City',
        'Owner Province', 'Owner City', 'Roaming Type', 'Machine IP Add type', 'SGW/GGSN IP Add', 'eNB/SGSN IP Add',
        'PGW Add', 'SGW/GGSN Port', 'eNB/SGSN Port', 'PGW Port', 'eNB/SGSN GTP-TEID', 'SGW/GGSN GTP-TEID', 'TAC',
        'Cell ID', 'APN', 'App Type Code', 'Procedure Start Time', 'Procedure End Time', 'longitude',
        'latitude']  # 'City',


data_path_file = "D:\\01Work\\04微智URL分析\\SCA疑似URL\\data\\"
path = data_path_file + "LTE_240_YDLNG00137_S1U103_20190728002004_0000.txt"

with open(path, mode='r', encoding='utf-8') as txt:
    lines = txt.readlines()
    # line = txt.readline()
    for i in range(3):
        line = lines[i]
        line_array = line.split("|")
        print("==" * 30)
        for j in range(0, 11):
            print(j+2, head[j], ":", line_array[j])

