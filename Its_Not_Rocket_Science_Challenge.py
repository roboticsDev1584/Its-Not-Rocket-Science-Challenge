import decimal

#preparing decimal values
decimal.getcontext().prec = 10

#simulated values
payload = decimal.Decimal(20000)
fuel = decimal.Decimal(500000)
dt = decimal.Decimal(0.001)
time = decimal.Decimal(0.0)
mass = payload + fuel
velocity = decimal.Decimal(0.0)
distance_from_surface = decimal.Decimal(0.0)

#drag force properties
b_max = decimal.Decimal(100)
min_dist_applied = 0
max_dist_applied = decimal.Decimal(200000)

#thrust force properties
uex = decimal.Decimal(3000)
min_flow_rate = 0
max_flow_rate = decimal.Decimal(2000)

#gravitational force properties
gravitational_constant = decimal.Decimal(6.67*(10**-11))
earth_mass = decimal.Decimal(6.00*(10**24))
earth_radius = decimal.Decimal(6.4*(10**6))

#Fd = -bv^2
def drag_force(distance, speed):
    b_value = (1-(distance/max_dist_applied))*b_max
    if (b_value < 0.0):
        b_value = decimal.Decimal(0.0)
    return b_value*((speed*dt)**2)

#Ft = (dm/dt)*uex
def thrust_force(ctime):
    mass_flow_rate = max_flow_rate
    if (ctime < 20.0):
        mass_flow_rate = (ctime/decimal.Decimal(20.0))*max_flow_rate
    return (mass_flow_rate)*uex

#Fg = G(M1)(M2)/R**2
def gravitational_force(mass_rocket, distance):
    return gravitational_constant*mass_rocket*earth_mass/((earth_radius+distance)**2)

#Until liftoff - until the point when thrust_force() = gravitational_force()
while (time < 20.0):
    ft = thrust_force(time)
    fuel -= (ft*dt/uex)
    mass = payload + fuel
    time = time + dt
    if (ft >= gravitational_force(mass,0)):
        break
print("Takeoff time: ",time)

#After takeoff until no fuel remains
while (fuel > 0.0):
    ft = thrust_force(time)
    fuel -= (ft*dt/uex)
    if (fuel < 0.0):
        fuel = decimal.Decimal(0.0)
    mass = payload + fuel

    net_force = decimal.Decimal(ft) - gravitational_force(mass, distance_from_surface) - drag_force(distance_from_surface, velocity)
    velocity += (net_force/mass * dt)
    distance_from_surface += (velocity * dt)
    time = time + dt
print("No fuel time: ",time)
print("No fuel mass: ",mass)
print("No fuel velocity: ",velocity)
print("No fuel distance from the surface: ",distance_from_surface)

#Keep going until 500 seconds later, when thrust force is 0 N
while (time < 500.0):
    net_force = -gravitational_force(mass, distance_from_surface)
    velocity += (net_force/mass * dt)
    distance_from_surface += (velocity * dt)
    time = time + dt
print("500 second velocity: ",velocity)
print("500 second distance from the surface: ",distance_from_surface)