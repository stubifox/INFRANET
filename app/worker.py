import sys
import json
import os


def read_in_stdin():
    return sys.stdin.readline()

#! if sending json to frontend dont forget to flush in printing with flush=True, end=''


def main():
    jsonFilePath = os.path.join(os.path.dirname(
        __file__), '..', 'Log', 'chatLog.json')
    data = read_in_stdin()
    print(data, flush=True, end='')
    with open(jsonFilePath, mode='w', encoding='utf-8') as f:
        json.dump([], f)
    # with open(jsonFilePath, 'r', encoding='utf-8') as jf:
    #     # json.dump(data, jf, ensure_ascii=True)
    #     jf.write(json.loads(data))


if __name__ == '__main__':
    main()
