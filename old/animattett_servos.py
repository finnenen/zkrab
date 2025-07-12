from machine import ADC, Pin, PWM
import time
import urandom

# Setup für ESP8266
adc = ADC(0)  # Poti an A0 (optional, nicht verwendet)
servo1 = PWM(Pin(5), freq=50)  # D1 = linker Motor
servo2 = PWM(Pin(4), freq=50)  # D2 = rechter Motor

# Konstante PWM-Werte (angepasst für FS90R)
# Servo1 (GPIO 5) - linker Motor
SERVO1_STOP = 76             # 1.5 ms (Stillstand)
SERVO1_FULL_FORWARD = 81     # ca. 2.5 ms (volle Vorwärtsfahrt)

# Servo2 (GPIO 4) - rechter Motor  
SERVO2_STOP = 76             # Angepasst für diesen Servo
SERVO2_FULL_FORWARD = 81     # Entsprechend angepasst

# Animation Parameter
PHASE_DURATION = 3000  # 7 Sekunden pro Phase in ms
TRANSITION_TIME = 3000  # 3 Sekunden Übergang in ms
UPDATE_INTERVAL = 50    # 50ms Update-Intervall

def get_random_speed():
    """
    Erzeugt zufällige Geschwindigkeit zwischen 0.0 und 1.0
    """
    return urandom.getrandbits(16) / 65535.0  # 16-bit zufällig normiert auf 0-1

def get_random_speeds():
    """
    Erzeugt zwei zufällige Geschwindigkeiten, wobei nie beide gleichzeitig stillstehen
    """
    speed1 = get_random_speed()
    speed2 = get_random_speed()
    
    # Wenn beide zu niedrig sind (quasi stillstehen), einen zufällig auf mindestens 0.3 setzen
    if speed1 <= 0.1 and speed2 <= 0.1:
        if urandom.getrandbits(1):  # Zufällig servo1 oder servo2 wählen
            speed1 = 0.3 + get_random_speed() * 0.7  # Mindestens 30% Geschwindigkeit
        else:
            speed2 = 0.3 + get_random_speed() * 0.7
    
    return speed1, speed2

def calc_duty_servo1(speed):
    """
    Konvertiert Speed [0.0–1.0] → PWM Duty für Servo1 (linker Motor)
    """
    if speed <= 0.05:
        return SERVO1_STOP
    return int(SERVO1_STOP + (SERVO1_FULL_FORWARD - SERVO1_STOP) * speed)

def calc_duty_servo2(speed):
    """
    Konvertiert Speed [0.0–1.0] → PWM Duty für Servo2 (rechter Motor)
    """
    if speed <= 0.05:
        return SERVO2_STOP
    return int(SERVO2_STOP + (SERVO2_FULL_FORWARD - SERVO2_STOP) * speed)

def smooth_transition(current_speed, target_speed, progress):
    """
    Sanfte Übergangsberechnung (0.0 bis 1.0)
    progress: 0.0 = Start, 1.0 = Ziel erreicht
    """
    # Einfache lineare Interpolation
    return current_speed + (target_speed - current_speed) * progress

# Animation Variablen
servo1_current_speed = 0.0
servo2_current_speed = 0.0
servo1_target_speed = 0.0
servo2_target_speed = 0.0

last_phase_time = time.ticks_ms()
last_update_time = time.ticks_ms()

# Erste zufällige Zielgeschwindigkeiten
servo1_target_speed, servo2_target_speed = get_random_speeds()  # Nie beide gleichzeitig stillstehend

print("Servo Animation gestartet!")
print(f"Erste Ziele: Servo1={servo1_target_speed:.2f}, Servo2={servo2_target_speed:.2f}")

while True:
    current_time = time.ticks_ms()
    
    # Prüfe ob neue Phase beginnt (alle 7 Sekunden)
    if time.ticks_diff(current_time, last_phase_time) >= PHASE_DURATION:
        # Aktuelle Geschwindigkeiten werden zu neuen Startgeschwindigkeiten
        servo1_current_speed = servo1_target_speed
        servo2_current_speed = servo2_target_speed
        
        # Neue zufällige Zielgeschwindigkeiten (nie beide gleichzeitig stillstehend)
        servo1_target_speed, servo2_target_speed = get_random_speeds()
        
        last_phase_time = current_time
        print(f"Neue Ziele: Servo1={servo1_target_speed:.2f}, Servo2={servo2_target_speed:.2f}")
    
    # Berechne Fortschritt der aktuellen Transition (0.0 bis 1.0)
    phase_progress = time.ticks_diff(current_time, last_phase_time) / PHASE_DURATION
    
    # Für die ersten 3 Sekunden sanft überblenden
    if phase_progress <= (TRANSITION_TIME / PHASE_DURATION):
        # Transition läuft noch
        transition_progress = phase_progress / (TRANSITION_TIME / PHASE_DURATION)
        
        # Berechne aktuelle Geschwindigkeiten mit sanftem Übergang
        servo1_actual_speed = smooth_transition(servo1_current_speed, servo1_target_speed, transition_progress)
        servo2_actual_speed = smooth_transition(servo2_current_speed, servo2_target_speed, transition_progress)
    else:
        # Transition abgeschlossen - Zielgeschwindigkeiten beibehalten
        servo1_actual_speed = servo1_target_speed
        servo2_actual_speed = servo2_target_speed
    
    # PWM-Werte setzen
    servo1.duty(calc_duty_servo1(servo1_actual_speed))
    servo2.duty(calc_duty_servo2(servo2_actual_speed))
    
    # Debug-Ausgabe
    print(f"Servo1: {servo1_actual_speed:.2f} | Servo2: {servo2_actual_speed:.2f}")
    
    time.sleep(UPDATE_INTERVAL / 1000.0)  # 50ms warten