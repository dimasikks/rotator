from rotatorDefs import *
from pathlib import Path
import yaml

with open("rotator.yml", "r", encoding="utf-8") as rotatorYML:
    rotatorMainConfig = yaml.safe_load(rotatorYML)

rotatorConfigsDir=Path(rotatorMainConfig["main"]["configs"])

for simpleConfig in rotatorConfigsDir.iterdir():
    if simpleConfig.is_file():
        if simpleConfig.suffix in [".yml",".yaml"]:
            with simpleConfig.open("r", encoding="utf-8") as simpleRotator:
                rotatorConfig = yaml.safe_load(simpleRotator)
            
            dir = rotatorConfig["dir"]
            files = rotatorConfig["files"]
            limit = rotatorConfig["limit"]

            for file in files:
                fileCount = fileCounter(dir, file)
                if fileCount == limit:
                    fileCount = updateFileCount(dir, file)
                    rotateLogs(dir, file, fileCount)
                else:
                    rotateLogs(dir, file, fileCount+1)
