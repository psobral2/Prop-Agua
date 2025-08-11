# README

Versión 1.0.

Realizó: Pablo Sobral, para Termodinámica. 

Fecha: 2025-08-09

Contacto: psobral@fi.uba.ar.

La exactitud de los resultados está supeditada a lo que genera CoolProp. Usar bajo la propia responsabilidad.

p = presión [bar(a)]

t = temperatura [°C]

v = volumen específico [m³/kg]

u = energía interna [kJ/kg]

h = entalpía [kJ/kg]

s = entropía [kJ/kg-K]

x = título [-]

Se deben ingresar valores razonables.

x = -1 significa que el estado no se encuentra ni dentro de la campana ni en su frontera.

CoolProp aún no permite calcular desde los siguientes pares de parámetros: (t,u) (t,h) (u,h) (u,s) (u,x) (h,x) y (s,x).

**Créditos:** Basada en la app del [Ing. Pablo Barral](mailto:pbarral@fi.uba.ar), sin sus comentarios yo no sabría nada de Python, Streamlit, CoolProp.
