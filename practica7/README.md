# Práctica 7: Comparación Reactor Batch vs CSTR

Estudio comparativo de dos configuraciones de reactores: discontinuo (Batch) y continuo (CSTR). Analiza diferencias fundamentales en conversión, tiempo de operación, productividad y eficiencia energética.

**Dificultad:** ⭐⭐⭐⭐ (Avanzado) | **Duración:** 2-3 horas

---

## Objetivos de Aprendizaje

Al completar esta práctica, serás capaz de:

1. ✅ Entender diferencias fundamentales entre reactores Batch y CSTR
2. ✅ Modelar dinámicamente un reactor Batch desde inicio hasta fin
3. ✅ Comparar conversión final en ambas configuraciones
4. ✅ Analizar productividad y tiempo de ciclo
5. ✅ Seleccionar configuración óptima según especificaciones

---

## Conceptos Clave

### Reactor Batch
Operación **discontinua** - Sin flujos de entrada/salida durante reacción:

```
    Carga inicial
         ↓
    [Reactor BATCH]  ← Calor (si es exotérmica/endotérmica)
    (Sin flujos)
         ↓
    Esperar tiempo t_reacción
         ↓
    Descarga de productos
```

**Características:**
- Conversión varía con tiempo: X(t) aumenta desde 0 a X_final
- Composición uniforme en el reactor (mezcla perfecta)
- Tiempo total = carga + reacción + descarga
- Típico: pequeña escala, productos especiales, lotes

**Ecuación de diseño:**
```
dX/dt = k(T)·f(X)

Para orden 1: dX/dt = k·(1-X)
Solución: X(t) = 1 - exp(-k·t)

Tiempo para alcanzar conversión: t = -ln(1-X)/k
```

### Reactor CSTR
Operación **continua** - Flujos constantemente:

```
    Entrada (F₀, X=0)
         ↓
    [CSTR con mezcla]  ← Calor
    (Salida = composición reactor)
         ↓
    Salida (F, X_ss)
```

**Características:**
- Conversión estacionaria: alcanzada en ~3-5 tiempos de residencia
- Salida tiene misma composición que interior
- Tiempo de residencia: τ = V/F
- Típico: producción continua, alto volumen

**Relación conversión-resistencia:**
```
τ·k = X / (1-X)   [primer orden]

X = (k·τ) / (1 + k·τ)  [despejando X]
```

### Comparación Cualitativa

| Aspecto | Batch | CSTR |
|---------|-------|------|
| **Modo** | Discontinuo | Continuo |
| **Conversión** | Aumenta con tiempo | Constante (Estado Est.) |
| **Escala** | Pequeña-Media | Media-Grande |
| **Complejidad** | Baja | Media (control flujos) |
| **Flexibilidad** | Alta (cambiar lotes) | Baja (cambiar productos) |
| **Capital** | Bajo | Medio-Alto |
| **Operación** | Bajo (manual) | Alto (automatizado) |
| **Tiempo de ciclo** | Incluye carga/descarga | Solo reacción |

### Productividad
Define eficiencia del sistema:

```
Productividad_Batch = (F_salida · X_final) / t_total
                    = (F_salida · X_final) / (t_carga + t_reacción + t_descarga)

Productividad_CSTR = (F_salida · X_ss) / 1  [tiempo infinito = estado estacionario]

En comparación justa: normalizar por volumen reactor
```

### Tiempo de Residencia vs Tiempo de Reacción
**No son lo mismo:**

```
Batch:
- Tiempo reacción: t_rxn = -ln(1-X) / k
- Tiempo total: t_total = t_rxn + t_carga + t_descarga

CSTR:
- Tiempo residencia: τ = V/F
- Tiempo alcanzar estado estacionario: ~3-5·τ
```

---

## Archivos de la Práctica

- **`aspython.py`**: Script que simula ambos reactores en ASPEN HYSYS. Reactor Batch: integración temporal hasta conversión final. Reactor CSTR: estado estacionario con mismo volumen/parámetros
- **`py_alone.py`**: Cálculos cinéticos sin HYSYS. Integra ecuación Batch dX/dt = k·(1-X), calcula conversión vs tiempo, compara con CSTR estacionario
- **`visualiza1.py`**: Gráficas: Conversión vs tiempo Batch, línea de CSTR estado estacionario superpuesta, análisis del punto de cruce
- **`visualiza2.py`**: Análisis económico simulado: productividad, tiempo de ciclo, rentabilidad relativa para diferentes flujos

---

## Cómo Usar Esta Práctica

### 1. Simulación Completa en ASPEN HYSYS

```bash
python practica7/aspython.py
```

Realiza:
- **Reactor Batch:**
  - Carga inicial (Methanol puro, CA0 = 1 mol/L, 100 L)
  - Especifica tiempo final de reacción (ej. 100 minutos)
  - Integra ecuación de velocidad
  - Obtiene conversión final

- **Reactor CSTR equivalente:**
  - Mismo volumen (100 L)
  - Mismo parámetros cinéticos (A, Eₐ)
  - Calcula tiempo de residencia necesario para misma conversión
  - O compara directamente con τ = t_rxn

- **Comparación:**
  - ¿Cuál logra mayor conversión en mismo tiempo?
  - ¿Cuál tiene mayor productividad?
  - ¿Cuál es más rentable?

### 2. Cálculos Dinámicos Independientes

```bash
python practica7/py_alone.py
```

Resuelve ecuaciones diferenciales:
```python
# Batch
dX/dt = k(T)·(1-X)  # Integra desde t=0 hasta t_final

# CSTR (comparación rápida)
X_ss = k·τ / (1 + k·τ)
```

