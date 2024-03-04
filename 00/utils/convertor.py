import json

original_data = ""


def read_json_file(filename):
    """
    按行读取文件，并把每行字符串转为 JSON

    Args:
      filename: 文件名

    Returns:
      一个列表，包含每个行的 JSON 对象
    """

    with open(filename, 'r') as f:
        f_lines = f.readlines()

    json_objects = []
    for line in f_lines:
        json_object = json.loads(line)
        json_objects.append(json_object)

    return json_objects


if __name__ == '__main__':
    lines2 = read_json_file(original_data)
    for line in lines2:
        results = line["result"]["result"]
        for result in results:
            if len(result['data']) > 0:
                print(line["result"]['image'])
