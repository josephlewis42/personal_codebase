import os

if POST_DICT:
    try:
        print POST_DICT.keys()
        print POST_DICT['filename']
        path = os.path.join("Downloads", POST_DICT['filename'])
        print path

        with open(path, 'wb') as f:
           f.write(POST_DICT['myfile'])
    except Exception, e:
        print e

self.redirect("index.py")