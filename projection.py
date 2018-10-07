#!/usr/bin/env python3
import argparse

from vpt import VideoProjectionTool
from logging import getLogger

logger = getLogger(__name__)

class ProjectionMapping:
    #　コンストラクタ
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.vpt = VideoProjectionTool(self.ip, self.port)

    def waiting(self):
        self.vpt.preset(1)
        self.vpt.sourcepreset(0)
        self.vpt.sourcepreset(1)
        logger.debug('待機画面投影')

    def normal_cross(self):
        self.vpt.preset(1)
        self.vpt.sourcepreset(0)
        self.vpt.sourcepreset(2)
        logger.debug('通常横断歩道投影')

    def arukisumaho(self):
        self.vpt.preset(1)
        self.vpt.sourcepreset(0)
        self.vpt.sourcepreset(3)
        logger.debug('歩きスマホ投影')

    def wide_cross(self):
        self.vpt.preset(1)
        self.vpt.sourcepreset(0)
        self.vpt.sourcepreset(4)
        logger.debug('大人数向け横断歩道投影')
