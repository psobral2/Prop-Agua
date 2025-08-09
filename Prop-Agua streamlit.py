import streamlit as st
import CoolProp.CoolProp as cp

# Inicializar claves en session_state
if 't' not in st.session_state:
    st.session_state['t'] = None
if 's' not in st.session_state:
    st.session_state['s'] = None

# Título de la aplicación
st.subheader("Termodinámica - Máquinas Térmicas - Tecnología del Calor")
st.title("💧 Calculador de propiedades del agua")
# Separador
st.markdown("---")

# Definir funciones para cálculos específicos
def calcular_propiedades(desde, **kwargs):
    t = None
    p = None
    v = None
    u = None
    h = None
    s = None
    x = None
    
    try:
        if desde == 'TP':
            t_kelvin = kwargs['t'] + 273.15
            p_pascal = kwargs['p'] * 1e5
            t = kwargs['t']
            p = kwargs['p']
            rho = cp.PropsSI('D', 'P', p_pascal, 'T', t_kelvin, "Water")
            v = 1 / rho if rho != 0 else float("inf")
            u = cp.PropsSI('U', 'P', p_pascal, 'T', t_kelvin, 'Water') / 1000
            h = cp.PropsSI('H', 'P', p_pascal, 'T', t_kelvin, 'Water') / 1000
            s = cp.PropsSI('S', 'P', p_pascal, 'T', t_kelvin, 'Water') / 1000
            x = cp.PropsSI('Q', 'P', p_pascal, 'T', t_kelvin, 'Water')
        elif desde == 'PH':
            h_joules = kwargs['h'] * 1000
            p_pascal = kwargs['p'] * 1e5
            h = kwargs['h']
            p = kwargs['p']
            t_kelvin = cp.PropsSI('T', 'P', p_pascal, 'H', h_joules, 'Water')
            rho = cp.PropsSI('D', 'P', p_pascal, 'H', h_joules, "Water")
            v = 1 / rho if rho != 0 else float("inf")
            u = cp.PropsSI('U', 'P', p_pascal, 'H', h_joules, 'Water') / 1000
            s = cp.PropsSI('S', 'P', p_pascal, 'H', h_joules, 'Water') / 1000
            x = cp.PropsSI('Q', 'P', p_pascal, 'H', h_joules, 'Water')
            t = t_kelvin - 273.15
        elif desde == 'HS':
            h_joules = kwargs['h'] * 1000
            s_joules = kwargs['s'] * 1000
            h = kwargs['h']
            s = kwargs['s']
            t_kelvin = cp.PropsSI('T', 'H', h_joules, 'S', s_joules, 'Water')
            p_pascal = cp.PropsSI('P', 'H', h_joules, 'S', s_joules, 'Water')
            rho = cp.PropsSI('D', 'H', h_joules, 'S', s_joules, "Water")
            v = 1 / rho if rho != 0 else float("inf")
            u = cp.PropsSI('U', 'H', h_joules, 'S', s_joules, 'Water') / 1000
            x = cp.PropsSI('Q', 'H', h_joules, 'S', s_joules, 'Water')
            t = t_kelvin - 273.15
            p = p_pascal / 1e5
        elif desde == 'PX':
            p_pascal = kwargs['p'] * 1e5
            x = kwargs['x']
            p = kwargs['p']
            t_kelvin = cp.PropsSI('T', 'P', p_pascal, 'Q', x, 'Water')
            rho = cp.PropsSI('D', 'P', p_pascal, 'Q', x, "Water")
            v = 1 / rho if rho != 0 else float("inf")
            u = cp.PropsSI('U', 'P', p_pascal, 'Q', x, 'Water') / 1000
            h = cp.PropsSI('H', 'P', p_pascal, 'Q', x, 'Water') / 1000
            s = cp.PropsSI('S', 'P', p_pascal, 'Q', x, 'Water') / 1000
            t = t_kelvin - 273.15
        elif desde == 'TX':
            t_kelvin = kwargs['t'] + 273.15
            x = kwargs['x']
            t = kwargs['t']
            p_pascal = cp.PropsSI('P', 'T', t_kelvin, 'Q', x, 'Water')
            rho = cp.PropsSI('D', 'T', t_kelvin, 'Q', x, "Water")
            v = 1 / rho if rho != 0 else float("inf")
            u = cp.PropsSI('U', 'T', t_kelvin, 'Q', x, 'Water') / 1000
            h = cp.PropsSI('H', 'T', t_kelvin, 'Q', x, 'Water') / 1000
            s = cp.PropsSI('S', 'T', t_kelvin, 'Q', x, 'Water') / 1000
            p = p_pascal / 1e5
        elif desde == 'PS':
            p_pascal = kwargs['p'] * 1e5
            s_joules = kwargs['s'] * 1000
            p = kwargs['p']
            s = kwargs['s']
            t_kelvin = cp.PropsSI('T', 'P', p_pascal, 'S', s_joules, 'Water')
            rho = cp.PropsSI('D', 'P', p_pascal, 'S', s_joules, "Water")
            v = 1 / rho if rho != 0 else float("inf")
            u = cp.PropsSI('U', 'P', p_pascal, 'S', s_joules, 'Water') / 1000
            h = cp.PropsSI('H', 'P', p_pascal, 'S', s_joules, 'Water') / 1000
            x = cp.PropsSI('Q', 'P', p_pascal, 'S', s_joules, 'Water')
            t = t_kelvin - 273.15
        elif desde == 'TS':
            t_kelvin = kwargs['t'] + 273.15
            s_joules = kwargs['s'] * 1000
            t = kwargs['t']
            s = kwargs['s']
            p_pascal = cp.PropsSI('P', 'T', t_kelvin, 'S', s_joules, 'Water')
            rho = cp.PropsSI('D', 'T', t_kelvin, 'S', s_joules, "Water")
            v = 1 / rho if rho != 0 else float("inf")
            u = cp.PropsSI('U', 'T', t_kelvin, 'S', s_joules, 'Water') / 1000
            h = cp.PropsSI('H', 'T', t_kelvin, 'S', s_joules, 'Water') / 1000
            x = cp.PropsSI('Q', 'T', t_kelvin, 'S', s_joules, 'Water')
            p = p_pascal / 1e5
        elif desde == 'PV':
            p_pascal = kwargs['p'] * 1e5
            rho = 1 / kwargs['v'] if kwargs['v'] != 0 else float("inf")
            p = kwargs['p']
            v = kwargs['v']
            t_kelvin = cp.PropsSI('T', 'P', p_pascal, 'D', rho, 'Water')
            u = cp.PropsSI('U', 'P', p_pascal, 'D', rho, 'Water') / 1000
            h = cp.PropsSI('H', 'P', p_pascal, 'D', rho, 'Water') / 1000
            s = cp.PropsSI('S', 'P', p_pascal, 'D', rho, 'Water') / 1000
            x = cp.PropsSI('Q', 'P', p_pascal, 'D', rho, 'Water')
            t = t_kelvin - 273.15
        elif desde == 'TV':
            t_kelvin = kwargs['t'] + 273.15
            rho = 1 / kwargs['v'] if kwargs['v'] != 0 else float("inf")
            t = kwargs['t']
            v = kwargs['v']
            p_pascal = cp.PropsSI('P', 'T', t_kelvin, 'D', rho, 'Water')
            u = cp.PropsSI('U', 'T', t_kelvin, 'D', rho, 'Water') / 1000
            h = cp.PropsSI('H', 'T', t_kelvin, 'D', rho, 'Water') / 1000
            s = cp.PropsSI('S', 'T', t_kelvin, 'D', rho, 'Water') / 1000
            x = cp.PropsSI('Q', 'T', t_kelvin, 'D', rho, 'Water')
            p = p_pascal / 1e5

        # Devolver todas las propiedades calculadas
        st.session_state['t'] = t
        st.session_state['s'] = s
        st.session_state['calculado'] = True
        return t, p, v, u, h, s, x


    except Exception as e:
        st.error(f"Error en el cálculo: {e}")
        st.session_state['t'] = None
        st.session_state['s'] = None
        st.session_state['calculado'] = False
        return None, None, None, None, None, None, None



