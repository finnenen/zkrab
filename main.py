from machine import ADC, Pin, PWM
import time

# Setup für ESP8266
adc = ADC(0)  # Poti an A0 (gibt Werte von 0–1023)
servo1 = PWM(Pin(5), freq=50)  # D1 = linker Motor
servo2 = PWM(Pin(4), freq=50)  # D2 = rechter Motor

# Konstante PWM-Werte (angepasst für FS90R)
STOP = 76             # 1.5 ms (Stillstand)
FULL_FORWARD = 80    # ca. 2.5 ms (volle Vorwärtsfahrt)

# Mittelwert und Toleranz
CENTER = 512
TOLERANCE = 20

def calc_duty(speed):
    """
    Konvertiert Speed [0.0–1.0] → PWM Duty für Vorwärtsfahrt
    """
    if speed <= 0.05:
        return STOP
    return int(STOP + (FULL_FORWARD - STOP) * speed)

while True:
    pot_val = adc.read()  # Lese Poti-Wert (0–1023)
    offset = pot_val - CENTER

    # Wenn Poti in Mittelposition (±TOLERANCE), beide stoppen
    if abs(offset) <= TOLERANCE:
        left_speed = 0.0
        right_speed = 0.0
    else:
        # Berechne normierte Position außerhalb der Toleranz (0.0 bis 1.0)
        if offset > 0:
            # Poti nach rechts (über CENTER + TOLERANCE)
            max_right = 1023 - CENTER - TOLERANCE  # Maximaler Bereich nach rechts
            norm = min(offset - TOLERANCE, max_right) / max_right
            norm = max(0.0, min(norm, 1.0))  # Sicherstellung 0-1 Bereich
            
            # Servo2 startet mit 0.5 Geschwindigkeit und steigt bis maximal
            # Servo1 startet mit minimaler und nähert sich servo2 an
            right_speed = 0.5 + (0.5 * norm)  # Servo2 von 0.5 bis 1.0
            left_speed = norm                   # Servo1 von 0 bis maximal
        else:
            # Poti nach links (unter CENTER - TOLERANCE)
            max_left = CENTER - TOLERANCE  # Maximaler Bereich nach links
            norm = min(abs(offset) - TOLERANCE, max_left) / max_left
            norm = max(0.0, min(norm, 1.0))  # Sicherstellung 0-1 Bereich
            
            # Servo1 startet mit 0.5 Geschwindigkeit und steigt bis maximal
            # Servo2 startet mit minimaler und nähert sich servo1 an
            left_speed = 0.5 + (0.5 * norm)   # Servo1 von 0.5 bis 1.0
            right_speed = norm                 # Servo2 von 0 bis maximal

    # PWM-Werte setzen
    servo1.duty(calc_duty(left_speed))
    servo2.duty(calc_duty(right_speed))

    # print(calc_duty(left_speed))

    print(f"Poti: {pot_val} -> L: {left_speed:.2f} R: {right_speed:.2f}")
    time.sleep(0.05)