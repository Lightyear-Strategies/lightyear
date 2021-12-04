import validate_email
import pandas as pd

df = pd.read_csv("test.csv")


def checkTheMail(name):
	try:
		isValid=validate_email.validate_email_or_fail(
				email_address=name,
				check_format=True,
				check_dns=True,
				check_smtp=True)
	except Exception as e:
		reply=[name, e]
		array.append(reply)


for idx, row in df.iterrows():
	print(idx, len(df))
	checkTheMail(row[0])
