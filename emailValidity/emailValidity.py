from threading import Thread
import validate_email
import pandas as pd
import os


class emailValidation:
	# Constructor
	# @param: filename — path, type — csv/xlsx, multi — multi-threading for faster processing
	def __init__(self, filename=None, type=None, debug=False, multi=False):
		self.filename = filename
		self.type = type
		self.debug = debug
		self.multi = multi
		self.df = None
		#length
		self.initialLength = None
		self.finalLength = None

		url = "http://www.kite.com"
		timeout = 5
		try:
			request = requests.get(url, timeout=timeout)
			print("Connected to the Internet")
		except (requests.ConnectionError, requests.Timeout) as exception:
			print("No internet connection.")

		self.checkCSV()

	# Check if the file is a csv or xlsx
	# @return: Validates the file or throws an error
	def checkCSV(self):
		if self.type == "csv":
			try:
				df = pd.read_csv(self.filename)
			except:
				raise Exception("File not found")
		elif self.type == "xlsx":
			try:
				df = pd.read_excel(self.filename)
			except:
				raise Exception("File not found")
		else:
			raise Exception("Invalid file type")

		# Change this code
		if "email" in df.columns:
			df.rename(columns={"email": "Email(s)"}, inplace=True)
		elif "Email(s)" in df.columns:
			pass
		elif "Email" in df.columns:
			df.rename(columns={"Email": "Email(s)"}, inplace=True)
		else:
			raise Exception("Column not found")

		self.df = df
		self.initialLength = len(df)

	# Validate the email
	# @param: data — either .self.df or a list of emails
	# @return: Validates the email or removes it from the dataframe
	def checkTheMail(self, data=None, threadNum = None):
		if data is None:
			data = self.df
		total = len(data)
		for i in range(0, len(data["Email(s)"])):
			currLength = len(data["Email(s)"])
			if self.debug:
				if threadNum:
					print(f"Checked {i+1} out of {total} (current length: {currLength}) in Thread №{threadNum}")
				else:
					print(f"Checked {i + 1} out of {total} (current length: {currLength})")
			try:
				validate_email.validate_email_or_fail(
									email_address=data["Email(s)"][i],
									check_format=True,
									check_dns=True,
									check_smtp=True,
									smtp_from_address="xakel6@gmail.com")
			except Exception as e:
				if "550" in str(e):
					continue
				else:
					if self.debug:
						print(e)
					data.drop(i, inplace=True)

		if self.multi:
			return data
		else:
			self.df = data
			self.finalLength = len(data)

	# Validate the emails in a thread
	# @return: Validates the emails or throws an error
	def multiprocess(self):
		# split dataframe into 4 parts with new index
		initial = len(self.df)

		df1 = self.df.iloc[0:initial//4]
		df2 = self.df.iloc[initial//4:initial//2]
		df3 = self.df.iloc[initial//2:initial*3//4]
		df4 = self.df.iloc[initial*3//4:initial]

		# reindex the dataframes
		df1.index = range(0, len(df1))
		df2.index = range(0, len(df2))
		df3.index = range(0, len(df3))
		df4.index = range(0, len(df4))

		# create threads
		t1 = Thread(target=self.checkTheMail, args=(df1,"1"))
		t2 = Thread(target=self.checkTheMail, args=(df2,"2"))
		t3 = Thread(target=self.checkTheMail, args=(df3,"3"))
		t4 = Thread(target=self.checkTheMail, args=(df4,"4"))

		# start threads
		t1.start()
		t2.start()
		t3.start()
		t4.start()

		# join threads
		t1.join()
		print("********************************************************")
		print("THREAD 1 COMPLETE")
		print("********************************************************")
		t2.join()
		print("********************************************************")
		print("THREAD 2 COMPLETE")
		print("********************************************************")
		t3.join()
		print("********************************************************")
		print("THREAD 3 COMPLETE")
		print("********************************************************")
		t4.join()
		print("********************************************************")
		print("THREAD 4 COMPLETE")
		print("********************************************************\n")

		# combine dataframes
		df = pd.concat([df1, df2, df3, df4])

		df.index = range(0, len(df))
		print("Initial length: ", initial)
		print("Final length: ", len(df))
		self.df = df
		self.finalLength = len(df)

	# Initiates the checks
	# @param: save — save the dataframe to a csv
	# @return: cleaned dataframe
	def check(self, save=False, inplace=False):
		if self.multi:
			self.multiprocess()
		else:
			self.checkTheMail()
		print('Checked before saving')
		if save:
			filename = os.path.basename(self.filename)
			if inplace:
				saveLocation = "../flask/uploadFolder/"
				filename = saveLocation+filename
			else:
				saveLoaction = "..flask/uploadFolder/"
				filename = saveLocation+filename.split(".")+"_clean.csv"

			self.df.to_csv(filename, index=False)
			return self.df
		else:
			return self.df

	def setFilename(self, filename):
		if type(filename) is str:
			self.filename = filename
		else:
			raise Exception("Invalid file type")

	def setType(self, type):
		if type == "csv" or type == "xlsx":
			self.type = type
		else:
			raise Exception("Invalid file type")

	def setMulti(self, multi):
		if type(multi) is bool:
			self.multi = multi
		else:
			raise Exception("Invalid file type")

	def setDebug(self, debug):
		if type(debug) is bool:
			self.debug = debug
		else:
			raise Exception("Invalid file type")

	def getFinalLength(self):
		return self.finalLength

	def getInitialLength(self):
		return self.initialLength


if __name__ == '__main__':
	valid = emailValidation(filename="test.csv", type="csv", debug=True, multi=True)
	valid.check(save=True)

