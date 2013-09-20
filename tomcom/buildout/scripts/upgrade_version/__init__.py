import argparse
import os
import sys
import logging
import urllib2
from ConfigParser import ConfigParser
import cStringIO
import types
import pkg_resources

parser = argparse.ArgumentParser(description="""Parse and upload a po file to the server.""")

parser.add_argument('--path_old',
                    dest='path_old',
                    required=True,
                    help="""The path to you current existing version.cfg. Complete path with file name.""")

parser.add_argument('--path_new',
                    dest='path_new',
                    help="""Path to the version.cfg with the next stable release. Complete path with file name.""")

parser.add_argument('--url_new',
                    dest='url_new',
                    help="""The url to a versions.cfg.""")

parser.add_argument('--sections',
                    dest='sections',
                    default=['versions'],
                    nargs='*',
                    help="""Only update a special section in version.cfg""")

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
        self.configs_url_new=[]
        self.config_new=None
        if not os.path.exists(self.args.path_old):
            logging.error('Path to old version.cfg does not exist. PATH="%s"'%self.args.path_old)

        if not self.args.path_new:
            if not self.args.url_new:
                logging.error('--path_new or --url_new argument has to be filled.')
        if self.args.path_new and not os.path.exists(self.args.path_new):
            logging.error('Path to new version.cfg does not exist. PATH="%s"'%self.args.path_new)

        if self.args.url_new:
            data=''
            try:
                #Test if config file exists
                fp = urllib2.urlopen(self.args.url_new)
                fp.close()
            except Exception,e:
                logging.error(e)

            self._get_recurse_config([self.args.url_new])

            self.config_new=CustomConfigParser()
            self.config_new.add_section('versions')
            for dict_ in self.configs_url_new:
                for product_name,version_new in dict_.values()[0].items('versions'):
                    if not self.config_new.has_option('versions',product_name):
                        self.config_new.set('versions',product_name,version_new)
                    else:
                        version_existing=self.config_new.get('versions',product_name)
                        print '_________'
                        print version_new
                        print version_existing
                        print pkg_resources.parse_version(version_new)>pkg_resources.parse_version(version_existing)
                        if pkg_resources.parse_version(version_new)>pkg_resources.parse_version(version_existing):
                            self.config_new.set('versions',product_name,version_new)


    def _get_recurse_config(self,urls):
        """ """
        for url in urls:
            print url
            fp = urllib2.urlopen(url)
            string_=fp.read()
            fp.close()

            output = cStringIO.StringIO()
            output.write(string_)
            output.seek(0)

            config=CustomConfigParser()
            config.readfp(output)

            dict_={}
            dict_={url:config}

            self.configs_url_new.append(dict_)

            if 'buildout' in config.sections():
                extends=config.get('buildout','extends')
                if extends:
                    if type(extends) in types.StringTypes:
                        self._get_recurse_config(extends.strip().split())

    def __call__(self):
        """ """

        self._build()

    def _build(self):
        """ """
        #read old
        config_old = CustomConfigParser()
        config_old.read(self.args.path_old)

        if self.config_new:
            config_new=self.config_new
        else:
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
