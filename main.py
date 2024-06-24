from config.global_config import GlobalConfig
from md5_helper import *
from update_markdown import *
from upload_markdown import *


def compare_maps(current_map, snapshot_map):
    new_post = {}
    edit_post = {}

    for file_name, md5_value in current_map.items():
        if file_name not in snapshot_map:
            new_post[file_name] = md5_value
        elif snapshot_map[file_name] != md5_value:
            edit_post[file_name] = md5_value

    return new_post, edit_post


if __name__ == '__main__':
    config = GlobalConfig.get_config()
    # 获取目录下所有文件的文件名以及md5值map
    current_file_map = get_files_md5_map(config['settings']['path'])
    file_map_snapshot = load_files_md5_map_from_file('files_md5_map_snapshot.txt')
    # 比较两个map
    new_post, edit_post = compare_maps(current_file_map, file_map_snapshot)
    unload_new_post(new_post)
    update_post(edit_post)
    save_files_md5_map_to_file(current_file_map, 'files_md5_map_snapshot.txt')
