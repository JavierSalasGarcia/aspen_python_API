# Práctica 6: Reactor CSTR con Cinética de Arrhenius

Reactor CSTR donde la velocidad de reacción se controla mediante la ecuación de Arrhenius. Simula reacciones reales dependientes de temperatura y estudia el efecto de parámetros cinéticos.

**Dificultad:** ⭐⭐⭐ (Avanzado) | **Duración:** 1.5-2 horas

---

## Objetivos de Aprendizaje

Al completar esta práctica, serás capaz de:

1. ✅ Entender y aplicar la ecuación de Arrhenius en ASPEN HYSYS
2. ✅ Crear reactores controlados por cinética de reacción
3. ✅ Analizar el efecto de temperatura en velocidad de reacción
4. ✅ Calcular energía de activación y factor pre-exponencial
5. ✅ Estimar conversión en función de temperatura y tiempo de residencia

---

## Conceptos Clave

### Ecuación de Arrhenius
Describe la velocidad de una reacción elemental como función de temperatura:

```
k = A · exp(-Eₐ / RT)

k    = constante de velocidad (s⁻¹)
A    = factor pre-exponencial (s⁻¹)
Eₐ   = energía de activación (kJ/mol)
R    = constante de gases (8.314 J/mol·K)
T    = temperatura absoluta (K)
```

**Interpretación:**
- A: frecuencia de colisiones efectivas
- Eₐ: barrera energética para la reacción
- Mayor Eₐ → mayor dependencia con T

### Velocidad de Reacción
Para reacción de orden n respecto a reactante A:

```
r = -d[A]/dt = k·[A]ⁿ

Orden 0: r = k (velocidad constante)
Orden 1: r = k·[A] (primera orden)
Orden 2: r = k·[A]² (segunda orden)
```

### Tiempo de Residencia
En reactor CSTR:

```
τ = V/F = volumen / flujo volumétrico

Conversión CSTR: τ·k·CA0 = X / (1-X)  [para orden 1]
```

### Efecto de Temperatura en Conversión
Mayor temperatura:
- Aumenta k exponencialmente (Arrhenius)
- Aumenta conversión (si endotérmica o limitada por cinética)
- Puede desplazar equilibrio (si reversible)

**Regla empírica:** Velocidad se duplica cada 10°C (aproximadamente)

### Relación de Arrhenius Integrada
Si conoces k en dos temperaturas:

```
ln(k₂/k₁) = (Eₐ/R)·(1/T₁ - 1/T₂)

Eₐ = R·ln(k₂/k₁) / (1/T₁ - 1/T₂)
```

---

## Archivos de la Práctica

- **`aspython.py`**: Script que configura reactor CSTR con cinética de Arrhenius. Parámetros: A = 1.0e8 s⁻¹, Eₐ = 65 kJ/mol. Simula reacción A → B de primer orden
- **`py_alone.py`**: Cálculos de cinética sin HYSYS. Integra ecuaciones de velocidad, calcula k(T) con Arrhenius, predice conversión vs tiempo y temperatura
- **`visualiza1.py`**: Gráficas de Arrhenius: ln(k) vs 1/T (gráfica de Arrhenius), k vs T, velocidad de reacción vs T
- **`visualiza2.py`**: Estudio paramétrico: conversión vs temperatura para diferentes tiempos de residencia, diagrama de operación reactor

---

## Cómo Usar Esta Práctica

### 1. Simulación Completa en ASPEN HYSYS

```bash
python practica6/aspython.py
```

Realiza:
- Configuración de componentes A (Methanol) y B (Ethanol)
- Definición de reacción elemental A → B primer orden
- Especificación de parámetros Arrhenius (A, Eₐ)
- Creación de reactor CSTR con cinética acoplada
- Simulación a temperatura base (por ej. 50°C)
- Estudio de sensibilidad: conversión vs temperatura (+/- 20°C)
- Cálculo de propiedades termodinámicas de salida

### 2. Cálculos Cinéticos Independientes

```bash
python practica6/py_alone.py
```

Sin ASPEN HYSYS:
- Define parámetros Arrhenius (A, Eₐ)
- Calcula k(T) en rango de temperaturas
- Integra ODE de primer orden: dA/dt = -k·[A]
- Predice conversión vs tiempo
- Crea tabla conversión vs temperatura
- Valida contra resultados HYSYS

### 3. Gráfica de Arrhenius

```bash
python practica6/visualiza1.py
```

Genera:
- **Gráfica clásica:** ln(k) vs 1/T (recta con pendiente Eₐ/R)
- **Gráfica alternativa:** k vs T (exponencial)
- **Gráfica velocidad:** r vs T a CA fija
- Extrae Eₐ del ajuste lineal

