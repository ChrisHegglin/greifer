#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import math

"""
    ____TO DO:____
    
    - def drehen() erstellen
    - Ultraschall initialieseren (port, name etc....)
    - ColorSensor richtig einbinden in def heben() -> (endanschlag arm (weiss))
    - Automatische Ablaufsteuerung: Ablauf entwerfen (Positionswechsel, Sensor etc...)
    
    
"""



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
kontrolle=UltrasonicSensor(Port.S2)
#pos_kralle=ColorSensor(Port.S3)

#Initialisierung__________________________________________________________
def init():
    motor_kralle.run_until_stalled(200, then=Stop.COAST, duty_limit=50)     #Kralle bis zum maximum schliessen
    motor_kralle.reset_angle(0)                                             #Winkel der Kralle auf null stellen
    motor_kralle.run_target(200, -110, then=Stop.HOLD, wait=True)           #Kralle öffnen
    motor_arm.run_until_stalled(-400, then=Stop.COAST, duty_limit=20)       #Arm bis maximum heben
    motor_arm.hold()                                                        #arm halten

    while not endpos_fuss.pressed():                                        #Fuss bis anschlag fahren und nullen
        motor_fuss.run_angle(80,6 , then=Stop.HOLD, wait=True)
    motor_fuss.reset_angle(180)


def kralle_zu():
    #motor_kralle.run_target(200, 0, then=Stop.HOLD, wait=True)
    motor_kralle.run_until_stalled(200, then=Stop.COAST, duty_limit=100)
    motor_kralle.hold()
    
    
  
def kralle_auf():
    motor_kralle.run_target(200, -110, then=Stop.HOLD, wait=True)
    
        
def heben():
    #roboterarm hebt sich [in cm]
    #Armlänge (A) ca 10cm, Hypothenuse (H) ca 14cm, hoehe (G) --> angle =asin(A/H)
    #A=10 #Armlänge 
    #H=14 #hypothenuse zu boden
    #angle_rad=math.acos(A/H)
    #angle_deg=math.degrees(angle_rad)
    
    #hoehe_angleRad= math.asin(hoehe/H)
    # hoehe_angleDeg=(hoehe/H)
    #if  pos_kralle.color() == Color.WHITE:
    # motor_arm.run_angle(200, 90, then=Stop.HOLD, wait=True)
    # Winkelfun ktion dunktioniert nicht korrekt. Habs nicht geschafft es auf diesem Weg zu realisieren
    motor_arm.run_until_stalled(-400, then=Stop.COAST, duty_limit=40)
    motor_arm.hold()

    
def senken():
    #roboterarm senkt
    motor_arm.run_until_stalled(200, then=Stop.COAST, duty_limit=20)
    
def drehen(angle): 
    #arm dreht sich an den angebenen Winkel
    if (angle<=180): 
        motor_fuss.run_target(200, angle, then=Stop.HOLD, wait=True)

  
def reset(): #OBSOLET:.....
    kralle_auf()
    heben()
    while not endpos_fuss.pressed():
        motor_fuss.run_angle(20,4 , then=Stop.HOLD, wait=True)
    motor_fuss.reset_angle(180)
    


 
init()    
while True:   
 
    if Button.CENTER in ev3.buttons.pressed() and Button.UP in ev3.buttons.pressed():  #Ablaufsteuerung
        ev3.screen.clear()
        ev3.screen.draw_text(0,0,"Automat")
        init()
        while not(Button.CENTER in ev3.buttons.pressed() and Button.DOWN in ev3.buttons.pressed()):  # abbruchbedingung
            #Automatischer Ablaufsteuerung
            dist = kontrolle.distance()
            if (70<dist<90):
                
                drehen(180)
                senken()
                kralle_zu()
                heben()
                drehen(60)
                senken()
                kralle_auf()
                heben()
                        
            #pass
        
   
    

#--------------------------------------------------------------------------
    elif Button.CENTER in ev3.buttons.pressed() and Button.DOWN in ev3.buttons.pressed():  #Manuelle Steuerung
        ev3.screen.clear()
        ev3.screen.draw_text(0,0,"Manuell")
        print (dist)   
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
                motor_arm.run(-20)

            elif (Button.DOWN in ev3.buttons.pressed() and not Button.CENTER in ev3.buttons.pressed()):
                ev3.screen.clear()
                ev3.screen.draw_text(0,0,"Arm senken")
                motor_arm.run(20)
                
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

            
                
                
            
                
        
            
        
    