# Formulario para seleccionar la opción
def reset_calculado():
    st.session_state['calculado'] = False

st.sidebar.title("Seleccioná una opción:")
option = st.sidebar.radio(
    "",
    ("t y p",
     "p y h",
     "h y s",
     "p y x",
     "t y x",
     "p y s",
     "t y s",
     "p y v",
     "t y v"),
    on_change=reset_calculado,
)

# Texto adicional
st.sidebar.write("Desarrollado por P Sobral para **Termodinámica**.")
st.sidebar.write("Versión: 0.01.")
st.sidebar.write("Contacto: psobral@fi.uba.ar.")
st.sidebar.write("Powered by CoolProp.")
st.sidebar.markdown("[Readme.md](https://github.com/psobral2/Prop-Agua/blob/main/README.md)")


if option == 't y p':

    # Formulario para Temperatura y Presión
    st.write("### Temperatura y Presión")

    with st.form(key='tp_form'):
        t = st.number_input("Ingrese la temperatura [°C]", value=0.0, step=0.01, format="%.2f", min_value=0.0)
        p_t = st.number_input("Ingrese la presión [bar(a)]", value=1.0, step=0.01, format="%.2f", min_value=0.0)

        tp_submit_button = st.form_submit_button(label='Calcular desde Temperatura y Presión')

    if tp_submit_button:
        t, p, v, u, h, s, x = calcular_propiedades('TP', t=t, p=p_t)

        if t is not None:
            st.write(f"Resultados a {t:.2f} °C y {p:.2f} bar(a):")
            st.write(f"Volumen específico: {v:.4f} m³/kg")
            st.write(f"Energía interna: {u:.2f} kJ/kg")
            st.write(f"Entalpía: {h:.2f} kJ/kg")
            st.write(f"Entropía: {s:.4f} kJ/(kg·K)")
            st.write(f"Título: {x:.4f}")
        else:
            st.write(f"Revisá que sean coherentes los valores ingresados, y volvé a intentarlo.")


