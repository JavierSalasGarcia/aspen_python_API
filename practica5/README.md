# Práctica 5: Reactor CSTR con Conversión Fija

Reactor continuo de tanque agitado (Continuous Stirred Tank Reactor). Simula una reacción químicamente controlada con conversión fija, aplicada al caso de transesterificación para producción de biodiesel.

**Dificultad:** ⭐⭐⭐ (Avanzado) | **Duración:** 1.5-2 horas

---

## Objetivos de Aprendizaje

Al completar esta práctica, serás capaz de:

1. ✅ Crear reactores CSTR en ASPEN HYSYS desde Python
2. ✅ Definir y especificar reacciones químicas estequiométricamente
3. ✅ Aplicar conversión fija como especificación de reactor
4. ✅ Calcular grado de reacción y rendimiento
5. ✅ Analizar el rol de la estequiometría en balance de materia

---

## Conceptos Clave

### Reactor CSTR
Reactor tipo "tanque agitado" con:
- **Mezcla instantánea:** composición uniforme en todo el volumen
- **Tiempo de residencia:** τ = V/F (volumen/flujo volumétrico)
- **Régimen estacionario:** no hay acumulación
- **Cinética reacción:** puede ser controlada o especificada

```
    Entrada → [Reactor CSTR] → Salida
              (Mezcla rápida)
                Outlet = Inlet - Reacted
```

### Conversión de Reactante Limitante
Definida como:
```
X = (moles reactante inicial - moles reactante final) / moles reactante inicial
```

Rango: 0 ≤ X ≤ 1

### Estequiometría y Extent of Reaction
Relación entre cambios en moles de reactantes y productos:
```
Para reacción: aA + bB → cC + dD

ξ = extensión de reacción (kmol/h)
Δn_A = -a·ξ
Δn_B = -b·ξ
Δn_C = c·ξ
Δn_D = d·ξ
```

### Rendimiento de Producto
```
Rendimiento = (moles producto obtenido) / (moles teóricos máximo)
            = (moles producto real) / (moles si reactante limitante convierte 100%)
```

### Reacción de Transesterificación
Simplifcada para HYSYS con componentes disponibles:
```
CH₃OH + ROH → ROCH₃ + CH₃OH
(Metanol + Triglicérido → Biodiesel + Glicerol)

En HYSYS: Methanol + Ethanol → Ethyl acetate + Water
```

---

## Archivos de la Práctica

- **`aspython.py`**: Script completo que simula reactor CSTR con 4 componentes (Methanol, Ethanol, Ethyl acetate, Water) con conversión fija de 75% en Metanol
- **`py_alone.py`**: Cálculos de balance de materia con estequiometría usando Python puro (manejo de conversión y extent of reaction)
- **`visualiza1.py`**: Gráficas mostrando composición de salida vs conversión especificada (0% a 100%)
- **`visualiza2.py`**: Análisis de rendimiento y selectividad de producto respecto a variación de parámetros de entrada

---

## Cómo Usar Esta Práctica

### 1. Ejecución Completa con ASPEN HYSYS

```bash
python practica5/aspython.py
```

Realiza:
- Configuración de 4 componentes para simular transesterificación
- Creación de corrientes de entrada (Metanol puro, Etanol)
- Creación de reactor CSTR con conversión fija (75% en Metanol)
- Cálculo automático de productos (Ethyl acetate, Water)
- Balance de materia completo verificando conservación
- Cálculo de extent of reaction y rendimiento

### 2. Cálculos de Balance Independientes

```bash
python practica5/py_alone.py
```

Permite verificar cálculos de estequiometría:
- Balance de materia manual
- Cálculo de extent of reaction
- Determinación de reactante limitante
- Rendimiento teórico vs real

### 3. Análisis de Conversión

```bash
python practica5/visualiza1.py
```

Genera series de simulaciones variando conversión de 0% a 100%:
- Gráfica: flujo de salida de cada componente vs conversión
- Gráfica: composición molar de salida vs conversión
- Gráfica: selectividad de producto vs conversión

### 4. Estudio Paramétrico Completo

```bash
python practica5/visualiza2.py
```

