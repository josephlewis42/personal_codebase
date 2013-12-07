''' Opens .xlsx files as if they were .csv files. '''
import zipfile
import xml.dom.minidom
import re

class XLSXReader:
    rows=[]
    
    def _nodeText(self, node):
        return "".join(t.nodeValue for t in node.childNodes if t.nodeType == t.TEXT_NODE)
        
    def _get_col_num(self, col):
        
        strpart = col.attributes['r'].value
        colnum = re.sub('[^A-Z]', '', strpart.upper().strip())
        
        c = 0
        for char in colnum:
            c += ord(char)
        
        c -= (65) # ASCII to number
        
        print("Colnum for '%s' is %s" % (strpart, c))
        
        return c

    
    def __init__(self, filename):
        shared_strings = []
        self.rows = []
        myFile = zipfile.ZipFile(filename)
        
        # Read the shared strings file.
        share = xml.dom.minidom.parseString(myFile.read('xl/sharedStrings.xml'))
        j = share.getElementsByTagName("t")

        for node in j:
            shared_strings.append(self._nodeText(node))
        
        sheet = xml.dom.minidom.parseString(myFile.read('xl/worksheets/sheet1.xml'))
        sheetrows = sheet.getElementsByTagName("row")
        for row in sheetrows:
            cols = row.getElementsByTagName("c")
            
            largest_col_num = 0
            for col in cols:
                colnum = self._get_col_num(col)
                if colnum > largest_col_num:
                    largest_col_num = colnum
                
            thiscol = ['']*(largest_col_num + 1)
            
            for col in cols:
                value = ""
                try:
                    value = self._nodeText(col.getElementsByTagName('v')[0])
                except IndexError:
                    continue
                
                #Get col number (A=0, B=1, etc. up to AA)
                
                colnum = self._get_col_num(col) # ASCII to number
                
                try:
                    if col.attributes['t'].value == 's':
                        thiscol[colnum] = shared_strings[int(value)]
                    else:
                        thiscol[colnum] = value
                except KeyError:
                    continue
            self.rows.append(thiscol)
            
        myFile.close()
     
    def __getitem__(self, i):
        return self.rows[i]