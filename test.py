keyboard_pin = {
    "C4" : 23,
    "D4" : 24,
    "E4" : 30,
}

LED_pin = {
    "LED_C4" : 16,
    "LED_D4" : 26,
    "LED_E4" : 30,
}

index2pin = {
    0 : LED_pin["LED_C4"], 
    2 : LED_pin["LED_D4"], 
    4 : LED_pin["LED_E4"], 
}

print(index2pin[0])