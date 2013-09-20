import argparse
import os
import sys
import logging
import sys
import shutil

from ConfigParser import ConfigParser

parser = argparse.ArgumentParser(description="""Remove no longer used eggs. Be sure you use a valid directory.""")

parser.add_argument('--egg_directory',
                    required=True,
                    dest='egg_directory',
                    help="""Path to the egg directory.""")

logger = logging.getLogger('clenaupeggs')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

class Handler:

    def __init__(self,args):
        """ """
        self.args=args
        self.egg_directories={}

        if not self.args.egg_directory.endswith(os.sep):
            self.args.egg_directory+=os.sep

        if not os.path.exists(self.args.egg_directory):
            logger.error('Path to egg directory. PATH="%s"'%self.args.path_old)


    def __call__(self):

        self.egg_directories

        for name in os.listdir(self.args.egg_directory):
            if not name.endswith('.egg'):
                raise Exception("""Files in egg directory are not valid. Directory should only contain files/directories with *.egg %s is a problem."""%(self.args.egg_directory+name))

            self.egg_directories[self.args.egg_directory+name]=1

        list_=[]
        for path in sys.path:

            if self.egg_directories.has_key(path):
                del self.egg_directories[path]

        if self.egg_directories:

            logger.info(('-'*20)+' INFORMATION '+('-'*20))
            logger.info('')
            logger.info('It could be possible that eggs are listed for deletion, wich are used in buildout but not while startup instance. These eggs will be deleted but back while the next buildout.')
            logger.info('')
            logger.info(('-'*20)+'INFORMATION'+('-'*20))

            logger.info(('-'*6)+' THE FOLLOWING EGGS SEEMS TO BE UNUSED '+('-'*6))
            logger.info('')
            for k in self.egg_directories.keys():
                logger.info(k)
            logger.info('')
            logger.info(('-'*6)+' THE FOLLOWING EGGS SEEMS TO BE UNUSED '+('-'*6))
            logger.info('')

            input_=raw_input('Do you want to delete them? y=yes, n=no:').strip()
            if input_ not in ['n','y']:
                logger.error('Shell input was not valid. You entered: %s'%input_)
            if input_=='y':
                for k in self.egg_directories.keys():
                    if os.path.isdir(k):
                        shutil.rmtree(k)
                    else:
                        os.unlink(k)
                    logger.info(k+' was removed.')


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    args = parser.parse_args()
    handler=Handler(args)
    handler()


if __name__ == '__main__':
    sys.exit(main())
