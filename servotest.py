import time
from machine import Pin, PWM

# Servo an GPIO 5 initialisieren
servo = PWM(Pin(5), freq=50)

# PWM-Werte für kontinuierlichen Servo (FS90R)
SERVO_STOP = 76          # 1.5 ms (Stillstand)
SERVO_MAX_FORWARD = 81   # ca. 2.5 ms (maximale Vorwärtsfahrt)

def set_servo_speed(speed):
    """
    Setzt die Servo-Geschwindigkeit
    speed: 0.0 = Stillstand, 1.0 = maximale Geschwindigkeit
    """
    if speed <= 0.05:
        duty = SERVO_STOP
    else:
        duty = int(SERVO_STOP + (SERVO_MAX_FORWARD - SERVO_STOP) * speed)
    
    servo.duty(duty)
    print(f"Geschwindigkeit: {speed:.2f} | PWM Duty: {duty}")

print("Servo-Test gestartet...")
print("Zyklus: Stillstand → Max Speed → Stillstand (alle 6 Sekunden)")

try:
    while True:
        # Phase 1: Stillstand (6 Sekunden)
        print("\n--- Stillstand ---")
        set_servo_speed(0.0)
        time.sleep(6)
        
        # Phase 2: Maximale Geschwindigkeit (6 Sekunden)
        print("\n--- Maximale Geschwindigkeit ---")
        set_servo_speed(1.0)
        time.sleep(6)
        
except KeyboardInterrupt:
    print("\nTest beendet - Servo gestoppt")
    set_servo_speed(0.0)