Estudia impacto de múltiples parámetros:
- Ratio Metanol:Etanol en entrada
- Rendimiento de producto a diferentes razas molares
- Conversión requerida para máximo rendimiento

---

## Ejercicios Sugeridos

### Ejercicio 5.1: Estequiometría Básica (20 min)
**Nivel:** ⭐⭐

Sin ejecutar HYSYS, calcular manualmente:

**Entrada:**
- Metanol: 100 kmol/h
- Etanol: 50 kmol/h

**Reacción:** CH₃OH + C₂H₅OH → C₂H₅OOCCH₃ + H₂O (1:1:1:1)

**Conversión especificada:** 80% en Metanol

**Calcula:**
1. ¿Cuál es el reactante limitante?
2. Extent of reaction (ξ)
3. Flujos molares de salida de todos los componentes
4. Rendimiento de producto

**Luego verifica** ejecutando `py_alone.py` con estos datos.

### Ejercicio 5.2: Impacto de Conversión (25 min)
**Nivel:** ⭐⭐

Modificar `aspython.py` para simular el reactor con 5 conversiones diferentes:
- 25%, 50%, 75%, 90%, 100%

Para cada caso registrar:
- Flujo de salida de Ethyl acetate (biodiesel)
- Rendimiento de producto
- Temperatura de salida (si es exotérmica/endotérmica)

¿Cuál es la conversión óptima? ¿Por qué no siempre es 100%?

### Ejercicio 5.3: Ratio de Reactantes (30 min)
**Nivel:** ⭐⭐⭐

Modificar para mantener conversión en 75% pero variar ratio Metanol:Etanol:
- 1:1, 2:1, 3:1, 4:1, 5:1

Analizar:
1. ¿Cómo cambia el rendimiento?
2. ¿Hay exceso de Metanol? (típico en transesterificación real)
3. ¿Qué ratio es más rentable?

### Ejercicio 5.4: Selección de Componentes (20 min)
**Nivel:** ⭐

Investigar por qué se usan sustitutos en HYSYS:
```
Real                    Sustituto en HYSYS
─────────────────────────────────────────────
Triglicérido           → Ethanol
Biodiesel (Metil ester) → Ethyl acetate
Glicerol               → Water
```

¿Qué propiedades termodinámicas son similares?
¿Dónde fallaría esta aproximación?

---

## Notas Técnicas

### Conversión Fija vs Cinética Controlada

**Conversión Fija (Este ejercicio):**
- Especificas: "El 75% del reactante se convierte"
- Útil para: estimaciones rápidas, diseño conceptual
- Ventaja: no requiere parámetros cinéticos
- Desventaja: no captura dependencia con temperatura, tiempo

**Cinética Controlada (Práctica 6):**
- Especificas: ecuación de velocidad k=A·exp(-Ea/RT)
- Requiere: parámetros cinéticos (A, Ea)
- Ventaja: más realista, predice efecto temperatura
- Desventaja: más parámetros desconocidos

### Estequiometría en HYSYS

En ASPEN HYSYS, las reacciones se definen como:

```
νᵢ·(Componente_i)

νᵢ > 0: producto
νᵢ < 0: reactante
Σνᵢ·M = cambio en masa molar total
```

**Importante:** HYSYS conserva masa automáticamente. Si especificas conversión, calcula los flujos de productos consistentemente.

### Limitaciones de Conversión Fija

1. **No incluye dependencia térmica:** conversión real varía con T
2. **No modela equilibrio:** reacciones reversibles no capturadas
3. **Asume mezcla perfecta:** en realidad hay gradientes
4. **Tiempo infinito:** asume estado estacionario alcanzado

---

## Referencias

- ASPEN HYSYS: Reactor CSTR con Conversion-Based Reactions
- Levenspiel, O. "Ingeniería de las Reacciones Químicas"
- Fogler, H.S. "Elements of Chemical Reaction Engineering"
- Production de biodiesel: De Bruyn et al. "Biodiesel Production Technology"

---

**Anterior:** [Práctica 4 - Mixer](../practica4/README.md)

**Siguiente:** [Práctica 6 - Cinética de Arrhenius](../practica6/README.md)
