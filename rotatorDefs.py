import subprocess
import string

args = { "capture_output":True, "text": True, "shell": True }

def getFiles(dir, fileName):
    getFilesCommand = f''' ls {fileName}'''

    result = subprocess.run(getFilesCommand, cwd=dir, **args).stdout.strip().split('\n')
    return result

def fileCounter(dir, file):
    countCommand = f''' ls {file}.*.gz 2>/dev/null | wc -l'''

    result = subprocess.run(countCommand, cwd=dir, **args)
    return int(result.stdout)

def deleteOldLogs(dir, file, fileCount, limit):
    extraFilesCount = fileCount - limit
    checkExtraFilesCommand = f''' ls -r {file}.*.gz | head -n {extraFilesCount} '''

    extraFiles = subprocess.run(checkExtraFilesCommand, cwd=dir, **args).stdout.strip().split('\n')

    getOldFilesCommand = f''' ls {file}.*.gz | head -n {limit} '''

    oldFiles = subprocess.run(getOldFilesCommand, cwd=dir, **args).stdout.strip().split('\n')
    
    for oldFile in oldFiles:
        if len(extraFiles) != 0:
            extraFile = extraFiles.pop()
            rewriteOldFileCommand = f''' mv {extraFile} {oldFile} '''
            subprocess.run(rewriteOldFileCommand, cwd=dir, **args)
        else:
            break
            
def updateFileCount(dir, file):
    findOldLogs = f''' ls -rt {file}.*.gz | head -n 1 |'''
    findOldLogsAppender = r''' awk -F '.' '{print$(NF-1)}' '''
    findOldLogsCommand = findOldLogs + findOldLogsAppender

    result = subprocess.run(findOldLogsCommand, cwd=dir, **args)
    return int(result.stdout)

def rotateLogs(dir, file, fileCount, threshold):
    rotateCommand = f'''find . -type f -name "{file}" '''
    rotateCommandExec = f''' -exec bash -c 'gzip -c \"$1\" > \"$1.{fileCount}.gz\"; echo 1 > \"$1\"' '''
    rotateCommandAppender = r''' _ {} \; '''

    if threshold != "":
        rotateCommandSize = f''' -size +{threshold} '''
        rotateFinalCommand = rotateCommand + rotateCommandSize + rotateCommandExec + rotateCommandAppender
    else:
        rotateFinalCommand = rotateCommand + rotateCommandExec + rotateCommandAppender

    result = subprocess.run(rotateFinalCommand, cwd=dir, **args)
