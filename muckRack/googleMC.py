try:
    from googlesearch import search
    import pandas as pd
except ImportError:
    print("No module named 'google' found")

def lookup_MC(name, outlet):
    if not isinstance(name, str):
        return 'ERROR'
    if name == '':
        return 'No name given'
    if not isinstance(outlet, str):
        return 'ERROR'

    try:
        print("Searching for: " + name + " at " + outlet)
    except:
        return "ERROR"
    query = name + " " + outlet + " " + "muckrack"
    for j in search(query, tld="com", num=3, stop=3):
        if "muckrack.com" in j:
            print(j)
            return j





if __name__ == '__main__':
    df = pd.read_csv('rehab_final.csv')
    df['Muckrack'] = ""
    for i in range(len(df)):
        total = len(df)
        print("{}/{}".format(i, total))
        name = df['Name'][i]
        outlet = df['Outlet(s)'][i]
        url = lookup_MC(name, outlet)
        if url != "":
            df['Muckrack'][i] = url
        #update the csv
        df.to_csv('rehab_MC_progress.csv', index=False)
    df.to_csv('rehab_MC.csv', index=False)
