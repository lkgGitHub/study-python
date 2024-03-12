from datetime import datetime
import os

root = "E:\\computer-vision"


def recursive_list_files(folder_path):
    """
    递归列出文件夹及其子文件夹中的所有文件。
    os.walk() 是 Python 中用于遍历文件夹（目录）以及其中所有子文件夹和文件的方法。它返回一个生成器，
    该生成器生成一个三元组 (dir_path, dir_names, file_names)，其中：
        dir_path 是当前文件夹的路径。
        dir_names 是当前文件夹中所有子文件夹的名称列表。
        file_names 是当前文件夹中所有文件的名称列表。
    """

    delete_files = []
    not_delete_file = []
    file_num = 0
    for dir_path, dir_names, file_names in os.walk(folder_path):
        for file in file_names:
            file_num += 1
            if file_num % 100 == 0:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file_num)
            if file.startswith('.'):
                file_path = os.path.join(dir_path, file)
                if file in ('.DS_Store', '.DS_Store', '__MACOSX'):
                    delete_files.append(file_path)
                    continue
                # mode='rb' b：这个模式表示以二进制方式打开文件。在二进制模式下，文件的内容被视为字节流，而不是文本
                with open(file_path, mode='rb') as f:
                    content = f.read().decode('utf-8', 'ignore')
                    if 'Mac OS X' in content:
                        delete_files.append(file_path)
                    else:
                        not_delete_file.append(file_path)
    print("delete files:", delete_files)
    # 删除文件
    delete_success_count = 0
    delete_failed_count = 0
    for delete_file_path in delete_files:
        try:
            os.remove(delete_file_path)
            delete_success_count += 1
        except OSError as e:
            delete_failed_count += 1
            print(f"delete failed. {delete_file_path}, exception: {e}")

    print("delete_success_count:", delete_success_count)
    print("delete_failed_count:", delete_failed_count)
    for index, file_path in enumerate(not_delete_file):
        print(f"{index} \t {os.path.basename(file_path)} \t\t path: {file_path}")


if __name__ == '__main__':
    start_time = datetime.now()
    recursive_list_files(root)
    print(f"程序运行时间：{datetime.now() - start_time}")
