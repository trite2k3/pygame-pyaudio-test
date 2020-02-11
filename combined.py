#!/usr/bin/python3
import pygame
import math
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import pyaudio
import wave
import sys
import numpy as np

CHUNK = 1024
maxValue = 2**16
#TARGET = 8000
TARGET = 3000
#3000 for ultrasonic
#6000 for haunted
#6000 for main
#TARGET2 = 7000
TARGET2 = 8000
#8000 for ultrasonic
#9000 for haunted
#8000 for main

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

#x, y, z
verticies = (
    (-6, -6, 0),  #A, 0
    (-6, -4, 0),  #B, 1
    (-4, -4, 0),  #C, 2
    (-1, 2,0),  #D, 3
    (-1, 4, 0),  #E, 4
    (-3, 4, 0),  #F, 5
    (-3, 6, 0),  #G, 6
    (-1, 6, 0),  #H, 7
    (1, 4, 0),  #I, 8
    (1, 2, 0),  #EXTRA, 9
    (4, -4, 0),  #J, 10
    (5, -4, 0),  #K, 11
    (5, -6, 0),  #L, 12
    (3, -6, 0),  #M, 13
    (0, 0, 0),  #N, 14
    (-3, -6, 0),  #O, 15
    (-6, -6, 2),  #A, 16
    (-6, -4, 2),  #B, 17
    (-4, -4, 2),  #C, 18
    (-1, 2, 2),  #D, 19
    (-1, 4, 2),  #E, 20
    (-3, 4, 2),  #F, 21
    (-3, 6, 2),  #G, 22
    (-1, 6, 2),  #H, 23
    (1, 4, 2),  #I, 24
    (1, 2, 2),  #EXTRA, 25
    (4, -4, 2),  #J, 26
    (5, -4, 2),  #K, 27
    (5, -6, 2),  #L, 28
    (3, -6, 2),  #M, 29
    (0, 0, 2),  #N, 30
    (-3, -6, 2)  #O, 31
    )

edges = (
    (0,1),
    (1,2),
    (2,3),
    (3,4),
    (4,5),
    (5,6),
    (6,7),
    (7,8),
    (8,9),
    (9,10),
    (10,11),
    (11,12),
    (12,13),
    (13,14),
    (14,15),
    (15,0),
    (16, 17),
    (17, 18),
    (18,19),
    (19,20),
    (20,21),
    (21,22),
    (22,23),
    (23,24),
    (24,25),
    (25,26),
    (26,27),
    (27,28),
    (28,29),
    (29,30),
    (30,31),
    (31,16),
    (0,16),
    (1,17),
    (2,18),
    (3,19),
    (4,20),
    (5,21),
    (6,22),
    (7,23),
    (8,24),
    (9,25),
    (10,26),
    (11,27),
    (12,28),
    (13,29),
    (14,30),
    (15,31)
)


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)

    glTranslatef(0.0,0.0, -25)

    #audio init
    wf = wave.open(sys.argv[1], 'rb')
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True,input=True,frames_per_buffer=6144)
    #read data
    #data = wf.readframes(CHUNK)
    RATE = wf.getframerate()
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #audio stop stuff
                stream.stop_stream()
                stream.close()
                p.terminate()
                #
                pygame.quit()
                quit()

        #glRotatef(math.cos(pygame.time.get_ticks()*2), math.cos(pygame.time.get_ticks()/3), math.cos(pygame.time.get_ticks()/2), math.cos(pygame.time.get_ticks()*3))
        #glRotatef(0.5,0.5,0.5,0.5)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        #pygame.time.wait(10)
        #audio volume meter
        data = wf.readframes(CHUNK)
        stream.write(data)
        streamdata = np.frombuffer(stream.read(CHUNK),dtype=np.int16)
        dataL = streamdata[0::2]
        peakL = np.abs(np.max(dataL)-np.min(dataL))/maxValue
        #print(int(peakL*100))
        #val = int(peakL*10)
        val = int(peakL*100)
        #end of volume, start of freq
        fft = abs(np.fft.fft(streamdata).real)
        fft = fft[:int(len(fft)/2)] # keep only first half
        freq = np.fft.fftfreq(CHUNK,1.0/RATE)
        freq = freq[:int(len(freq)/2)] # keep only first half
        assert freq[-1]>TARGET, "ERROR: increase chunk size"
        assert freq[-1]>TARGET2, "ERROR: increase chunk size"
        val2 = fft[np.where(freq>TARGET)[0][0]]
        val3 = fft[np.where(freq>TARGET2)[0][0]]
        val3 = int(val3/1000)
        val2 = int(val2/1000)
        val = int(val/10)
        valslowrot = int(val/1.5)
        #end of freq        
        #glRotatef(val,val2,val,val2)
        #glRotatef(angle,x,y,z)
        if val2 < 30:
            #glRotatef(val,0.1,0,0)
            glRotatef(valslowrot,1,0,0)
        elif val2 > 30 & val2 < 90:
            glRotatef(valslowrot,0,1,0)
        else:
            #glRotatef(val,0,0,0.1)
            glRotatef(val,0,0,1)
        #print(val)
        #print(val2)
        #print(val3)
        if val3 < 90:
            #glTranslate(0,0.1,0)
            glTranslate(0,0,0)
        #elif val3 > 30 & val3 < 60:
            #glTranslate(0,-0.1,0)
            #glTranslate(0,0,0)
        else:
            #glTranslate(0,0,0.1)
            glTranslate(0,0,0.1)

main()
