import streamlit as st
import CoolProp.CoolProp as cp
import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI
from itertools import combinations

# Título de la aplicación
st.set_page_config(page_title="Propiedades de los Fluidos", page_icon="🌡️", layout="wide")
st.caption("###### Termodinámica – Máquinas Térmicas – Tecnología del Calor")

# Selección de fluido
FLUID_MAP = {
    'Agua': 'Water',
    'R134a': 'R134a',
    'R22': 'R22',
    'R404A': 'R404A',
    'Amoníaco': 'Ammonia',
}
st.session_state.setdefault('fluid', 'Water')

# Determinar el nombre del fluido
fluid_name = next(k for k, v in FLUID_MAP.items() if v == st.session_state['fluid'])

# Elegir el ícono
icon = "💧" if fluid_name == "Agua" else "❄️"

# Mostrar el título
st.markdown(f"### **{icon} Propiedades del {fluid_name}**")

st.selectbox(
    "Sustancia",
    list(FLUID_MAP.values()),
    key='fluid',
    format_func=lambda v: next(k for k, val in FLUID_MAP.items() if val == v),
)
st.divider()

# Variables disponibles
VARIABLES = ['p', 't', 'v', 'u', 'h', 's', 'x']

# Inicialización del estado
for var in VARIABLES:
    st.session_state.setdefault(var, None)
st.session_state.setdefault('first_input', None)
st.session_state.setdefault('second_input', None)
st.session_state.setdefault('input_order', [])
st.session_state.setdefault('t_num', None)
st.session_state.setdefault('s_num', None)
st.session_state.setdefault('calculado', False)
st.session_state.setdefault('resultados', None)

# Actualizar los valores calculados antes de instanciar los widgets
if st.session_state.get('resultados'):
    resultados = st.session_state.pop('resultados')
    for var in VARIABLES:
        valor = resultados.get(var)
        st.session_state[var] = valor if valor is not None else None
    st.session_state['t_num'] = resultados.get('t')
    st.session_state['s_num'] = resultados.get('s')
    st.session_state['calculado'] = True


def manejar_cambio(key):
    """Mantiene sólo los dos últimos inputs editados."""
    valor = st.session_state.get(key)
    input_order = st.session_state.get('input_order', [])
    if key in input_order:
        input_order.remove(key)
    if valor is not None:
        input_order.append(key)
    if len(input_order) > 2:
        input_order = input_order[-2:]
    st.session_state['input_order'] = input_order
    for var in VARIABLES:
        if var not in input_order:
            st.session_state[var] = None
    st.session_state['first_input'] = input_order[0] if len(input_order) > 0 else None
    st.session_state['second_input'] = input_order[1] if len(input_order) > 1 else None
    st.session_state['calculado'] = False
    st.session_state['t_num'] = None
    st.session_state['s_num'] = None


def limpiar_campos():
    for var in VARIABLES:
        st.session_state[var] = None
    st.session_state['input_order'] = []
    st.session_state['first_input'] = None
    st.session_state['second_input'] = None
    st.session_state['t_num'] = None
    st.session_state['s_num'] = None
    st.session_state['calculado'] = False
    st.session_state['resultados'] = None


def calcular_propiedades(var1, var2, fluid, **kwargs):
    """Calcula todas las propiedades del fluido seleccionado a partir de cualquier par de variables."""
    input_map = {
        'p': ('P', lambda v: v * 1e5),
        't': ('T', lambda v: v + 273.15),
        'v': ('D', lambda v: 1 / v if v != 0 else float("inf")),
        'u': ('U', lambda v: v * 1000),
        'h': ('H', lambda v: v * 1000),
        's': ('S', lambda v: v * 1000),
        'x': ('Q', lambda v: v),
    }
    try:
        name1, val1 = input_map[var1][0], input_map[var1][1](kwargs[var1])
        name2, val2 = input_map[var2][0], input_map[var2][1](kwargs[var2])

        t_kelvin = cp.PropsSI('T', name1, val1, name2, val2, fluid)
        p_pascal = cp.PropsSI('P', name1, val1, name2, val2, fluid)
        rho = cp.PropsSI('D', name1, val1, name2, val2, fluid)
        u_joules = cp.PropsSI('U', name1, val1, name2, val2, fluid)
        h_joules = cp.PropsSI('H', name1, val1, name2, val2, fluid)
        s_joules = cp.PropsSI('S', name1, val1, name2, val2, fluid)
        x = cp.PropsSI('Q', name1, val1, name2, val2, fluid)

        t = t_kelvin - 273.15
        p = p_pascal / 1e5
        v = 1 / rho if rho != 0 else float("inf")
        u = u_joules / 1000
        h = h_joules / 1000
        s = s_joules / 1000

        return t, p, v, u, h, s, x
    except Exception as e:
        st.error(f"Error en el cálculo: {e}")
        st.session_state['calculado'] = False
        return None, None, None, None, None, None, None


