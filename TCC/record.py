'''Here the file operations are done'''
import datetime

file = []

def setName(now):
    day = '{:02d}'.format(now.day)
    month = '{:02d}'.format(now.month)
    year = str(now.year)
    date = day + '-' + month + '-' + year

    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    time = hour + ':' + minute


    return date + '.' + time + '.txt'

def newFile():
	global file
	now = datetime.datetime.now()
	file = open(setName(now), "a") 

def write(text):
	file.write(text)

def close():
	file.close()