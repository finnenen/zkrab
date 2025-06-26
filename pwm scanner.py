from machine import ADC, Pin, PWM
import time

# Setup für ESP8266
adc = ADC(0)  # Poti an A0 (gibt Werte von 0–1023)
servo_test = PWM(Pin(4), freq=50)  # D2 = GPIO 4 (rechter Motor zum Testen)

# PWM-Scan-Bereich (typisch für Servos: 40-120)
MIN_PWM = 40
MAX_PWM = 120

def map_poti_to_pwm(poti_val):
    """
    Mappt Poti-Wert (0-1023) auf PWM-Bereich (MIN_PWM bis MAX_PWM)
    """
    return int(MIN_PWM + (poti_val / 1023.0) * (MAX_PWM - MIN_PWM))

print("=== Servo PWM Scanner ===")
print(f"PWM-Bereich: {MIN_PWM} bis {MAX_PWM}")
print("Drehe das Poti langsam und beobachte, wann der Servo stoppt!")
print("Format: Poti-Wert -> PWM-Wert")
print("-" * 40)

while True:
    pot_val = adc.read()  # Lese Poti-Wert (0–1023)
    pwm_val = map_poti_to_pwm(pot_val)
    
    # PWM-Wert an Servo senden
    servo_test.duty(pwm_val)
    
    # Status ausgeben
    print(f"Poti: {pot_val:4d} -> PWM: {pwm_val:3d}")
    
    time.sleep(0.1)  # Etwas langsamer für bessere Beobachtung
