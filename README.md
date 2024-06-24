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