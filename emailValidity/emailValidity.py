import validate_email
import pandas as pd

#INPUT: filename
#OUTPUT: dataframe
#DESCRIPTION: Checks the csv file for valid email columns
def checkCSV(filanemae):
	try:
		df = pd.read_csv(filanemae)
	except:
		raise("File not found")

	if "email" in df.columns:
		return df
	elif "Email" in df.columns:
		df.rename(columns={"Email":"email"}, inplace=True)
		return df

	else:
		raise("Column not found")

#INPUT: filename, debug
#OUTPUT: updated dataframe
#DESCRIPTION: Goes through the csv file and checks the email column for valid emails
#			  Removes invalid emails and returns a dataframe
def checkTheMail(filename, debug=False):
	df = checkCSV(filename)

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

#INPUT: filename, debug
#OUTPUT: saved dataframe
#DESCRIPTION: Save the dataframe to a csv file
def checkAndSave(filename, debug=False):
	df = checkTheMail(filename, debug)
	filename = filename.split(".")
	df.to_csv(filename[0]+"_updated.csv", index=False)

#INPUT: filename
#OUTPUT: dataframe
#DESCRIPTION: Returns the checked dataframe
def checkAndShow(filename, debug=False):
	return checkTheMail(filename, debug)


if __name__ == '__main__':
	checkAndSave("test.csv", debug=True)
