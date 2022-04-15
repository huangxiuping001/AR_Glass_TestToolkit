
import os

# 比对2个文本文件中对应翻译记录是否一致
class analyze:

    def compare(self, arrayA, arrayB):

        number = 0
        for language in arrayA:
            # print("key = " + key)
            # print("value + " + value)

            # 遍历字典A
            for audio in arrayA[language]:
                # 如果字典A的语种key在字典B中则继续
                if language in arrayB.keys():
                    # 如果字典A中当前音频的key在字典B中则继续
                    if audio in arrayB[language].keys():
                        client_value = arrayA[language][audio].rstrip(".")
                        research_value = arrayB[language][audio].rstrip(".")

                        # print("client_value = " + client_value)
                        # print("research_value = " + research_value)

                        if client_value != research_value:
                            number += 1
                            print("Not Equal : Language = " + language + ", Audio = " + audio + "\n"
                                  + "Client_Result = " + client_value + "\n" +
                                  "Target_Result = " + research_value + "\n")
                    else:
                        print("research don't contain this audio, name = " + audio + ", language = " + language)
                else:
                    print("language name not equal, client_language = " + language)

        print("Unequals number : " + str(number))

    def deal_file(self, dir_path = ""):

        result = []

        if os.path.isdir(dir_path):

            for kind in os.listdir(dir_path):

                database = {}

                if os.path.isdir(dir_path + "\\" + kind):
                    for file in os.listdir(dir_path + "\\" + kind):
                        language = file.split(".")[0]
                        scene = {}

                        file = open(dir_path + "\\" + kind + "\\" + file, 'rb')
                        for line in file:
                            if line:
                                line = str(line, encoding='utf-8').strip()

                                line = line.split("\t")

                                if len(line) == 2:
                                    scene[line[0]] = line[1]
                                else:
                                    scene[line[0]] = '__'

                        database[language] = scene
                        file.close()

                result.append(database)

        # print(result)
        return result

if __name__ == '__main__':

    obj = analyze()

    data = obj.deal_file("E:\\python_home\\untitled\\data2")
    # print(data[0])
    #
    #
    # print(data[1])

    obj.compare(data[0], data[1])