    """
    ____TO DO:____
    
    - def heben(), def senken() und def drehen() erstellen
    - Ultraschall initialieseren (port, name etc....)
    - ColorSensor richtig einbinden in def heben() -> (endanschlag arm (weiss))
    - Automatische Ablaufsteuerung: Ablauf entwerfen (Positionswechsel, Sensor etc...)
    
    
    """

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

#Aktoren_________________________________________________________________
#class Motor(port, positive_direction=Direction.CLOCKWISE, gears=None)
#getriebe -> Zahnräder an der Konstruktion
motor_kralle=Motor(Port.A,Direction.CLOCKWISE)
motor_arm=Motor(Port.B,Direction.CLOCKWISE,[8,40])
motor_fuss=Motor(Port.C,Direction.CLOCKWISE,[12,40])

#Sensoren_________________________________________________________________
#class TouchSensor(port)
endpos_fuss=TouchSensor(Port.S1)
pos_kralle=ColorSensor(Port.S3)

# Write your program here.

def kralle_zu():
    #Kralle soll zubeissen bis der Motor abwürgt
    motor_kralle.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    
  
def kralle_auf():
    #Kralle soll objekt loslassen
    motor_kralle.run_target(200, -10)
    
        
def heben(hoehe):
    #roboterarm hebt sich
    pass
    
def senken():
    #roboterarm senkt sich
    motor_arm.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    
def drehen(direction,angle):
    #arm dreht sich
    if not endpos_fuss:
        pass
    
    
while True:   
    if Button.CENTER in ev3.buttons.pressed() and Button.UP in ev3.buttons.pressed():  #Ablaufsteuerung
        ev3.screen.clear()
        ev3.screen.draw_text(0,0,"Automat")
        while not(Button.CENTER in ev3.buttons.pressed() and Button.DOWN in ev3.buttons.pressed()):  # abbruchbedingung
            #Automatischer Ablaufsteuerung
            pass
        
   
    
#MS 23.8.22: Keine Endpositionen relaisiert. Manuelle Steuerung soweit i.O.
#--------------------------------------------------------------------------
    elif Button.CENTER in ev3.buttons.pressed() and Button.DOWN in ev3.buttons.pressed():  #Manuelle Steuerung
        ev3.screen.clear()
        ev3.screen.draw_text(0,0,"Manuell")
        while not(Button.CENTER in ev3.buttons.pressed() and Button.UP in ev3.buttons.pressed()):     #abbruchbedingung
         #Manuelle Steuerungsablauf
            if (Button.LEFT in ev3.buttons.pressed() and not Button.CENTER in ev3.buttons.pressed()) :
                ev3.screen.clear()
                ev3.screen.draw_text(0,0,"Kralle zu")
                kralle_zu()
           
            elif (Button.RIGHT in ev3.buttons.pressed() and not Button.CENTER in ev3.buttons.pressed()):
                ev3.screen.clear()
                ev3.screen.draw_text(0,0,"Kralle auf")
                kralle_auf()
                
            elif (Button.UP in ev3.buttons.pressed() and not Button.CENTER in ev3.buttons.pressed()):
                ev3.screen.clear()
                ev3.screen.draw_text(0,0,"Arm heben")
                motor_arm.run(-10)

            elif (Button.DOWN in ev3.buttons.pressed() and not Button.CENTER in ev3.buttons.pressed()):
                ev3.screen.clear()
                ev3.screen.draw_text(0,0,"Arm senken")
                motor_arm.run(10)
                
            elif (Button.RIGHT in ev3.buttons.pressed() and Button.CENTER in ev3.buttons.pressed()):
                ev3.screen.clear()
                ev3.screen.draw_text(0,0,"rechts drehen")
                motor_fuss.run(20) #(positiver Wert, winkel)
            
            elif (Button.LEFT in ev3.buttons.pressed() and Button.CENTER in ev3.buttons.pressed()):
                ev3.screen.clear()
                ev3.screen.draw_text(0,0,"links drehen")
                motor_fuss.run(-20) #(negativer Wert, winkel)    
                
            else:
                motor_kralle.brake()
                motor_arm.brake()
                motor_fuss.brake()

            
                
                
            
                
        
            
        
    