# Barra lateral informativa
st.sidebar.write("Desarrollado por **P. Sobral** para **Termodinámica**.")
st.sidebar.write("Versión: 1.0.")
st.sidebar.write("Contacto: psobral@fi.uba.ar.")
st.sidebar.write("Powered by CoolProp.")
st.sidebar.markdown("[Readme.md](https://github.com/psobral2/Prop-Agua/blob/main/README.md)")
st.sidebar.markdown("---")
st.sidebar.markdown("**Créditos:** Basada en la app de [Pablo Barral](https://github.com/PabloMBarral)")

st.caption("###### Ingrese solo dos propiedades")

col1, col2 = st.columns(2, gap=None)
with col1:
    st.number_input(
        "Presión [bar(a)]",
        key='p',
        on_change=manejar_cambio,
        args=('p',),
        format="%.2f",
        step=0.01,
    )
    st.number_input(
        "Temperatura [°C]",
        key='t',
        on_change=manejar_cambio,
        args=('t',),
        format="%.2f",
        step=0.01,
    )
    st.number_input(
        "Volumen específico [m³/kg]",
        key='v',
        on_change=manejar_cambio,
        args=('v',),
        format="%.4f",
        step=0.0001,
    )
    st.number_input(
        "Título [0-1]",
        key='x',
        on_change=manejar_cambio,
        args=('x',),
        format="%.4f",
        step=0.0001,
        max_value=1.0,
    )
with col2:
    st.number_input(
        "Energía interna [kJ/kg]",
        key='u',
        on_change=manejar_cambio,
        args=('u',),
        format="%.2f",
        step=0.01,
    )
    st.number_input(
        "Entalpía [kJ/kg]",
        key='h',
        on_change=manejar_cambio,
        args=('h',),
        format="%.2f",
        step=0.01,
    )
    st.number_input(
        "Entropía [kJ/(kg·K)]",
        key='s',
        on_change=manejar_cambio,
        args=('s',),
        format="%.4f",
        step=0.0001,
    )

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    calcular = st.button("Calcular")
with col_btn2:
    st.button("Limpiar", on_click=limpiar_campos)

if calcular:
    valores = {k: st.session_state[k] for k in VARIABLES if st.session_state[k] is not None}
    if len(valores) != 2:
        st.error("Por favor, ingrese exactamente dos valores.")
    else:
        pair_map = {frozenset(c): c for c in combinations(VARIABLES, 2)}
        clave = pair_map.get(frozenset(valores.keys()))
        if clave is None:
            st.error("Combinación de propiedades no soportada.")
        else:
            t, p, v, u, h, s, x = calcular_propiedades(
                *clave, st.session_state['fluid'], **valores
            )
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
                st.session_state['input_order'] = []
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()


if st.session_state.get('calculado', False):
    t_session = st.session_state.get('t_num')
    s_session = st.session_state.get('s_num')
    if t_session is not None and s_session is not None:
        fluido = st.session_state['fluid']
        Tcrit = PropsSI('Tcrit', fluido)
        Tmin = PropsSI('Ttriple', fluido)
        Tsat = np.linspace(Tmin, Tcrit, 500)
        s_liq = [PropsSI('S', 'T', T, 'Q', 0, fluido) / 1000 for T in Tsat]
        s_vap = [PropsSI('S', 'T', T, 'Q', 1, fluido) / 1000 for T in Tsat]
        T_C = Tsat - 273.15

        s_user = s_session
        T_user = t_session

        fig, ax = plt.subplots()
        ax.plot(s_liq, T_C, label="Líquido saturado", color="blue")
        ax.plot(s_vap, T_C, label="Vapor saturado", color="red")
        ax.plot(s_user, T_user, "ko", label="Punto ingresado")

        ax.set_xlabel("Entropía específica [kJ/kg·K]")
        ax.set_ylabel("Temperatura [°C]")
        ax.set_title(
            f"Diagrama T–s del {next(k for k, v in FLUID_MAP.items() if v == fluido)}"
        )
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)

