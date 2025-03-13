import os
import time

from PIL import Image, ImageDraw, ImageFont


def add_watermark_to_images(input_dir, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # 检查文件是否为jpg格式（不区分大小写）
            if file.lower().endswith(('.jpg', '.jpeg')):
                input_path = os.path.join(root, file)

                # 构建输出文件路径
                rel_path = os.path.relpath(root, input_dir)
                if rel_path == '.':
                    output_subdir = output_dir
                else:
                    output_subdir = os.path.join(output_dir, rel_path)

                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)
                output_path = os.path.join(output_subdir, file)

                try:
                    # 打开图片并添加水印
                    image = Image.open(input_path)
                    draw = ImageDraw.Draw(image)

                    # 从文件名中提取时间
                    filename_parts = file.split('_')
                    if len(filename_parts) >= 3:
                        watermark_date = f"{filename_parts[0]}-{filename_parts[1]}-{filename_parts[2]}"
                    else:
                        # 如果文件名格式不匹配，使用当前时间
                        print(f"文件名格式不匹配: {file}")
                        continue

                    # 设置字体和大小
                    font = ImageFont.load_default(size=80)

                    # 设置水印位置和颜色
                    text_color = (255, 255, 255)  # 白色
                    position = (20, image.height - 100)  # 左下角

                    # 添加水印
                    draw.text(position, watermark_date, fill=text_color, font=font)

                    # 保存处理后的图片
                    image.save(output_path)
                    print(f"已处理: {file}")
                except Exception as e:
                    print(f"处理 {file} 时出错: {str(e)}")


def list_files_and_sizes(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            print(f"文件: {file_path}, 大小: {file_size} 字节")


# 替换为你要读取的目录路径
directory_path = "/path/to/your/directory"
list_files_and_sizes(directory_path)

if __name__ == '__main__':
    start_time = time.time()  # 记录开始时间

    # 输入和输出目录
    input_dir = ""
    output_dir = "水印"

    add_watermark_to_images(input_dir, output_dir)

    # 计算并显示总耗时
    end_time = time.time()
    total_time = end_time - start_time
    print(f"总耗时: {total_time:.2f} 秒")
