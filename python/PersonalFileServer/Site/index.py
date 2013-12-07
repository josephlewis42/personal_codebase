self.send_200()
self.wfile.write('''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Upload/Download</title>
        <style TYPE="text/css"> 
        body {
            background-color:#ADD8E6;
            text-align:center;
            margin:0px;
            padding:0px;
            font-family:airal,helvetica;
        }
        .main{
            display:block;
            background-color:#E5E5E5;
            margin-left:auto;
            margin-right:auto;
            padding:10px;
            width:800px;
        }
        
        </style>
        
        <script type="text/javascript">
        function getNameFromPath(strFilepath) {
            var objRE = new RegExp(/([^\\/\\\\]+)$/);
            var strName = objRE.exec(strFilepath);
         
            if (strName == null) {
                return null;
            }
            else {
                return strName[0];
            }
        }
        
        function setName()
        {
            document.getElementById('filename').value = getNameFromPath(document.getElementById('up').value);
        }
        </script>
    </head>

    <body>
    <div class="main">
       <H1>Upload / Download Files</H1>
       <form action="upload.py" enctype="multipart/form-data" method="post">
       <input type="file" name="myfile" size="chars" id="up">
       <input name="filename" id="filename" type="hidden"></input>
       <input type="submit" value="Send" onclick="setName()"> 
       </form>
       
       
       <hr>
       <h2>Download</h2>
       <ul>
''')

import os
j = os.listdir("Downloads")
for item in j:
    self.wfile.write("<li><a href='download.py?f=%s'>%s</a></li>" % (item,item))
    
    
self.wfile.write('''
           </ul>
       
    </div>
    </body>
</html>''')