### 4. Diagramas de Operación Reactor

```bash
python practica6/visualiza2.py
```

Crea gráficas mostrando:
- Conversión vs temperatura para τ = 1, 5, 10, 20 minutos
- "Mapa" de operación: zona de baja/media/alta conversión
- Temperatura óptima para conversión objetivo

---

## Ejercicios Sugeridos

### Ejercicio 6.1: Cálculo de Energía de Activación (20 min)
**Nivel:** ⭐⭐

**Datos experimentales:**
```
T₁ = 50°C,  k₁ = 0.01 s⁻¹
T₂ = 60°C,  k₂ = 0.025 s⁻¹
```

**Calcula:**
1. Energía de activación (Eₐ) usando la relación de Arrhenius
2. Factor pre-exponencial (A)
3. Constante k a 70°C y 40°C (extrapolación)

**Luego verifica** comparando con parámetros en `py_alone.py` (A ≈ 1e8, Eₐ ≈ 65 kJ/mol)

### Ejercicio 6.2: Conversión vs Temperatura (25 min)
**Nivel:** ⭐⭐

Para reactor CSTR con:
- τ = 10 minutos
- CA0 = 1 mol/L
- A = 1e8 s⁻¹
- Eₐ = 65 kJ/mol

Calcular conversión en rango 30°C a 80°C (cada 10°C).

**Preguntas:**
1. ¿Hay relación lineal entre T y X?
2. ¿A qué temperatura se dobla la conversión?
3. ¿Cuánto debe cambiar T para aumentar X de 50% a 80%?

### Ejercicio 6.3: Optimización de Reactor (30 min)
**Nivel:** ⭐⭐⭐

Objetivo: Diseñar reactor CSTR para obtener 75% conversión minimizando tiempo de residencia.

**Parámetros fijos:**
- A = 1e8 s⁻¹
- Eₐ = 65 kJ/mol
- Reacción primer orden

**Procedimiento:**
1. Para cada temperatura (30, 40, 50, 60, 70°C), calcular τ requerido para X = 75%
2. Estimar costo (proporcional a V = τ·F, asumiendo F = 1 L/min)
3. ¿Cuál es la temperatura óptima?
4. ¿Hay limitaciones prácticas (materiales, seguridad)?

### Ejercicio 6.4: Reacciones con Diferentes Eₐ (25 min)
**Nivel:** ⭐⭐

Comparar dos reacciones:
```
Reacción A: Eₐ = 30 kJ/mol  (baja activación)
Reacción B: Eₐ = 80 kJ/mol  (alta activación)

Ambas con A = 1e8 s⁻¹
```

**Calcula** conversión a 30°C y 70°C para ambas.

**Análisis:**
1. ¿Cuál es más sensible a temperatura?
2. ¿Cuál prefieres industrialmente?
3. ¿Cómo lo manipularías (catalizador)?

---

## Notas Técnicas

### Ecuación de Arrhenius: Rango de Validez

La ecuación es **válida para:**
- Reacciones elementales
- Temperatura moderada (no cerca de fusión, descomposición)
- Sin cambios de mecanismo

**No es válida para:**
- Reacciones complejas (suma de pasos elementales)
- Reacciones catalizadas (Eₐ cambia con catalizador)
- Temperaturas extremas (cerca de T_crítica, etc.)

### Orden de Reacción

Este ejercicio asume **primer orden**. En realidad:

```
Reacción elemental A → B:
- Si es unimolecular: orden 1
- Si es bimolecular (2A → ...): orden 2 posible
- Si hay catalizador: orden puede ser 0, 1, 1.5, etc.

HYSYS permite especificar orden en definición de reacción
```

### Equilibrio vs Cinética

- **Limitada por cinética (Práctica 6):** k es pequeño, r lenta
- **Limitada por equilibrio (Práctica 6 avanzada):** X_máx limitada por K_eq

A temperatura baja: cinética lenta pero equilibrio favorable
A temperatura alta: cinética rápida pero equilibrio puede ser desfavorable

---

## Referencias

- ASPEN HYSYS: Reactor CSTR con Kinetics-Based Reactions
- Fogler, H.S. "Elements of Chemical Reaction Engineering" (4ta ed.)
- Levenspiel, O. "Chemical Reaction Engineering"
- Matlab/Python para integración ODE: scipy.integrate.odeint

---

**Anterior:** [Práctica 5 - Reactor CSTR Conversión Fija](../practica5/README.md)

**Siguiente:** [Práctica 7 - Batch vs CSTR](../practica7/README.md)
