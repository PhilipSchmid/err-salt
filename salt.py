from errbot import BotPlugin, botcmd, ShlexArgParser
from optparse import OptionParser

import json
import shlex
import logging
import requests

log = logging.getLogger(name='errbot.plugins.Salt')

try:
    import pepper
except ImportError:
    log.error("Please install 'salt-pepper' python package")


class Salt(BotPlugin):
    """Plugin to run salt commands on hosts"""

    def get_configuration_template(self):
        """ configuration entries """
        config = [
            {
                'environment' : None,
                'paste_api_url': None,
                'api_url': None,
                'api_user': None,
                'api_pass': None,
                'api_auth': None
            }
        ]
        return config

    def pastebin(self, config_dict, data):
      ''' Post the output to pastebin '''
      try:
        clean_data = data
        url = requests.post(
            config_dict['paste_api_url'],
            data={
                'content': clean_data,
            },
        )
        log.debug('url: {}'.format(url))
        return url.text.strip('"')
      except Exception, e:
        return 'Error in pastebin integration.'

    @botcmd
    def salt(self, msg, args):
        ''' executes a salt command on systems,
            using the specified environment
            example:
            !salt prod log*.local cmd.run 'cat /etc/hosts'
            !salt prod log*.local test.ping
        '''
        parser = OptionParser()
        (options, args) = parser.parse_args(shlex.split(args))

        if len(args) < 3:
            response = '3 parameters required. see !help salt'
            self.send(msg.frm,
                      response,
                      in_reply_to=msg,
                      groupchat_nick_reply=True)
            return

        environment = args.pop(0)
        targets = args.pop(0)
        action = args.pop(0)

        config_dict = {entry['environment']:entry for entry in self.config}

        api = pepper.Pepper(config_dict[environment]['api_url'], debug_http=False)
        auth = api.login(config_dict[environment]['api_user'],
                         config_dict[environment]['api_pass'],
                         config_dict[environment]['api_auth'])
        ret = api.local(targets,
                        action,
                        arg=args,
                        kwarg=None,
                        expr_form='pcre')
        results = json.dumps(ret, sort_keys=True, indent=4)
        self.send(msg.frm,
                  results,
                  #self.pastebin(config_dict[environment], results),
                  in_reply_to=msg,
                  groupchat_nick_reply=True)

    @botcmd(split_args_with=ShlexArgParser())
    def salt_grains(self, msg, args):
        ''' executes a salt command on systems
            example:
            !salt grains 'os:Centos' cmd.run 'cat /etc/hosts'
        '''
        if len(args) < 2:
            response = '2 parameters required. see !help salt'
            self.send(msg.frm,
                      response,
                      in_reply_to=msg,
                      groupchat_nick_reply=True)
            return

        environment = args.pop(0)
        targets = args.pop(0)
        action = args.pop(0)

        config_dict = {entry['environment']:entry for entry in self.config}

        api = pepper.Pepper(config_dict[environment]['api_url'], debug_http=False)
        auth = api.login(config_dict[environment]['api_user'],
                         config_dict[environment]['api_pass'],
                         config_dict[environment]['api_auth'])
        ret = api.local(targets,
                        action,
                        arg=args,
                        kwarg=None,
                        expr_form='grain')
        results = json.dumps(ret, sort_keys=True, indent=4)
        self.send(msg.frm,
                  self.pastebin(results),
                  in_reply_to=msg,
                  groupchat_nick_reply=True)
