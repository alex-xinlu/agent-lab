import os


def ordered_list_dir(dir):
    entries = os.listdir(dir)
    entries.sort()
    return entries


def ordered_list_json_dir(dir):
    return list(
        filter(lambda f: os.path.splitext(f)[1] == '.json',
               ['{}/{}'.format(dir, f) for f in ordered_list_dir(dir)]))


def retrieve_file_paths(dir_name):
    file_paths = []
    for root, directories, files in os.walk(dir_name):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_paths.append(file_path)
    return file_paths


def init_path(options):

    # 定义初始化目录，这些目录不会提交到 git
    # 但是需要程序启动的时候自动生成
    # 确保目录存在
    depend_dirs = [
        # 配置参数目录结构
        'config',

        # 配置测试文件目录结构
        'data',

        # 配置 component 目录结构
        'component'
    ]

    for depend_dir in depend_dirs:
        os.makedirs(depend_dir, exist_ok=True)


def get_data_root():
    return 'data'


def get_test_data_path(task_name, sub_task_name, file_name):
    return os.path.join(get_data_root(), task_name, sub_task_name, file_name)

