#!/usr/bin/env python3
import argparse

from pythonosc import osc_message_builder
from pythonosc import udp_client

class VideoProjectionTool:
    #　コンストラクタ
    def __init__(self,ip="127.0.0.1",port=6666):
        self.ip = ip
        self.port = port
        self.client = udp_client.UDPClient(self.ip, self.port)

    # メッセージをビルドし送信するメソッド
    def build_message(self, address,*args):
        msg = osc_message_builder.OscMessageBuilder(address=address)
        for arg in args:
            msg.add_arg(arg)
        msg = msg.build()
        self.client.send(msg)

    def fullscreen(self):
        self.build_message("/fullscreen")

    def blackout(self):
        self.build_message("/blackout")

    def preset(self, preset_num):
        self.build_message("/vpt/preset", preset_num)

    def presetprev(self):
        self.build_message("/vpt/presetprev")

    def presetnext(self):
        self.build_message("/vpt/presetnext")

    def cue(self, cue_num):
        self.build_message("/cue",cue_num)

    def cuenext(self):
        self.build_message("/vpt/cuenext")

    def cueprev(self):
        self.build_message("/vpt/cueprev")

    def sourcepreset(self,source_num):
        self.build_message("/sourcepreset", source_num)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1", required=True, type=str,
      help="The ip of the vpt")
  parser.add_argument("--port", type=int, default=6666, required=True,
      help="The port the vpt is listening on")
  parser.add_argument("--address",  required=True, type=str,
      help="The address of OSC message to send to VPT")
  parser.add_argument("--command",  required=False,
      help="The OSC command to send to VPT")
  args = parser.parse_args()
  vpt = VideoProjectionTool(args.ip, args.port)
  if args.command is not None:
      # ここ型によってはまだ動作しないです。確認中。。。
      vpt.build_message(args.address, args.command)
  else:
      vpt.build_message(args.address)
