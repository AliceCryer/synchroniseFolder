Project to sychronise local and server files with python
To Run: 
1. modify config.json to desired server name, port, and destination folder
2. run command line 'python src/server.py'
3. run command line 'python src/main.py pathToSource', for example 'src/main.py source'

ToDo:
-Refactor so code runs on a scheduler (currently manual)
-Check security of data transmission (https, add ssl check to requests)
-Check rel and abs paths on windows & unix
