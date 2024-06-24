# -*- coding: utf-8 -*-
# @Time : 2024-06-24 16:36:23
# @Author : intotw
# @File : upload_markdown.py
# @Function: Upload new posts in WordPress with local Markdown files
# @Software: PyCharm
# @Reference: original

import os  # 用来遍历文件路径
import sys
import time

# 1 导入frontmatter模块
import frontmatter

# 2 导入markdown模块
import markdown

# 3 导入wordpress_xmlrpc模块
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

from config.global_config import GlobalConfig


def make_post(filepath, metadata):
    """
    make a WordPressPost for Client call
    :param filepath: 要发布的文件路径
    :param metadata: 字典类型
             包括 metadata['category']: 文章分类
                  metadata['tag']: 文章标签
                  metadata['status']: 有publish发布、draft草稿、private隐私状态可选
    :return WordPressPost: if success
            None: if failure
    """
    filename = os.path.basename(filepath)  # 例如：test(2021.11.19).md
    filename_suffix = filename.split('.')[-1]  # 例如：md
    filename_prefix = filename.replace('.' + filename_suffix, '')  # 例如：test(2021.11.19)；注意：这种替换方法要求文件名中只有一个".md"

    # 目前只支持 .md 后缀的文件
    if filename_suffix != 'md':
        return None

    # 1 通过frontmatter.load函数加载读取文档里的信息，包括元数据
    post_from_file = frontmatter.load(filepath)

    # 2 markdown库导入内容
    post_content_html = markdown.markdown(post_from_file.content, extensions=['markdown.extensions.fenced_code'])
    post_content_html = post_content_html.encode("utf-8")

    # 3 将本地post的元数据暂存到metadata中
    metadata['title'] = filename_prefix  # 将文件名去掉.md后缀，作为标题
    # metadata['slug'] = metadata['title']  # 别名
    metadata_keys = metadata.keys()
    # 如果post_from_file.metadata中的属性key存在，那么就将metadata[key]替换为它
    for key in metadata_keys:
        if key in post_from_file.metadata:  # 若md文件中没有元数据'category'，则无法调用post.metadata['category']
            metadata[key] = post_from_file.metadata[key]

    # 4 将metadata中的属性赋值给post的对应属性
    post = WordPressPost()  # 要返回的post
    post.content = post_content_html
    post.title = metadata['title']
    # post.slug = metadata['slug']
    post.post_status = metadata['status']
    post.date = metadata["date"]
    post.date_modified_gmt = metadata["lastmod"]
    post.slug = filename_prefix
    post.terms_names = {
        'category': metadata['categories'],
        'post_tag': metadata['tags']
    }
    post.comment_status = 'open'  # 开启评论
    return post


def push_post(post, client):
    """
    上传post到WordPress网站
    :param post: 要发布的文章（WordPressPost类型），由make_post函数得到
    :param client: 客户端
    :return True: if success
    """
    return client.call(NewPost(post))


def unload_new_post(new_post_map):
    if not new_post_map:
        print('No new post to upload.')
        return
    for key in new_post_map:
        print(f'新增文章: {key}')
    config = GlobalConfig.get_config()
    path = config['settings']['path']
    client = Client(config['settings']['domain'] + '/xmlrpc.php',
                    config['settings']['username'],
                    config['settings']['password'])  # 客户端
    filepaths = []
    for key in new_post_map:
        filepaths.append(f"{path}/{key}.md")
    # Optional Configuration
    post_metadata = {
        'categories': ['博客存档'],  # 文章分类
        'tags': ['博客存档'],  # 文章标签
        'status': 'publish',  # 可选publish发布、draft草稿、private隐私状态
        'date': time.localtime(),  # 可选publish发布、draft草稿、private隐私状态
        'lastmod': time.localtime()  # 可选publish发布、draft草稿、private隐私状态
    }
    for filepath in filepaths:
        post = make_post(filepath, post_metadata)
        filename = os.path.basename(filepath)
        if post is not None:
            push_post(post, client)
            print('SUCCESS: Push "%s" completed!' % filename)
        else:
            print('ERROR: Push "%s" failed!' % filename)

