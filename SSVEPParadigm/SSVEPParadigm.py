import pygame;
import sys;
import numpy;
from Utils  import Utils;


class SSVEPParadigm(object):
    def __init__(self, windowHight, windowWidth):
        self._windowHight = windowHight;
        self._windowWidth = windowWidth;
        self._freqs = numpy.array([30, 15, 12, 8.57, 7.5, 6.6667]);
        self._delays = 1000 / self._freqs;
        self._BLACK = (0,0,0);
        self._WHITE = (255,255,255);
        self._RED = (255,0,0);
        self._rects = [
            {
                "rect" : (10,10,10,10),
                "freq": self._freqs[0],
                "delay": self._delays[0],
                "nextevent" : 0,
                "color": self._BLACK,
                "show": True,
            },{
                "rect" : (30,10,10,10),
                "freq": self._freqs[2],
                "delay": self._delays[2],
                "nextevent" : 0,
                "color": self._BLACK,
                "show": True,
            },{
                "rect" : (50,10,10,10),
                "freq": self._freqs[3],
                "delay": self._delays[3],
                "nextevent" : 0,
                "color": self._BLACK,
                "show": True,
            },{
                "rect" : (70,10,10,10),
                "freq": self._freqs[4],
                "delay": self._delays[4],
                "nextevent" : 0,
                "color": self._BLACK,
                "show": True,
            },{
                "rect" : (90,10,10,10),
                "freq": self._freqs[5],
                "delay": self._delays[5],
                "nextevent" : 0,
                "color": self._BLACK,
                "show": True,
            },
            ];

        self._displayFuncHandle = self.display();

    @Utils.thread
    def display(self):
        pygame.init();
        fenetre = pygame.display.set_mode((500, 400), 0, 32)

        # time in millisecond from start program 
        current_time = pygame.time.get_ticks()

        self.getNextEvent_allRects(current_time);

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit();

            current_time = pygame.time.get_ticks();

            fenetre.fill(self._BLACK);

            for rect in self._rects:
                if current_time >= rect.nextevent:
                    rect.nextevent = current_time + delay;
                    rect.show = not rect.show;

                if rect.show:
                    pygame.draw.rect(fenetre, self._WHITE, rect.rect);

            pygame.display.update();
            

            


    def getNextEvent_allRects(self, current_time):
        for rect in self._rects:
            rect.nextevent = current_time + rect.delay;

