from threading import Thread
import validate_email
import pandas as pd

#INPUT: filename, type
#OUTPUT: dataframe
#DESCRIPTION: Checks the csv file for valid email columns
#			  Accepted filetype: csv, tsv,xlsx
def checkCSV(filename, type, debug=False, multi=False):
	if(type == "csv"):
		try:
			df = pd.read_csv(filename)
		except:
			raise Exception("File not found")
	elif(type == "xlsx"):
		try:
			df = pd.read_excel(filename)
		except:
			raise Exception("File not found")
	else:
		raise Exception("Invalid file type")

	#refractor this code
	if "email" in df.columns:
		pass
	elif "Email(s)" in df.columns:
		df.rename(columns={"Email(s)":"email"}, inplace=True)
	elif "Email" in df.columns:
		df.rename(columns={"Email":"email"}, inplace=True)
	else:
		raise Exception("Column not found")

	if multi:
		return multiprocess(df, debug)
	else:
		return checkTheMail(df, debug)

#INPUT: filename, debug, type
#OUTPUT: updated dataframe
#DESCRIPTION: Goes through the csv file and checks the email column for valid emails
#			  Removes invalid emails and returns a dataframe
def checkTheMail(df, debug=True):
	total = len(df)
	for i in range(0, len(df["email"])):
		currLength = len(df["email"])
		if debug:
			print("Checked ", i+1, "out of ", total, "(current length: ", currLength, ")")
		try:
			validate_email.validate_email_or_fail(
								email_address=df["email"][i],
								check_format=True,
								check_dns=True,
								check_smtp=True,
								smtp_from_address="xakel6@gmail.com")
		except Exception as e:
			if "Hui" in str(e):
				continue
			else:
				if(debug):
					print(e)
				df.drop(i, inplace=True)
	return df

#INPUT: filename, debug, type
#OUTPUT: saved dataframe
#DESCRIPTION: Save the dataframe to a csv file
# 			  Use type to specify the file type
def checkAndSave(filename, type, debug=True, multi=False):
	df = checkCSV(filename, type, debug, multi)
	filename = filename.split(".")
	df.to_csv(filename[0]+"_clean.csv", index=False)

#INPUT: filename, debug, type
#OUTPUT: dataframe
#DESCRIPTION: Returns the checked dataframe
# 			  Use type to specify the file type
def checkAndShow(filename, type, debug=True, multi=False):
	return checkCSV(filename, type, debug, multi)

def multiprocess(df, debug=True):
	#split dataframe into 4 parts with new index
	df1 = df.iloc[0:len(df)//4]
	df2 = df.iloc[len(df)//4:len(df)//2]
	df3 = df.iloc[len(df)//2:len(df)*3//4]
	df4 = df.iloc[len(df)*3//4:len(df)]

	#reindex the dataframes
	df1.index = range(0, len(df1))
	df2.index = range(0, len(df2))
	df3.index = range(0, len(df3))
	df4.index = range(0, len(df4))

	#create threads
	t1 = Thread(target=checkTheMail, args=(df1, debug))
	t2 = Thread(target=checkTheMail, args=(df2, debug))
	t3 = Thread(target=checkTheMail, args=(df3, debug))
	t4 = Thread(target=checkTheMail, args=(df4, debug))

	#start threads
	t1.start()
	t2.start()
	t3.start()
	t4.start()

	#join threads
	t1.join()
	t2.join()
	t3.join()
	t4.join()

	#combine dataframes
	df = pd.concat([df1, df2, df3, df4])
	df.index = range(0, len(df))

	#save dataframe
	return df


if __name__ == '__main__':
	print(checkAndShow("ChoiceNYoutlets.csv", "csv", True, True))

