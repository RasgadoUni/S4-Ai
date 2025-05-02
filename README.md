<div align="center">
  <h1 align="center">
    S4-Ai
  </h1>
</div>

<br />
<br />

![image](https://github.com/user-attachments/assets/340e25d7-53ec-4351-9dd6-4a283abb2b57)
![image](https://github.com/user-attachments/assets/9bea5d80-ed68-414e-813f-f593d25849cc)
<h2>
	Imagenes referentes a registros de nuevas transacciones, así como la opción de escoger las transacciones
</h2>

<br />
<br />


![image](https://github.com/user-attachments/assets/289c408a-bc4c-49ca-82f7-3207b4107b60)
<h2>
Imagen del libro diario con registro de transacciones
</h2>

<br />
<br />

		
![image](https://github.com/user-attachments/assets/db1264a8-c652-4b68-a3a6-1a8f9f76d18d)
<h2>Esa es la imagen de la balanza de comprobación </h2> 

<br />
<br />


![image](https://github.com/user-attachments/assets/d6ffda02-0d64-4485-a600-14de52be951f)
![image](https://github.com/user-attachments/assets/b035f1bf-3113-4696-b5e1-1982a064d53a)
<h2> El estado de resultados </h2>

<br />
<br />


![image](https://github.com/user-attachments/assets/48cd80ff-4254-4c17-95aa-96ab8f40577d)
![image](https://github.com/user-attachments/assets/1dada476-25e1-4930-8996-7283821367c6)
![image](https://github.com/user-attachments/assets/9a9920bb-7baa-4148-a9ab-8a9930208a4d)
![image](https://github.com/user-attachments/assets/4edc7148-100f-4985-9ba2-9ed275a4fab1)
![image](https://github.com/user-attachments/assets/571c13f5-ca1b-4452-9663-58bd6133ace3)
<h2>El libro mayor </h2>

<br />
<br />


![image](https://github.com/user-attachments/assets/f9097527-b11e-42e6-b813-156ed3be179d)

<h2>Y el arqueo de caja </h2>

<h1>
	Aqui una breve explicacion del codigo
</h1>




<h1>Sistema Contable - El Colesterol</h1>

<h2>Descripción General</h2>
<p>Este sistema contable implementa los libros principales de contabilidad usando Python y Streamlit. La estructura básica inicializa los datos con:</p>

<pre>
if 'transacciones' not in st.session_state:
st.session_state.transacciones = []

if 'balances' not in st.session_state:
st.session_state.balances = {
"Activo": {"Caja": 0, "Bancos": 0, ...},
"Pasivo": {"IVA Trasladado": 0, ...},
...
}</pre>

<h2>Funcionalidades Clave</h2>

<h3>1. Registro de Transacciones</h3>
<p>El sistema permite registrar diferentes tipos de transacciones mediante un formulario dinámico:</p>

<pre>
tipo_transaccion = st.selectbox(
'Tipo de Transacción',
['Traspaso', 'Compra en efectivo', 'Ventas del día', ...]
)

if tipo_transaccion == 'Compra en efectivo':
compras = st.number_input("Compras", min_value=0.0)
iva_acreditable = compras * 0.16</pre>

<h3>2. Procesamiento Contable</h3>
<p>Cada transacción se registra con doble entrada:</p>

<pre>
def registrar_transaccion(transaccion):
transaccion["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.session_state.transacciones.append(transaccion)
actualizar_balances(transaccion)</pre>

<p>La función <code>actualizar_balances()</code> recalcula todos los saldos:</p>

<pre>
for tx in st.session_state.transacciones:
for cuenta, monto in tx["deber"].items():
if cuenta in st.session_state.balances[categoria]:
st.session_state.balances[categoria][cuenta] += monto</pre>

<h3>3. Reportes Contables</h3>

<h4>Libro Diario</h4>
<pre>
st.dataframe(pd.DataFrame(st.session_state.transacciones))</pre>

<h4>Balanza de Comprobación</h4>
<pre>
balanza_df = pd.DataFrame({
"Cuenta": cuentas,
"Debe": saldo_debe,
"Haber": saldo_haber
})</pre>

<h4>Estado de Resultados</h4>
<p>Calcula automáticamente la utilidad:</p>
<pre>
ventas_netas = ventas_totales - (desc_ventas + dev_ventas + reb_ventas)
utilidad_bruta = ventas_netas - costo_ventas</pre>

<h4>Libro Mayor</h4>
<pre>
for cuenta, movimientos in st.session_state.libro_mayor.items():
st.subheader(f"Cuenta: {cuenta}")
st.dataframe(pd.DataFrame(movimientos))</pre>

<h4>Arqueo de Caja</h4>
<pre>
st.session_state.arqueo_caja = {
"monedas": {
"Denominación": [0.5, 1, 2, 5, 10, 20],
"Cantidad": [0, 22, 20, 40, 33, 0],
"Total": [0, 22, 40, 200, 330, 0]
},
...
}</pre>

<h2>Flujo del Programa</h2>
<ol>
<li>Inicializa los estados de sesión con <code>st.session_state</code></li>
<li>Muestra el formulario de transacciones con <code>st.selectbox</code> y <code>st.number_input</code></li>
<li>Al registrar, llama a <code>registrar_transaccion()</code> que:
<pre>transaccion = {
"tipo": tipo_transaccion,
"deber": {"Cuenta1": monto1},
"haber": {"Cuenta2": monto2}
}</pre>
</li>
<li>Actualiza todos los reportes automáticamente</li>
</ol>
