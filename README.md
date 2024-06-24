# How to use
1. fill your config in config.yml
2. run `main.py`

# How to hold update

## different compare
1. the program will save all md5 of the files in the files_md5_map_snapshot.txt after running.
2. when run twice or more, the program will compare the md5 of the files in the files_md5_map_snapshot.txt with the files in the folder.
3. if the md5 is different, the program will update the post to the server.

## upload way
1. the program will use the filename(without .md suffix) as post.slug to upload,it will appear as post_name when query the post list.
2. when update happened, the program will use the filename(without .md suffix) to find post by post_name，
3. then edit the content of the post.

# Some YAML Front Matter mapping

in YAML Front Matter, program do some mapping

| YAML Front Matter      | wordpress                                                 |
| ----------- |-----------------------------------------------------------|
| title      | the title of post                                         |
| date   | the create_date of post e.g 2024-03-26T16:46:04+08:00     |
| tags: ["tt"]   | the tags of the post                                      |
| categories: ["tp"]   | the categories of the post                                |
| lastmod: ["tp"]   | the update_time of the post e.g 2024-03-26T16:46:04+08:00 |


# 如何使用
1. 在config.yml中填写您的配置
2. 运行“main.py”

# 如何保持更新

## 不同的比较
1. 程序运行后将所有文件的md5保存在files_md5_map_snapshot.txt文件中。
2. 当运行两次或更多次时，该程序将比较files_md5_map_snapshot.txt中文件的md5与文件夹中的文件的md5。
3. 如果md5不同，程序将更新到服务器的帖子。

## 上传方式
1. 该程序将使用文件名(没有。md后缀)作为post。要上传的字段，在查询帖子列表时将显示为post_name。
2. 当更新发生时，程序将使用文件名(没有。md后缀)通过post_name查找post，
3. 然后编辑文章的内容。

# 一些YAML的前内容映射

在YAML Front Matter中，程序做一些映射

| YAML首页| wordpress |
| ----------- |-----------------------------------------------------------|
| title |文章标题 |
date | post的create_date，例如2024-03-26T16:46:04+08:00|
| tags: ["tt"] |文章的标签|
| categories: ["tp"] |文章的类别|
| lastmod: ["tp"] | post的update_time，例如:2024-03-26T16:46:04+08:00|