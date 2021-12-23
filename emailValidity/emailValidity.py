import validate_email
import pandas as pd

#INPUT: filename, type
#OUTPUT: dataframe
#DESCRIPTION: Checks the csv file for valid email columns
#			  Accepted filetype: csv, tsv,xlsx
def checkCSV(filename, type):
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

	if "email(s)" in df.columns:
		return df
	elif "Email(s)" in df.columns:
		df.rename(columns={"Email(s)":"email"}, inplace=True)
		return df

	else:
		raise Exception("Column not found")

#INPUT: filename, debug, type
#OUTPUT: updated dataframe
#DESCRIPTION: Goes through the csv file and checks the email column for valid emails
#			  Removes invalid emails and returns a dataframe
def checkTheMail(filename, type, debug):
	df = checkCSV(filename, type)

	for i in range(0, len(df["email"])):
		if debug:
			print(i, len(df["email"]))
		try:
			validate_email.validate_email_or_fail(
								email_address=df["email"][i],
								check_format=True,
								check_dns=True,
								check_smtp=True)
		except Exception as e:
			if(debug):
				print(e)
			df.drop(i, inplace=True)

	return df

#INPUT: filename, debug, type
#OUTPUT: saved dataframe
#DESCRIPTION: Save the dataframe to a csv file
# 			  Use type to specify the file type
def checkAndSave(filename, type, debug=False):
	df = checkTheMail(filename, type, debug)
	filename = filename.split(".")
	df.to_csv(filename[0]+"_updated.csv", index=False)

def checkAndSave2(filepath,safepath, type, debug=False):
	df = checkTheMail(filepath, type, debug)
	filename = filepath.split("/")[-1]
	filename = filename.split(".")[0]
	df.to_csv(safepath+filename+"_updated.csv", index=False)

#INPUT: filename, debug, type
#OUTPUT: dataframe
#DESCRIPTION: Returns the checked dataframe
# 			  Use type to specify the file type
def checkAndShow(filename, type, debug=False):
	return checkTheMail(filename, type, debug)


if __name__ == '__main__':
	checkAndSave("test.csv", debug=True, type="csv")
