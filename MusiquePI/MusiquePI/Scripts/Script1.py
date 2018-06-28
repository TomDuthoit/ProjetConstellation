#!/usr/bin/env python
#!/bin/sh
import Constellation
import os
import subprocess
import signal


def OnExit():
    pass

@Constellation.MessageCallback()
def Play(music):
    Mus = os.popen('mpg321 /home/pi/Music/'+music+'.mp3')
    Constellation.WriteInfo(music+" is playing")


def OnStart():
    Constellation.OnExitCallback = OnExit


Constellation.Start(OnStart);