import argparse
import os
import sys
import logging

from ConfigParser import ConfigParser

parser = argparse.ArgumentParser(description="""Parse and upload a po file to the server.""")

parser.add_argument('--path_old',
                    dest='path_old',
                    required=True,
                    help="""The path to you current existing version.cfg""")

parser.add_argument('--path_new',
                    dest='path_new',
                    required=True,
                    help="""Path to the version.cfg with the next stable release""")

parser.add_argument('--sections',
                    dest='sections',
                    default=['versions'],
                    nargs='*',
                    help="""Path to the version.cfg with the next stable release""")

class CustomConfigParser(ConfigParser):

    #lame, otherwise its lowercase
    def optionxform(self, optionstr):
        return optionstr


class Handler:
    def __init__(self,args):
        """ """
        self.args=args
        self.old={}
        self.new={}

        if not os.path.exists(self.args.path_old):
            logging.error('Path to old version.cfg does not exist. PATH="%s"'%self.args.path_old)
        if not os.path.exists(self.args.path_new):
            logging.error('Path to new version.cfg does not exist. PATH="%s"'%self.args.path_new)

    def __call__(self):
        """ """

        self._build()

    def _build(self):
        """ """
        #read old
        config_old = CustomConfigParser()
        config_old.read(self.args.path_old)

        #read new
        config_new = CustomConfigParser()
        config_new.read(self.args.path_new)

        for section in self.args.sections:
            for product_name,version in config_new.items(section):
                if config_old.has_option(section,product_name):
                    if version>=config_old.get(section,product_name):
                        config_old.set(section,product_name,version)
                    else:
                        logging.info(product_name+' version is newer in old. NOTHING DONE')
                else:
                    logging.info(product_name+' does not exists in old. ADDED')
                    config_old.set(section,product_name,version)
        config_old.write(open(self.args.path_old,'w'))


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    args = parser.parse_args()
    handler=Handler(args)
    handler()


if __name__ == '__main__':
    sys.exit(main())
