import sys
import os


def main():
    if len(sys.argv) > 2:
        print('Python: Got args {} and {} from React'.format(sys.argv[1], sys.argv[2]))
    else:
        print('Got no args from React')
    print('The current working directory is {}'.format(os.getcwd()))


if __name__ == '__main__':
    main()