elif option == 'p y h':


    # Formulario para Presión y Entalpía
    st.write("### Presión y Entalpía")
    with st.form(key='ph_form'):
        h = st.number_input("Ingrese la entalpía [kJ/kg]", value=0.0, step=0.01, format="%.2f", min_value=0.0)
        p_h = st.number_input("Ingrese la presión [bar(a)]", value=1.0, step=0.01, format="%.2f", min_value=0.0)
        ph_submit_button = st.form_submit_button(label='Calcular desde Presión y Entalpía')

    if ph_submit_button:
        t, p, v, u, h, s, x = calcular_propiedades('PH', h=h, p=p_h)
        if t is not None:
            st.write(f"Resultados a {h:.2f} kJ/kg y {p:.2f} bar(a):")
            st.write(f"Temperatura: {t:.2f} °C")
            st.write(f"Volumen específico: {v:.4f} m³/kg")
            st.write(f"Energía interna: {u:.2f} kJ/kg")
            st.write(f"Entropía: {s:.4f} kJ/(kg·K)")
            st.write(f"Título: {x:.4f}")
        else:
            st.write(f"Revisá que sean coherentes los valores ingresados, y volvé a intentarlo.")


elif option == 'h y s':

    # Formulario para Entalpía y Entropía
    st.write("### Entalpía y Entropía")
    with st.form(key='hs_form'):
        h = st.number_input("Ingrese la entalpía [kJ/kg]", value=0.0, step=0.01, format="%.2f", min_value=0.0)
        s = st.number_input("Ingrese la entropía [kJ/(kg·K)]", value=0.0, step=0.01, format="%.4f", min_value=0.0)
        hs_submit_button = st.form_submit_button(label='Calcular desde Entalpía y Entropía')

    if hs_submit_button:
        t, p, v, u, h, s, x = calcular_propiedades('HS', h=h, s=s)
        if t is not None:
            st.write(f"Resultados a {h:.2f} kJ/kg y {s:.4f} kJ/(kg·K):")
            st.write(f"Temperatura: {t:.2f} °C")
            st.write(f"Presión: {p:.2f} bar(a)")
            st.write(f"Volumen específico: {v:.4f} m³/kg")
            st.write(f"Energía interna: {u:.2f} kJ/kg")
            st.write(f"Título: {x:.4f}")
        else:
            st.write(f"Revisá que sean coherentes los valores ingresados, y volvé a intentarlo.")

