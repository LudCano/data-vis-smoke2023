
def pressure_to_altitude(pressure):
    h = (1-((pressure/1013.25)**0.190284))*145366.45*0.3048
    return h

def alt_to_press(altitude):
    p = (((1- altitude/(145366.45*0.3048)))**(1/0.190284))*1013.25
    return p


a = pressure_to_altitude(800)
b = alt_to_press(a)
print(b)