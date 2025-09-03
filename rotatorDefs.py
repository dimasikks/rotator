import subprocess
import string

def fileCounter(dir, file):
    args = { "capture_output":True, "text": True, "cwd": dir, "shell": True }

    command = []
    countCommand = f''' ls {file}.*.gz 2>/dev/null | wc -l'''
    command.append(countCommand)

    result = subprocess.run(command, **args)
    del command

    return int(result.stdout)

def updateFileCount(dir, file):
    args = { "capture_output":True, "text": True, "cwd": dir, "shell": True }

    command = []
    findOldLogs = f''' ls -rt {file}.*.gz | head -n 1 |'''
    findOldLogsAppender = r''' awk -F '.' '{print$(NF-1)}' '''
    command.append(findOldLogs + findOldLogsAppender)

    result = subprocess.run(command, **args)
    del command

    return int(result.stdout)

def rotateLogs(dir, file, fileCount):
    args = { "capture_output":True, "text": True, "cwd": dir, "shell": True }
    
    command = []
    rotateCommand = f'''find . -type f -name "{file}" -exec bash -c 'gzip -c \"$1\" > \"$1.{fileCount}.gz\"; echo 1 > \"$1\"' '''
    rotateCommandAppender = r''' _ {} \; '''
    command.append(rotateCommand + rotateCommandAppender)

    result = subprocess.run(command, **args)
    del command
