from machine import Pin, PWM
import time
import math

# Setup für ESP8266
servo1 = PWM(Pin(5), freq=50)  # D1 = linker Motor (Pin 5)

# Konstante PWM-Werte für Servo1 (aus deinem Referenz-Skript)
SERVO1_STOP = 75             # Stillstand
SERVO1_FULL_FORWARD = 81     # Volle Vorwärtsfahrt

def calc_duty_servo1(speed):
    """
    Konvertiert Speed [0.0–1.0] → PWM Duty für Servo1 (linker Motor)
    """
    if speed <= 0.05:
        return SERVO1_STOP
    return int(SERVO1_STOP + (SERVO1_FULL_FORWARD - SERVO1_STOP) * speed)

print("=== Servo Stufen Test ===")
print("Servo an Pin 5 fährt in Stufen von max bis min")
print("Stoppe mit Ctrl+C")
print("-" * 50)

# Geschwindigkeitsstufen von max bis min
speed_steps = [1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.05, 0.0]
step_duration = 2.0  # Jede Stufe 2 Sekunden lang

try:
    while True:
        for i, speed in enumerate(speed_steps):
            print(f"\nStufe {i+1}/{len(speed_steps)}: Speed {speed:.2f}")
            
            # PWM-Wert berechnen und setzen
            pwm_duty = calc_duty_servo1(speed)
            servo1.duty(pwm_duty)
            
            # Status ausgeben und warten
            print(f"PWM: {pwm_duty} - Warte {step_duration}s...")
            time.sleep(step_duration)
        
        print("\n" + "="*50)
        print("Zyklus beendet - Starte von vorne")
        print("="*50)
        
except KeyboardInterrupt:
    print("\nTest beendet. Servo stoppen...")
    servo1.duty(SERVO1_STOP)
    print("Servo gestoppt.")
