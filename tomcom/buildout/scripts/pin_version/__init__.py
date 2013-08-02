import argparse
import os
import sys
import logging
import sys


from ConfigParser import ConfigParser

parser = argparse.ArgumentParser(description="""Parse and upload a po file to the server.""")

parser.add_argument('--file_name',
                    dest='file_name',
                    default='versions.cfg',
                    help="""File name for the versions.cfg file""")

class Handler:

    def __init__(self,args):
        """ """
        self.args=args

    def __call__(self):

        list_=[]
        string_='[versions]\n'
        for path in sys.path:
            file_name=path.split(os.sep)[-1]
            if path.endswith('.egg'):
                list_.append(file_name)
            else:
                logging.info(file_name+" is not handled it's no egg")

        list_.sort()

        for file_name in list_:
            splitted=file_name.split('-')
            product_name=splitted[0]
            version=splitted[1]
            product_name=product_name.replace('_','-')
            string_+='%s = %s\n'%(product_name,version)

        open(self.args.file_name,'w').write(string_[:-1])

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    args = parser.parse_args()
    handler=Handler(args)
    handler()


if __name__ == '__main__':
    sys.exit(main())
