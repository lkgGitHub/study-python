import os
import shutil

base_dir = ""


def diff_dir(old, new):
    diff_files = []
    new_num = 0
    old_num = 0
    common_num = 0

    new_files = os.listdir(new)
    new_dict = {}
    for f in new_files:
        new_num = new_num + 1
        new_dict[f] = ""

    old_files = os.listdir(old)
    old_dict = {}
    for f in old_files:
        old_num = old_num + 1
        old_dict[f] = ""
        if f not in new_dict:
            diff_files.append(os.path.join(old, f))
        else:
            common_num = common_num + 1

    new_add_num = 0
    for f in new_files:
        if f not in old_dict:
            delete_num = new_add_num + 1

    print("diff_files:", diff_files)
    new_dir = os.path.join(base_dir, "diff_files")
    try:
        os.mkdir(new_dir)
    except OSError as e:
        print(f"创建目录时出现错误: {e}")
    for f in diff_files:
        try:
            shutil.copyfile(f, os.path.join(new_dir, os.path.basename(f)))
        except Exception as e:
            print(f": {e}")
    print(f"{old} num: {old_num}")
    print(f"{new} num: {new_num}")
    print(f"diff num: {len(diff_files)}")
    print(new_num + new_add_num == old_num + len(diff_files))


if __name__ == '__main__':
    d1 = ''
    d2 = ''
    diff_dir(d1, d2)