elif option == 'p y x':

    # Formulario para Presión y Título
    st.write("### Presión y Título")
    with st.form(key='px_form'):
        p = st.number_input("Ingrese la presión [bar(a)]", value=1.0, step=0.01, format="%.2f", min_value=0.0)
        x = st.number_input("Ingrese el título (calidad del vapor) [0-1]", value=0.0, step=0.01, format="%.2f", min_value=0.0, max_value=1.0)
        px_submit_button = st.form_submit_button(label='Calcular desde Presión y Título')

    if px_submit_button:
        t, p, v, u, h, s, x = calcular_propiedades('PX', p=p, x=x)
        if t is not None:
            st.write(f"Resultados a {p:.2f} bar(a) y {x:.4f}:")
            st.write(f"Temperatura: {t:.2f} °C")
            st.write(f"Volumen específico: {v:.4f} m³/kg")
            st.write(f"Energía interna: {u:.2f} kJ/kg")
            st.write(f"Entalpía: {h:.2f} kJ/kg")
            st.write(f"Entropía: {s:.4f} kJ/(kg·K)")
        else:
            st.write(f"Revisá que sean coherentes los valores ingresados, y volvé a intentarlo.")


elif option == 't y x':

    # Formulario para Temperatura y Título
    st.write("### Temperatura y Título")
    with st.form(key='tx_form'):
        t = st.number_input("Ingrese la temperatura [°C]", value=0.0, step=0.01, format="%.2f", min_value=0.0)
        x = st.number_input("Ingrese el título (calidad del vapor) [0-1]", value=0.0, step=0.01, format="%.2f", min_value=0.0, max_value=1.0)
        tx_submit_button = st.form_submit_button(label='Calcular desde Temperatura y Título')

    if tx_submit_button:
        t, p, v, u, h, s, x = calcular_propiedades('TX', t=t, x=x)
        if t is not None:
            st.write(f"Resultados a {t:.2f} °C y {x:.4f}:")
            st.write(f"Presión: {p:.2f} bar(a)")
            st.write(f"Volumen específico: {v:.4f} m³/kg")
            st.write(f"Energía interna: {u:.2f} kJ/kg")
            st.write(f"Entalpía: {h:.2f} kJ/kg")
            st.write(f"Entropía: {s:.4f} kJ/(kg·K)")
        else:
            st.write(f"Revisá que sean coherentes los valores ingresados, y volvé a intentarlo.")


elif option == 'p y v':

    # Formulario para Presión y Volumen específico
    st.write("### Presión y Volumen específico")
    with st.form(key='pv_form'):
        p = st.number_input("Ingrese la presión [bar(a)]", value=1.0, step=0.01, format="%.2f", min_value=0.0)
        v_input = st.number_input("Ingrese el volumen específico [m³/kg]", value=0.001, step=0.0001, format="%.4f", min_value=0.0)
        pv_submit_button = st.form_submit_button(label='Calcular desde Presión y Volumen específico')

    if pv_submit_button:
        t, p, v, u, h, s, x = calcular_propiedades('PV', p=p, v=v_input)
        if t is not None:
            st.write(f"Resultados a {p:.2f} bar(a) y {v:.4f} m³/kg:")
            st.write(f"Temperatura: {t:.2f} °C")
            st.write(f"Energía interna: {u:.2f} kJ/kg")
            st.write(f"Entalpía: {h:.2f} kJ/kg")
            st.write(f"Entropía: {s:.4f} kJ/(kg·K)")
            st.write(f"Título: {x:.4f}")
        else:
            st.write(f"Revisá que sean coherentes los valores ingresados, y volvé a intentarlo.")

elif option == 't y v':

    # Formulario para Temperatura y Volumen específico
    st.write("### Temperatura y Volumen específico")
    with st.form(key='tv_form'):
        t = st.number_input("Ingrese la temperatura [°C]", value=0.0, step=0.01, format="%.2f", min_value=0.0)
        v_input = st.number_input("Ingrese el volumen específico [m³/kg]", value=0.001, step=0.0001, format="%.4f", min_value=0.0)
        tv_submit_button = st.form_submit_button(label='Calcular desde Temperatura y Volumen específico')

    if tv_submit_button:
        t, p, v, u, h, s, x = calcular_propiedades('TV', t=t, v=v_input)
        if t is not None:
            st.write(f"Resultados a {t:.2f} °C y {v:.4f} m³/kg:")
            st.write(f"Presión: {p:.2f} bar(a)")
            st.write(f"Energía interna: {u:.2f} kJ/kg")
            st.write(f"Entalpía: {h:.2f} kJ/kg")
            st.write(f"Entropía: {s:.4f} kJ/(kg·K)")
            st.write(f"Título: {x:.4f}")
        else:
            st.write(f"Revisá que sean coherentes los valores ingresados, y volvé a intentarlo.")

