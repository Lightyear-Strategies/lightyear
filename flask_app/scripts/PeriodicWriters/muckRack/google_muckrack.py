try:
    from googlesearch import search
    import pandas as pd
except ImportError:
    print("No module named 'google' found")

class google_muckrack:
    def __init__(self, dataframe, colname):
        self.df = dataframe
        self.colname = colname

        self.__parse_muckrack()


    def __parse_muckrack(self):
        self.df["Muckrack"] = ""
        for index, row in self.df.iterrows():
            total = len(self.df)
            print("{}/{}".format(index, total))
            name = row[self.colname]
            url = self.__lookUp(name)
            if url != "" and url is not None:
                if not url.endswith("/articles"):
                    url = url + "/articles"
                self.df.at[index, "Muckrack"] = url

    def get_dataframe(self):
        return self.df

    def save_dataframe(self, filename):
        self.df.to_csv(filename)

    def __lookUp(self, name):
        if not isinstance(name, str):
            return 'ERROR'
        if name == '' or len(name) < 3:
            return 'No name given'

        try:
            print("Searching for: " + name)
        except Exception as e:
            print(e)
            return "ERROR"
        query = name + " " + "muckrack"
        for j in search(query, tld="com", num=3, stop=3):
            if "muckrack.com" in j:
                print(j)
                return j

if __name__ == '__main__':
    df = pd.read_csv("valiot_MC.csv")
    gm = google_muckrack(df, 'Name')
    print(gm.get_dataframe().columns)
