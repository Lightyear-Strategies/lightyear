try:
    from googlesearch import search
    import pandas as pd
except ImportError:
    print("No module named 'google' found")

class google_muckrack:
    def __init__(self, dataframe, colname):
        self.df = dataframe
        self.targetCol = self.df[colname]

        self.__parse_muckrack()


    def __parse_muckrack(self):
        df = self.df
        df['Muckrack'] = ""
        for i in range(len(df)):
            total = len(df)
            print("{}/{}".format(i, total))
            name = self.targetCol[i]
            url = self.__lookUp(name)
            if url != "" and url is not None:
                if not url.endswith("/articles"):
                    url = url + "/articles"
                df['Muckrack'][i] = url
        self.df = df

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
        except:
            return "ERROR"
        query = name + " " + "muckrack"

        s = list(search(query, num_results=1))[0]
        if "muckrack.com" not in s:
            print("NONE")
            return None
        elif "muckrack.com" in s:
            print(s)
            return s
        # for j in search(query, num_results=1):

        #     if "muckrack.com" in j:
        #         print(j)
        #         return j


if __name__ == '__main__':
    df = pd.read_csv("valiot_MC.csv")
    gm = google_muckrack(df, 'Name')
    gm.get_dataframe()