Genera tabla mostrando:
- Batch: X en función de tiempo (cada 10 minutos)
- CSTR: X constante (estado estacionario)

### 3. Gráficas Conversión vs Tiempo

```bash
python practica7/visualiza1.py
```

Genera:
- **Curva Batch:** X(t) sigmoide suave (primer orden)
- **Línea CSTR:** X_ss horizontal (estado estacionario)
- **Cruce:** punto donde ambos tienen igual conversión
- **Análisis:** ¿A qué t_batch = t_residencia_CSTR?

### 4. Análisis Económico y Productividad

```bash
python practica7/visualiza2.py
```

Simula:
- Productividad relativa (Batch vs CSTR) vs conversión objetivo
- Tiempo de ciclo Batch (incluye carga 10 min, descarga 10 min)
- Rendimiento económico simulado ($/kg producto)
- Conclusión: ¿Cuándo usar cada configuración?

---

## Ejercicios Sugeridos

### Ejercicio 7.1: Cálculo Manual Batch vs CSTR (25 min)
**Nivel:** ⭐⭐

**Datos:**
```
Reacción primer orden: A → B
k = 0.05 min⁻¹
Objetivo: X = 80%
```

**Reactor Batch:**
Calcular tiempo necesario para alcanzar 80% conversión.

```
X(t) = 1 - exp(-k·t)
0.80 = 1 - exp(-0.05·t)
exp(-0.05·t) = 0.20
t_batch = -ln(0.20) / 0.05 = ?
```

**Reactor CSTR con τ = t_batch:**
Calcular conversión estacionaria.

```
X_CSTR = (k·τ) / (1 + k·τ)
X_CSTR = (0.05·t_batch) / (1 + 0.05·t_batch) = ?
```

**Conclusión:** ¿Cuál alcanza mayor conversión en mismo tiempo?

### Ejercicio 7.2: Equivalencia de Volúmenes (30 min)
**Nivel:** ⭐⭐⭐

Para lograr **misma conversión final** (80%), ¿qué relación de volúmenes se necesita?

**Supuestos:**
- Batch: espera t_batch
- CSTR: opera continuamente, F_entrada = 1 L/min
- Ambos con k = 0.05 min⁻¹

**Procedimiento:**
1. Calcula t_batch para X = 80% (del ejercicio anterior)
2. Calcula V_CSTR necesario para τ = t_batch
3. Compara: ¿V_CSTR vs V_Batch?

**Respuesta esperada:** V_CSTR ~ 0.44·V_Batch (mucho menor para CSTR)

### Ejercicio 7.3: Productividad con Tiempos Muertos (25 min)
**Nivel:** ⭐⭐⭐

**Reactor Batch de 100 L:**
```
Tiempo carga:    10 min
Tiempo reacción: t_batch = ? (de ejercicio 7.1)
Tiempo descarga: 10 min
Total: t_total = 20 + t_batch

Productividad = (100 L · 0.80) / t_total [kg/h si consideramos densidad]
```

**Reactor CSTR de 50 L:**
```
Flujo entrada: 1 L/min
Tiempo residencia: τ = 50/1 = 50 min
Conversión estado estacionario: X_CSTR = (de ejercicio 7.1)

Productividad = (1 L/min · X_CSTR) [continuamente]
```

**Comparación:** ¿Cuál produce más?

### Ejercicio 7.4: Cinética de Segundo Orden (30 min)
**Nivel:** ⭐⭐⭐⭐

Repetir ejercicio 7.1 pero con reacción de **segundo orden**:

```
-dCA/dt = k·CA²

Solución: CA(t) = CA0 / (1 + k·CA0·t)

Conversión: X = 1 - CA/CA0 = (k·CA0·t) / (1 + k·CA0·t)

Tiempo para X: t = 1 / (k·CA0·(1-X))
```

**Preguntas:**
1. Tiempo de Batch para X = 80% (orden 2)
2. Comparar con orden 1 - ¿Cuál es más rápido?
3. ¿Por qué depende de CA0?

---

## Notas Técnicas

### Dinámicas Transientes

En HYSYS, un reactor Batch en Python requiere:
1. Especificar volumen inicial
2. Integrar ecuación: dX/dt = k(T)·f(X)
3. Usar método numérico (RK4, método implícito)
4. Reportar X(t) en varios puntos

Alternativamente, calcular X_final analíticamente e informar.

### Efectos No Modelados

En realidad, hay complicaciones:
- **Acumulación de calor:** reacción exotérmica sin control T → runaway
- **Gradientes:** si no hay mezcla perfecta, hay "cold spots"
- **Cambios de volumen:** si hay reacción gaseosa
- **Evaporación:** en fases volátiles

### Selección de Configuración Real

**Elegir Batch si:**
- Producto de alto valor (farmacéuticos, especiales)
- Flexibilidad en recetas necesaria
- Escala pequeña (<100 kg/día)
- Parada frecuente para cambios

**Elegir CSTR si:**
- Producción alta (>1 ton/día)
- Producto commodity
- Demanda constante
- Control automático necesario

**Elegir Tubular o PFR si:**
- Necesitas máxima conversión con mínimo volumen
- Reacciones sensibles a composición local

---

## Referencias

- ASPEN HYSYS: Batch Reactor y CSTR Reactor
- Fogler, H.S. "Elements of Chemical Reaction Engineering" - Capítulos 3-5
- Levenspiel, O. "Chemical Reaction Engineering" - Diseño de reactores
- Himmelblau & Riggs. "Basic Principles and Calculations in Chemical Engineering"

---

**Anterior:** [Práctica 6 - Cinética de Arrhenius](../practica6/README.md)

**Siguiente:** [Práctica 8 - Planta Biodiesel Completa](../practica8/README.md)
