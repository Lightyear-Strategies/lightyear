import json
import os
import base64

class Haro():
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        if not os.path.exists(self.file_path):
            print('File not found')
            return

        with open(self.file_path, 'r') as f:
            haro_data = json.load(f)


        parsing_body = (haro_data[-1]['payload']['parts'][0]['parts'])

        data = ""
        for part in range(len(parsing_body)):
            data+=parsing_body[part]['body']['data']

        data=base64.urlsafe_b64decode(data)
        #break into lines
        data=data.decode('utf-8')
        #split lines based on "-----------------------------------"
        test = data.split("****************************")

        if(len(test)==2):
            quarries = test[-1].split("-----------------------------------")[:-2]
            for i in quarries[-1].split("\n"):
                print(i)
        else:
            pass



if __name__ == "__main__":
    test = Haro("haro_jsons/test.json")
    test.parse()