import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Sistema Contable - El Colesterol", layout="wide", page_icon="💰")

# Título principal
st.title("💰 Sistema Contable - El Colesterol")

# --- INICIALIZACIÓN DE DATOS ---
if 'transacciones' not in st.session_state:
    st.session_state.transacciones = []
    
if 'balances' not in st.session_state:
    st.session_state.balances = {
        "Activo": {
            "Caja": 0, 
            "Bancos": 0,
            "Compras": 0,
            "IVA Acreditable": 0,
            "Clientes": 0
        },
        "Pasivo": {
            "IVA Trasladado": 0,
            "Documentos por pagar": 0,
            "Acreedores": 0
        },
        "Ingresos": {
            "Ventas": 0,
            "Descuentos sobre ventas": 0,
            "Devoluciones sobre ventas": 0,
            "Rebajas sobre ventas": 0
        },
        "Costos": {
            "Descuentos sobre compras": 0,
            "Devoluciones sobre compras": 0,
            "Rebajas sobre compras": 0,
            "Costo de lo Vendido": 0
        }
    }

if 'libro_mayor' not in st.session_state:
    st.session_state.libro_mayor = {}

if 'arqueo_caja' not in st.session_state:
    st.session_state.arqueo_caja = {
        "monedas": {
            "Denominación": [0.5, 1, 2, 5, 10, 20],
            "Cantidad": [0, 22, 20, 40, 33, 0],
            "Total": [0, 22, 40, 200, 330, 0]
        },
        "billetes": {
            "Denominación": [20, 50, 100, 200, 500, 1000],
            "Cantidad": [10, 10, 11, 10, 7, 0],
            "Total": [200, 500, 1100, 2000, 3500, 0]
        }
    }

# --- FUNCIONES PRINCIPALES ---
def actualizar_balances(transaccion):
    # Reiniciar balances
    st.session_state.balances = {
        "Activo": {k: 0 for k in st.session_state.balances["Activo"]},
        "Pasivo": {k: 0 for k in st.session_state.balances["Pasivo"]},
        "Ingresos": {k: 0 for k in st.session_state.balances["Ingresos"]},
        "Costos": {k: 0 for k in st.session_state.balances["Costos"]}
    }
    
    # Reiniciar libro mayor
    st.session_state.libro_mayor = {}
    
    # Reprocesar todas las transacciones
    for tx in st.session_state.transacciones:
        for cuenta, monto in tx["deber"].items():
            for categoria in st.session_state.balances:
                if cuenta in st.session_state.balances[categoria]:
                    st.session_state.balances[categoria][cuenta] += monto
                    break
            
            if cuenta not in st.session_state.libro_mayor:
                st.session_state.libro_mayor[cuenta] = {"Debe": [], "Haber": []}
            st.session_state.libro_mayor[cuenta]["Debe"].append(monto)
        
        for cuenta, monto in tx["haber"].items():
            for categoria in st.session_state.balances:
                if cuenta in st.session_state.balances[categoria]:
                    st.session_state.balances[categoria][cuenta] -= monto
                    break
            
            if cuenta not in st.session_state.libro_mayor:
                st.session_state.libro_mayor[cuenta] = {"Debe": [], "Haber": []}
            st.session_state.libro_mayor[cuenta]["Haber"].append(monto)

