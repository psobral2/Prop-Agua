import streamlit as st
import CoolProp.CoolProp as cp
import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI

# Título de la aplicación
st.subheader("Termodinámica - Máquinas Térmicas - Tecnología del Calor")
st.title("💧 Calculador de propiedades del agua")
st.markdown("---")

# Variables disponibles
VARIABLES = ['p', 't', 'v', 'u', 'h', 's', 'x']
FMT = {
    'p': '{:.2f}',
    't': '{:.2f}',
    'v': '{:.4f}',
    'u': '{:.2f}',
    'h': '{:.2f}',
    's': '{:.4f}',
    'x': '{:.4f}',
}

# Inicialización del estado
for var in VARIABLES:
    st.session_state.setdefault(var, '')
st.session_state.setdefault('first_input', None)
st.session_state.setdefault('second_input', None)
st.session_state.setdefault('t_num', None)
st.session_state.setdefault('s_num', None)
st.session_state.setdefault('calculado', False)
st.session_state.setdefault('resultados', None)

# Actualizar los valores calculados antes de instanciar los widgets
if st.session_state.get('resultados'):
    resultados = st.session_state.pop('resultados')
    for var in VARIABLES:
        valor = resultados.get(var)
        st.session_state[var] = FMT[var].format(valor) if valor is not None else ''
    st.session_state['t_num'] = resultados.get('t')
    st.session_state['s_num'] = resultados.get('s')
    st.session_state['calculado'] = True


def manejar_cambio(key):
    """Borra los otros inputs al ingresar el primer valor."""
    valor = st.session_state.get(key, '')
    if st.session_state.get('first_input') is None:
        if valor != '':
            st.session_state['first_input'] = key
            st.session_state['second_input'] = None
            for var in VARIABLES:
                if var != key:
                    st.session_state[var] = ''
            st.session_state['calculado'] = False
            st.session_state['t_num'] = None
            st.session_state['s_num'] = None
    elif st.session_state.get('first_input') != key and st.session_state.get('second_input') is None:
        if valor != '':
            st.session_state['second_input'] = key


def calcular_propiedades(desde, **kwargs):
    """Calcula todas las propiedades del agua a partir de un par de variables."""
    t = p = v = u = h = s = x = None
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

        return t, p, v, u, h, s, x
    except Exception as e:
        st.error(f"Error en el cálculo: {e}")
        st.session_state['calculado'] = False
        return None, None, None, None, None, None, None


# Barra lateral informativa
st.sidebar.write("Desarrollado por P Sobral para **Termodinámica**.")
st.sidebar.write("Versión: 0.01.")
st.sidebar.write("Contacto: psobral@fi.uba.ar.")
st.sidebar.write("Powered by CoolProp.")
st.sidebar.markdown("[Readme.md](https://github.com/psobral2/Prop-Agua/blob/main/README.md)")


st.write("### Ingrese dos propiedades en las casillas correspondientes")

col1, col2, col3 = st.columns(3)
with col1:
    st.text_input("Presión [bar(a)]", key='p', on_change=manejar_cambio, args=('p',))
    st.text_input("Volumen específico [m³/kg]", key='v', on_change=manejar_cambio, args=('v',))
    st.text_input("Entalpía [kJ/kg]", key='h', on_change=manejar_cambio, args=('h',))
with col2:
    st.text_input("Temperatura [°C]", key='t', on_change=manejar_cambio, args=('t',))
    st.text_input("Energía interna [kJ/kg]", key='u', on_change=manejar_cambio, args=('u',))
    st.text_input("Entropía [kJ/(kg·K)]", key='s', on_change=manejar_cambio, args=('s',))
with col3:
    st.text_input("Título [0-1]", key='x', on_change=manejar_cambio, args=('x',))


if st.button("Calcular"):
    valores = {k: st.session_state[k] for k in VARIABLES if st.session_state[k] not in ('', None)}
    if len(valores) != 2:
        st.error("Por favor, ingrese exactamente dos valores.")
    else:
        pair_map = {
            frozenset({'t', 'p'}): 'TP',
            frozenset({'p', 'h'}): 'PH',
            frozenset({'h', 's'}): 'HS',
            frozenset({'p', 'x'}): 'PX',
            frozenset({'t', 'x'}): 'TX',
            frozenset({'p', 's'}): 'PS',
            frozenset({'t', 's'}): 'TS',
            frozenset({'p', 'v'}): 'PV',
            frozenset({'t', 'v'}): 'TV',
        }
        clave = pair_map.get(frozenset(valores.keys()))
        if clave is None:
            st.error("Combinación de propiedades no soportada.")
        else:
            try:
                parsed = {k: float(v) for k, v in valores.items()}
            except ValueError:
                st.error("Los valores deben ser numéricos.")
            else:
                t, p, v, u, h, s, x = calcular_propiedades(clave, **parsed)
                if t is not None:
                    st.session_state['resultados'] = {
                        'p': p,
                        't': t,
                        'v': v,
                        'u': u,
                        'h': h,
                        's': s,
                        'x': x,
                    }
                    st.session_state['first_input'] = None
                    st.session_state['second_input'] = None
                    try:
                        st.rerun()
                    except AttributeError:
                        st.experimental_rerun()


if st.session_state.get('calculado', False):
    t_session = st.session_state.get('t_num')
    s_session = st.session_state.get('s_num')
    if t_session is not None and s_session is not None:
        Tsat = np.linspace(273.15, 647.095, 500)
        s_liq = [PropsSI("S", "T", T, "Q", 0, "Water") / 1000 for T in Tsat]
        s_vap = [PropsSI("S", "T", T, "Q", 1, "Water") / 1000 for T in Tsat]
        T_C = Tsat - 273.15

        s_user = s_session
        T_user = t_session

        fig, ax = plt.subplots()
        ax.plot(s_liq, T_C, label="Líquido saturado", color="blue")
        ax.plot(s_vap, T_C, label="Vapor saturado", color="red")
        ax.plot(s_user, T_user, "ko", label="Punto ingresado")

        ax.set_xlabel("Entropía específica [kJ/kg·K]")
        ax.set_ylabel("Temperatura [°C]")
        ax.set_title("Diagrama T–s del agua")
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)

