from errbot import BotPlugin, botcmd, webhook
from bottle import abort
from itsdangerous import URLSafeSerializer


class PingPlugin(BotPlugin):

    def get_configuration_template(self):
        return {'SECRET_KEY': "Example value"}

    @webhook
    def ping(self, incoming_request):
        serializer = URLSafeSerializer(self.config['SECRET_KEY'])
        req = serializer.loads(incoming_request['payload'])
        self._bot.conn.client.register_plugin('xep_0033')
        message = self._bot.conn.client.Message()
        message['to'] = 'multicast.j4lp.com'
        message['body'] = req['body']
        for user in req['users']:
            message['addresses'].addAddress(atype='bcc', jid=user)
        message.send()
        return