def registrar_transaccion(transaccion):
    transaccion["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.transacciones.append(transaccion)
    actualizar_balances(transaccion)
    st.success("✅ Transacción registrada correctamente.")

# --- INTERFAZ DE USUARIO ---
# --- SECCIÓN DE TRANSACCIONES ---
with st.expander("📝 Registrar Nueva Transacción", expanded=True):
    tipo_transaccion = st.selectbox(
        'Tipo de Transacción',
        ['Traspaso', 'Compra en efectivo', 'Descuento por pronto pago 10%', 'Ventas del día', 
         'Descuento por pronto pago 8%', 'Devolución de mercancias', 'Devolución de mercancias 2', 
         'Rebaja de mercancia', 'Rebaja sobre la venta', 'Registrar arqueo de caja']
    )

    if tipo_transaccion == 'Traspaso':
        
            bancos = st.number_input("Bancos", min_value=0.0, value=7892.0)
            caja = st.number_input("Caja", min_value=0.0, value=7892.0)
        

    if tipo_transaccion == 'Compra en efectivo':
        col1, col2 = st.columns(2)
        with col1:
            compras = st.number_input("Compras", min_value=0.0, value=2000.0)
            iva_acreditable = st.number_input("IVA Acreditable (16%)", min_value=0.0, value=compras * 0.16)
        with col2:
            total_pagar = compras + iva_acreditable
            st.metric("Total a pagar", f"${total_pagar:,.2f}")
            bancos = st.number_input("Monto a pagar desde Bancos", min_value=0.0, value=compras + iva_acreditable)

    elif tipo_transaccion == 'Descuento por pronto pago 10%':
        col1, col2 = st.columns(2)
        with col1:
            descuento = st.number_input("Descuento sobre compras", min_value=0.0, value=200.0)
            iva_acreditable = st.number_input("IVA Acreditable", min_value=0.0, value=descuento * 0.16)
            compras = st.number_input("Bancos", min_value=0.0, value= descuento + iva_acreditable)
        with col2:
            total_pagar = compras 
            st.metric("Total a pagar", f"${total_pagar:,.2f}")
            

    elif tipo_transaccion == 'Ventas del día':
        col1, col2 = st.columns(2)
        with col1:
            ventas = st.number_input("Valor de venta", min_value=0.0, value=2500.0)
            iva_trasladado = st.number_input("IVA Trasladado (16%)", min_value=0.0, value=ventas * 0.16)
        with col2:
            total_cobrar = ventas + iva_trasladado
            bancos = st.number_input("Monto a recibir en Bancos", min_value=0.0, value=ventas + iva_trasladado)
            st.metric("Total", f"${total_cobrar:,.2f}")

    elif tipo_transaccion == 'Descuento por pronto pago 8%':
        col1, col2 = st.columns(2)
        with col1:
            descuento = st.number_input("Descuento sobre compras", min_value=0.0, value=200.0)
            iva_trasladado = st.number_input("IVA Acreditable", min_value=0.0, value=descuento * 0.16)
            compras = st.number_input("Bancos", min_value=0.0, value= descuento + iva_trasladado)
        with col2:
            total_pagar = compras 
            st.metric("Total a pagar", f"${total_pagar:,.2f}")

    elif tipo_transaccion == 'Devolución de mercancias':
        col1, col2 = st.columns(2)
        with col1:
            devVentas = st.number_input("Devolución sobre ventas", min_value=0.0, value=300.0)
            iva_acreditable = st.number_input("IVA Trasladado", min_value=0.0, value=devVentas* 0.16)
            bancos = st.number_input("Bancos", min_value=0.0, value= devVentas + iva_acreditable)
        with col2:
            total_pagar = bancos
            st.metric("Total a pagar", f"${total_pagar:,.2f}")

    elif tipo_transaccion == 'Devolución de mercancias 2':
        col1, col2 = st.columns(2)
        with col1:
            devCompras = st.number_input("Devolución sobre compras", min_value=0.0, value=400.0)
            iva_acreditable = st.number_input("IVA Trasladado", min_value=0.0, value=devCompras* 0.16)
            bancos = st.number_input("Bancos", min_value=0.0, value= devCompras + iva_acreditable)
        with col2:
            total_pagar = bancos
            st.metric("Total a pagar", f"${total_pagar:,.2f}")

    elif tipo_transaccion == 'Rebaja de mercancia':
        col1, col2 = st.columns(2)
        with col1:
            rebajas = st.number_input("Rebaja sobre compras", min_value=0.0, value=450.0)
            iva_acreditable = st.number_input("IVA Trasladado", min_value=0.0, value=rebajas* 0.16)
            bancos = st.number_input("Bancos", min_value=0.0, value= rebajas + iva_acreditable)
        with col2:
            total_pagar = bancos
            st.metric("Total a pagar", f"${total_pagar:,.2f}")

    elif tipo_transaccion == 'Rebaja sobre la venta':
        col1, col2 = st.columns(2)
        with col1:
            rebajas = st.number_input("Rebaja sobre ventas", min_value=0.0, value=500.0)
            iva_trasladado = st.number_input("IVA Trasladado", min_value=0.0, value=rebajas* 0.16)
            bancos = st.number_input("Bancos", min_value=0.0, value= rebajas + iva_trasladado)
        with col2:
            total_pagar = bancos
            st.metric("Total a pagar", f"${total_pagar:,.2f}")

    elif tipo_transaccion == 'Registrar arqueo de caja':
        st.subheader("Monedas")
        cols = st.columns(6)
        for i, denom in enumerate(st.session_state.arqueo_caja["monedas"]["Denominación"]):
            with cols[i]:
                cantidad = st.number_input(
                    f"${denom}", 
                    min_value=0, 
                    value=st.session_state.arqueo_caja["monedas"]["Cantidad"][i],
                    key=f"moneda_{i}"
                )
                st.session_state.arqueo_caja["monedas"]["Cantidad"][i] = cantidad
                st.session_state.arqueo_caja["monedas"]["Total"][i] = cantidad * denom
        
        st.subheader("Billetes")
        cols = st.columns(6)
        for i, denom in enumerate(st.session_state.arqueo_caja["billetes"]["Denominación"]):
            with cols[i]:
                cantidad = st.number_input(
                    f"${denom}", 
                    min_value=0, 
                    value=st.session_state.arqueo_caja["billetes"]["Cantidad"][i],
                    key=f"billete_{i}"
                )
                st.session_state.arqueo_caja["billetes"]["Cantidad"][i] = cantidad
                st.session_state.arqueo_caja["billetes"]["Total"][i] = cantidad * denom
        
        # Actualizar caja en balances
        total_monedas = sum(st.session_state.arqueo_caja["monedas"]["Total"])
        total_billetes = sum(st.session_state.arqueo_caja["billetes"]["Total"])
        st.session_state.balances["Activo"]["Caja"] = total_monedas + total_billetes
        st.success("Arqueo de caja actualizado correctamente")
        st.stop()

    if st.button("Registrar Transacción") and tipo_transaccion != 'Seleccionar...':
        transaccion = {"tipo": tipo_transaccion, "deber": {}, "haber": {}}
        
        if tipo_transaccion == 'Compra en efectivo':
            transaccion["deber"]["Compras"] = compras
            transaccion["deber"]["IVA Acreditable"] = iva_acreditable
            transaccion["haber"]["Bancos"] = bancos
        
        elif tipo_transaccion == 'Descuento por pronto pago 10%':
            transaccion["deber"]["Bancos"] = compras
            transaccion["haber"]["Descuentos sobre compras"] = descuento
            transaccion["haber"]["IVA Acreditable"] = iva_acreditable
        
        elif tipo_transaccion == 'Ventas del día':
            transaccion["deber"]["Bancos"] = bancos
            transaccion["haber"]["Ventas"] = ventas
            transaccion["haber"]["IVA Trasladado"] = iva_trasladado

        elif tipo_transaccion == 'Traspaso':
            transaccion["deber"]["Bancos"] = bancos
            transaccion["haber"]["Caja"] = caja

        elif tipo_transaccion == 'Descuento por pronto pago 8%':
            transaccion["haber"]["Bancos"] = compras
            transaccion["deber"]["Descuentos sobre ventas"] = descuento
            transaccion["deber"]["IVA Trasladado"] = iva_trasladado

        elif tipo_transaccion == 'Devolución de mercancias':
            transaccion["deber"]["Bancos"] = bancos
            transaccion["haber"]["Devoluciones sobre ventas"] = devVentas
            transaccion["haber"]["IVA Acreditable"] = iva_acreditable

        elif tipo_transaccion == 'Devolución de mercancias 2':
            transaccion["haber"]["Bancos"] = bancos
            transaccion["deber"]["Devoluciones sobre compras"] = devCompras
            transaccion["deber"]["IVA Trasladado"] = iva_acreditable

        elif tipo_transaccion == 'Rebaja de mercancia':
            transaccion["deber"]["Bancos"] = bancos
            transaccion["haber"]["Rebajas sobre compras"] = rebajas
            transaccion["haber"]["IVA Acreditable"] = iva_acreditable

        elif tipo_transaccion == 'Rebaja sobre la venta':
            transaccion["haber"]["Bancos"] = bancos
            transaccion["deber"]["Rebajas sobre ventas"] = rebajas
            transaccion["deber"]["IVA Trasladado"] = iva_trasladado
        
        registrar_transaccion(transaccion)

# --- SECCIÓN DE REPORTES ---
tab1, tab2, tab3, tab4,tab5 = st.tabs([
    "📋 Transacciones", "⚖️ Balanza", "📈 Resultados", "🏦 Arqueo","📚 Libro Mayor"
])

with tab1:
    st.subheader("Transacciones Registradas")
    if st.session_state.transacciones:
        st.dataframe(pd.DataFrame(st.session_state.transacciones), use_container_width=True)
    else:
        st.info("No hay transacciones registradas.")

with tab2:
    st.subheader("Balanza de Comprobación")
    
    # Preparar datos para la balanza
    cuentas = []
    saldo_debe = []
    saldo_haber = []
    
    for categoria in st.session_state.balances:
        for cuenta, saldo in st.session_state.balances[categoria].items():
            if saldo != 0:  # Solo mostrar cuentas con saldo
                cuentas.append(cuenta)
                if saldo > 0:
                    saldo_debe.append(abs(saldo))
                    saldo_haber.append(0)
                else:
                    saldo_debe.append(0)
                    saldo_haber.append(abs(saldo))
    
    if cuentas:
        balanza_df = pd.DataFrame({
            "Cuenta": cuentas,
            "Debe": saldo_debe,
            "Haber": saldo_haber
        })
        
        st.dataframe(
            balanza_df.style.format({
                "Debe": "${:,.2f}",
                "Haber": "${:,.2f}"
            }),
            use_container_width=True
        )
        
        # Totales
        total_debe = balanza_df["Debe"].sum()
        total_haber = balanza_df["Haber"].sum()
        
        col1, col2 = st.columns(2)
        col1.metric("Total Debe", f"${total_debe:,.2f}")
        col2.metric("Total Haber", f"${total_haber:,.2f}", 
                    delta=f"${(total_debe - total_haber):,.2f}" if total_debe != total_haber else "Balanceado")
    else:
        st.info("No hay movimientos para mostrar")

with tab3:
    st.subheader("Estado de Resultados")
    
    # Obtener valores relevantes de los balances
    ventas_totales = (st.session_state.balances["Ingresos"].get("Ventas", 0)*-1)
    desc_ventas = st.session_state.balances["Ingresos"].get("Descuentos sobre ventas", 0)
    dev_ventas = st.session_state.balances["Ingresos"].get("Devoluciones sobre ventas", 0)
    reb_ventas = st.session_state.balances["Ingresos"].get("Rebajas sobre ventas", 0)
    
    # Cálculo de ventas netas
    ventas_netas = ventas_totales - (desc_ventas + dev_ventas + reb_ventas)
    
    # Obtener valores de compras
    compras_totales = st.session_state.balances["Activo"].get("Compras", 0)
    gastos_compras = 0  # Asumiendo que no hay gastos de compras
    dev_compras = st.session_state.balances["Costos"].get("Devoluciones sobre compras", 0)
    desc_compras = (st.session_state.balances["Costos"].get("Descuentos sobre compras", 0)*-1)
    reb_compras = st.session_state.balances["Costos"].get("Rebajas sobre compras", 0)*-1
    
    
    #Sumas extras
    devreb_ventas =  desc_ventas + dev_ventas + reb_ventas
    rebCompras = desc_compras + dev_compras + reb_compras
    
    
    
    
    # Cálculo de compras netas
    compras_netas = compras_totales - rebCompras

    # Cálculo de mercancías disponibles y costo de ventas
    mercancias_disponibles = compras_netas

    
    # Inventarios
    inventario_inicial = 0.00
    inventario_final = mercancias_disponibles * 0.03
    

    costo_ventas = mercancias_disponibles - inventario_final
    
    
    # Cálculo de utilidad bruta
    utilidad_bruta = ventas_netas - costo_ventas
    
    # Gastos de operación
    gastos_venta = 0.00
    gastos_administracion = 0.00
    total_gastos_operacion = gastos_venta + gastos_administracion
    
    # Utilidad por operación
    utilidad_operacion = utilidad_bruta - total_gastos_operacion
    
    # Otros ingresos y gastos
    otros_ingresos_gastos = 0.00
    utilidad_final = utilidad_operacion + otros_ingresos_gastos

    
    

    # Crear DataFrame con 5 columnas (Concepto + 4 numéricas)
    resultados = [
        ["Ventas totales", "", "", ventas_totales , ""],
        ["Descuentos sobre ventas", "", desc_ventas, "", ""],
        ["Devoluciones/Rebajas sobre ventas", "", dev_ventas + reb_ventas, devreb_ventas, ""],
        ["Ventas netas", "", "", "", ventas_netas],
        ["Inventario Inicial", "", "", inventario_inicial, ""],
        ["Compras", compras_totales, "", "", ""],
        ["Gastos de compras", gastos_compras, "", "", ""],
        ["Compras totales", "", compras_totales + gastos_compras, "", ""],
        ["Devoluciones sobre compra", dev_compras, "", "", ""],
        ["Descuentos sobre compras", desc_compras, "", "", ""],
        ["Rebajas sobre compra", reb_compras, rebCompras, "", ""],
        ["Compras netas", "", "", compras_netas, ""],
        ["Mercancías disponibles", "", "", mercancias_disponibles, ""],
        ["Inventario Final", "", "", inventario_final, ""],
        ["Costo de ventas", "", "", "", costo_ventas],
        ["Utilidad bruta", "", "", "", utilidad_bruta],
        ["Gastos de operación", "", "", "", ""],  # Fila de título
        ["Gastos de venta", "", "", gastos_venta, ""],
        ["Gastos de administración", "", "", gastos_administracion, gastos_venta + gastos_administracion],
        ["Utilidad por operación", "", "", "", utilidad_operacion],
        ["Otros ingresos y gastos", "", "", "", ""],  # Fila de título
        ["Donaciones", "", "", 0.00, ""],
        ["Perdida en venta de inmuebles", "", "", 0.00, 0.00],
        ["Total", "", "", "", utilidad_final]
    ]
    
    # Crear DataFrame con las columnas especificadas
    df_resultados = pd.DataFrame(resultados, columns=["Concepto", "1", "2", "3", "4"])
    
    # Función para formatear valores
    def format_value(val):
        if isinstance(val, (int, float)):
            return f"${val:,.2f}" if val != 0 else "$0.00"
        return val
    
    # Aplicar formato a las columnas numéricas
    for col in ["1", "2", "3", "4"]:
        df_resultados[col] = df_resultados[col].apply(format_value)
    
    # Mostrar el DataFrame
    st.dataframe(
        df_resultados,
        use_container_width=True,
        hide_index=True
    )
    
    # Métricas resumen
    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas Netas", f"${ventas_netas:,.2f}")
    col2.metric("Utilidad Bruta", f"${utilidad_bruta:,.2f}")
    col3.metric("Utilidad Final", f"${utilidad_final:,.2f}")

with tab4:
    st.subheader("Arqueo de Caja")
    
    # Mostrar datos de arqueo
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Monedas")
        st.dataframe(
            pd.DataFrame(st.session_state.arqueo_caja["monedas"])
            .style.format({"Denominación": "${:,.2f}", "Total": "${:,.2f}"})
        )
        
    with col2:
        st.markdown("#### Billetes")
        st.dataframe(
            pd.DataFrame(st.session_state.arqueo_caja["billetes"])
            .style.format({"Denominación": "${:,.2f}", "Total": "${:,.2f}"})
        )
    
    # Calcular totales
    total_monedas = sum(st.session_state.arqueo_caja["monedas"]["Total"])
    total_billetes = sum(st.session_state.arqueo_caja["billetes"]["Total"])
    total_efectivo = total_monedas + total_billetes
    
    st.metric("Total Efectivo en Caja", f"${total_efectivo:,.2f}")
    
with tab5:
    # --- SECCIÓN LIBRO MAYOR ---
    st.subheader("📚 Libro Mayor")
    
    if st.session_state.libro_mayor:
        for cuenta, movimientos in st.session_state.libro_mayor.items():
            # Título de la cuenta
            st.subheader(f"Cuenta: {cuenta}")
            
            # Filtrar transacciones para esta cuenta
            transacciones_cuenta = [
                tx for tx in st.session_state.transacciones 
                if cuenta in tx["deber"] or cuenta in tx["haber"]
            ]
            
            if transacciones_cuenta:
                # Crear DataFrame con los datos correctamente estructurados
                data = {
                    "Fecha": [tx["fecha"] for tx in transacciones_cuenta],
                    "Concepto": [tx["tipo"] for tx in transacciones_cuenta],
                    "Debe": [tx["deber"].get(cuenta, 0) for tx in transacciones_cuenta],
                    "Haber": [tx["haber"].get(cuenta, 0) for tx in transacciones_cuenta]
                }
                
                df_movimientos = pd.DataFrame(data)
                
                # Mostrar tabla de movimientos
                st.dataframe(
                    df_movimientos.style.format({
                        "Debe": "${:,.2f}",
                        "Haber": "${:,.2f}"
                    }),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Calcular totales
                total_debe = df_movimientos["Debe"].sum()
                total_haber = df_movimientos["Haber"].sum()
                saldo = total_debe - total_haber
                
                # Mostrar resumen
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Debe", f"${total_debe:,.2f}")
                col2.metric("Total Haber", f"${total_haber:,.2f}")
                col3.metric("Saldo", 
                            f"${abs(saldo):,.2f}", 
                            "Deudor" if saldo > 0 else "Acreedor" if saldo < 0 else "Cero")
            else:
                st.info(f"No hay movimientos para la cuenta {cuenta}")
            st.markdown("---")  # Separador entre cuentas
    else:
        st.info("No hay movimientos registrados en el libro mayor.")