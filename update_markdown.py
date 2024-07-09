# -*- coding: utf-8 -*-
# @Time : 2024-06-24 16:36:10
# @Author : intotw
# @File : update_markdown.py
# @Function: Update an existing post in WordPress with a local Markdown file
# @Software: PyCharm
# @Reference: original


import os
import sys
import frontmatter
import markdown
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import GetPosts, EditPost
from config.global_config import GlobalConfig



def find_post(filepath, client):
    """
    find the post in WordPress by using filename in filepath as the searching title
    :param filepath: 更新用的文件路径
    :param client: 客户端
    :return True: if success
    """
    filename = os.path.basename(filepath)  # 例如：test(2021.11.19).md
    filename_suffix = filename.split('.')[-1]  # 例如：md
    filename_prefix = filename.replace('.' + filename_suffix, '')  # 例如：test(2021.11.19)；注意：这种替换方法要求文件名中只有一个".md"
    # 目前只支持 .md 后缀的文件
    if filename_suffix != 'md':
        print('ERROR: not Markdown file')
        return None
    # get pages in batches of 20
    offset = 0  # 每个batch的初始下标位置
    batch = 20  # 每次得到batch个post，存入posts中
    while True:  # 会得到所有文章，包括private(私密)、draft(草稿)状态的
        posts = client.call(GetPosts({'number': batch, 'offset': offset}))
        if len(posts) == 0:
            return None  # no more posts returned
        for post in posts:
            title = post.title
            if title == filename_prefix:
                return post
        offset = offset + batch


def update_post_content(post, filepath, client):
    """
    update a post in WordPress with the content in file path
    :param post: 已发布的文章（WordPressPost类型），由find_post函数得到
    :param filepath: 更新用的文件路径
    :param client: 客户端
    :return True: if success
    """
    post_from_file = frontmatter.load(filepath)  # 读取文档里的信息
    post_content_html = markdown.markdown(post_from_file.content,
                                          extensions=['markdown.extensions.fenced_code']).encode("utf-8")  # 转换为html
    post.content = post_content_html  # 修改内容
    return client.call(EditPost(post.id, post))


def update_post(edit_post_map):
    if not edit_post_map:
        print('No new post to edit.')
        return
    for key in edit_post_map:
        print(f'更新文章: {key}')
    config = GlobalConfig.get_config()
    path = config['settings']['path']
    client = Client(config['settings']['domain'] + '/xmlrpc.php',
                    config['settings']['username'],
                    config['settings']['password'])

    find_map = {}
    lower_edit_post_map = {k.lower(): v for k, v in edit_post_map.items()}
    # 查找到所有需要更新的文章的信息
    offset = 0  # 每个batch的初始下标位置
    batch = 20  # 每次得到batch个post，存入posts中
    while True:  # 会得到所有文章，包括private(私密)、draft(草稿)状态的
        posts = client.call(GetPosts({'number': batch, 'offset': offset}))
        if len(posts) == 0:
            break  # no more posts returned
        for post in posts:
            post_name = post.struct['post_name']
            if post_name.lower() in lower_edit_post_map:
                find_map[post_name] = post
        offset = offset + batch

    for key, value in find_map.items():
        update_post_content(value, os.path.join(path, key + '.md'), client)




