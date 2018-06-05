from slackclient import SlackClient
import os


class SlackBOT:

    def __init__(self):

        self.slack_token = os.environ.get("SLACK_API_TOKEN")
        self.sc = SlackClient(self.slack_token)

    def send_msg(self, msg, chnel):
        if self.slack_token is not None:
            self.sc.api_call(
                "chat.postMessage",
                channel=chnel,
                text=msg
            )
        else:
            print "Erro sending notification on slack."

# SlackBOT().send_msg('oi','#random')