elif option == 'p y s':

    # Formulario para Presión y Entropía
    st.write("### Presión y Entropía")
    with st.form(key='ps_form'):
        p = st.number_input("Ingrese la presión [bar(a)]", value=1.0, step=0.01, format="%.2f", min_value=0.0)
        s = st.number_input("Ingrese la entropía [kJ/(kg·K)]", value=0.0, step=0.01, format="%.4f", min_value=0.0)
        ps_submit_button = st.form_submit_button(label='Calcular desde Presión y Entropía')

    if ps_submit_button:
        t, p, v, u, h, s, x = calcular_propiedades('PS', p=p, s=s)
        if t is not None:
            st.write(f"Resultados a {p:.2f} bar(a) y {s:.4f} kJ/(kg·K):")
            st.write(f"Temperatura: {t:.2f} °C")
            st.write(f"Volumen específico: {v:.4f} m³/kg")
            st.write(f"Energía interna: {u:.2f} kJ/kg")
            st.write(f"Entalpía: {h:.2f} kJ/kg")
            st.write(f"Título: {x:.4f}")
        else:
            st.write(f"Revisá que sean coherentes los valores ingresados, y volvé a intentarlo.")

elif option == 't y s':

    # Formulario para Temperatura y Entropía
    st.write("### Temperatura y Entropía")
    with st.form(key='ts_form'):
        t = st.number_input("Ingrese la temperatura [°C]", value=0.0, step=0.01, format="%.2f", min_value=0.0)
        s = st.number_input("Ingrese la entropía [kJ/(kg·K)]", value=0.0, step=0.01, format="%.4f", min_value=0.0)
        ts_submit_button = st.form_submit_button(label='Calcular desde Temperatura y Entropía')

    if ts_submit_button:
        t, p, v, u, h, s, x = calcular_propiedades('TS', t=t, s=s)
        if t is not None:
            st.write(f"Resultados a {t:.2f} °C y {s:.4f} kJ/(kg·K):")
            st.write(f"Presión: {p:.2f} bar(a)")
            st.write(f"Volumen específico: {v:.4f} m³/kg")
            st.write(f"Energía interna: {u:.2f} kJ/kg")
            st.write(f"Entalpía: {h:.2f} kJ/kg")
            st.write(f"Título: {x:.4f}")
        else:
            st.write(f"Revisá que sean coherentes los valores ingresados, y volvé a intentarlo.")

import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI

if st.session_state.get('calculado', False):
    t_session = st.session_state.get('t')
    s_session = st.session_state.get('s')
    if t_session is not None and s_session is not None:
        # Crear curva de saturación para agua
        Tsat = np.linspace(273.15, 647.095, 500)  # Desde 0°C a punto crítico
        s_liq = [PropsSI("S", "T", T, "Q", 0, "Water") / 1000 for T in Tsat]  # kJ/kg.K
        s_vap = [PropsSI("S", "T", T, "Q", 1, "Water") / 1000 for T in Tsat]  # kJ/kg.K
        T_C = Tsat - 273.15  # Convertir a °C para mostrar

        # Punto del usuario
        s_user = s_session  # kJ/kg.K
        T_user = t_session  # °C

        # Graficar
        fig, ax = plt.subplots()
        ax.plot(s_liq, T_C, label="Líquido saturado", color="blue")
        ax.plot(s_vap, T_C, label="Vapor saturado", color="red")
        ax.plot(s_user, T_user, "ko", label="Punto ingresado")  # Punto del usuario

        ax.set_xlabel("Entropía específica [kJ/kg·K]")
        ax.set_ylabel("Temperatura [°C]")
        ax.set_title("Diagrama T–s del agua")
        ax.grid(True)
        ax.legend()

        # Mostrar en Streamlit
        st.pyplot(fig)

# Separador
#st.markdown("---")
# Texto adicional
#st.write("Desarrollado por P. Sobral para **Termodinámica**. Versión: 0.01. Contacto: psobral@fi.uba.ar. Powered by CoolProp. Ver [Readme.md](https://github.com/psobral2/Prop-Agua/blob/main/README.md) en Github.")
