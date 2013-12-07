import os
import mimetypes
import urllib

if QUERY_DICT:
    filename = urllib.unquote(QUERY_DICT['f'][0])
    
    mime = mimetypes.guess_type(filename)

    path = os.path.join("Downloads", filename)
    head={'Content-Disposition':'attachment; filename="%s"' %(filename)}
    self.send_200(mime_type=mime, headers=head)
    with open(path) as f:
       self.wfile.write(f.read())

else:
    self.redirect("index.py")