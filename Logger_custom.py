from datetime import datetime
import os


# Append 'hello' at the end of file
def AppendLog(record):
    os.chdir('Log_files')
    file_object = open('log.txt', 'a+')
    addstr = ""
    addstr += '\n' + record
    addstr += '        ' + datetime.now().strftime("(%m.%d.%Y_%H.%M.%S)")
    file_object.write(addstr)
    file_object.close()
    os.chdir('../')