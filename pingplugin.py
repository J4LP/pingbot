from errbot import BotPlugin, botcmd, webhook, abort
from itsdangerous import Serializer


class PingPlugin(BotPlugin):

    def get_configuration_template(self):
		return {'SECRET_KEY': "Example value"}

    @webhook
    def ping(self, incoming_request):
        serializer = Serializer(self.config['SECRET_KEY'])
        try:
            req = serializer.loads(incoming_request)
        except Exception:
            abort(403)
        self._bot.conn.client.register_plugin('xep_0033')
        message = self._bot.conn.client.Message()
        message['to'] = 'multicast.j4lp.com'
        message['body'] = req['body']
        for user in req['users']:
            message['addresses'].addAddress(atype='bcc', jid=user)
        message.send()
        return incoming_request
