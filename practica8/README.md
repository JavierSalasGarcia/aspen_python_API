# Práctica 8: Planta Completa de Biodiesel

Simulación integrada de una planta industrial de producción de biodiesel. Combina múltiples operaciones unitarias (Mixer, Reactor, Separador, Lavado, Secado) en un diagrama de flujo completo, con análisis de balance de materia global, rendimiento de producto, pureza y eficiencia energética.

**Dificultad:** ⭐⭐⭐⭐ (Avanzado) | **Duración:** 2-3 horas

---

## Objetivos de Aprendizaje

Al completar esta práctica, serás capaz de:

1. ✅ Construir diagramas de flujo completos en ASPEN HYSYS programáticamente
2. ✅ Conectar múltiples operaciones unitarias en serie
3. ✅ Manejar recirculación de corrientes no reaccionadas
4. ✅ Realizar balance de materia global (entrada = salida)
5. ✅ Optimizar condiciones de operación para máxima pureza y rendimiento
6. ✅ Analizar economía del proceso (rendimiento, pérdidas, eficiencia)

---

## Conceptos Clave

### Flujo Integrado de Materia
En una planta compleja, el balance de materia abarca múltiples unidades:

```
Entrada global = Σ Salida final + Pérdidas
                = Biodiesel + Glicerol + Agua + Impurezas + Efluentes

Rendimiento = (kg Biodiesel puro obtenido) / (kg Triglicérido alimentado)
            = (típicamente 85-95%)
```

### Proceso de Transesterificación
Reacción típica de biodiesel:

```
Triglicérido + 3 Metanol  →(Catalizador)→ 3 Biodiesel (FAME) + Glicerol
     TG            MeOH                        FAME                GL

Condiciones:
- Temperatura: 50-70°C
- Presión: 1-5 atm (baja)
- Catalizador: NaOH, KOH, ácidos, enzimas
- Conversión: 95-99% (reversible, limitada por equilibrio)
```

### Unidades Necesarias

**1. Mixer (Preparación)**
```
Entrada: Aceite + Metanol + Catalizador
Salida: Mezcla homogénea
Objetivo: Mezclar reactivos antes de reactor
```

**2. Reactor CSTR (Transesterificación)**
```
Entrada: Mezcla reactivos
Salida: Productos + Reactivos no convertidos
Objective: Máxima conversión (95-99%)
Control: Temperatura, tiempo residencia
```

**3. Separador/Decantador (Separación de Fases)**
```
Entrada: Productos de reacción (líquido)
Salida: Fase biodiesel (arriba) + Fase glicerol (abajo)
Principio: Diferencia densidad (FAME más ligero)
Pureza inicial: ~99% FAME, ~95% Glicerol
```

**4. Lavador (Remoción de Catalizador)**
```
Entrada: Biodiesel + Glicerol + catalizador
Salida: Biodiesel lavado, Agua de desecho (con catalizador)
Líquido lavado: Agua destilada o diluta
Pureza mejorada: ~99.9% FAME
```

**5. Secador (Remoción de Agua)**
```
Entrada: Biodiesel lavado
Salida: Biodiesel seco
Método: Evaporación al vacío, trampas de agua
Humedad final: <50 ppm
Especificación EN 14214: <500 ppm agua
```

### Balance de Materia Global

Para 1000 kg de triglicérido:

```
ENTRADA:
  Triglicérido: 1000 kg
  Metanol:      ~300 kg (3:1 molar típico)
  Catalizador:  ~1 kg (0.1% wt)
  Total:        ~1301 kg

SALIDA:
  Biodiesel:    ~950 kg (95% conversión, rendimiento 95%)
  Glicerol:     ~105 kg (subproducto)
  Metanol sin reac: ~150 kg (recuperado/reciclado)
  Agua:         ~80 kg (de reacción, secado)
  Pérdidas:     ~16 kg
  Total:        ~1301 kg ✓
```

### Indicadores de Desempeño

```
Rendimiento = (kg biodiesel obtenido) / (kg aceite alimentado)
            = 950 / 1000 = 95%

Pureza biodiesel = (kg FAME puro) / (kg biodiesel total)
                 ≈ 99-99.9%

Recuperación glicerol = (kg glicerol obtenido) / (kg teórico)
                      ≈ 85-90%

Eficiencia energética = Energía en productos / Energía alimentada
                      ≈ 85-95% (sin exceso de calor)
```

---

## Archivos de la Práctica

- **`aspython.py`**: Script completo que construye planta integrada en ASPEN HYSYS con 5 unidades (Mixer → Reactor → Separador → Lavador → Secador), calcula balances de materia, rendimiento final, pureza, eficiencia energética
- **`py_alone.py`**: Cálculos estequiométricos sin HYSYS. Asigna componentes sustitutos, integra balances por unidad, rastrea pureza del biodiesel a través del proceso
- **`visualiza1.py`**: Gráficas Sankey de flujos: muestra entrada de 1000 kg de aceite, rastrea cómo se reparte entre biodiesel, glicerol, pérdidas, agua; análisis de dónde ocurren pérdidas significativas
- **`visualiza2.py`**: Análisis de sensibilidad: cómo varían rendimiento, pureza y economía con parámetros clave (conversión reactor, eficiencia separación, temperatura)

---

## Cómo Usar Esta Práctica

### 1. Construcción Completa de Planta

```bash
python practica8/aspython.py
```

Realiza **secuencialmente:**

#### Paso 1: Iniciar HYSYS y Configurar
```
- ASPEN HYSYS abierto
- 5 componentes: Methanol, Ethanol (aceite), Ethyl acetate (biodiesel), Water, Glycerol
- Paquete termodinámico: NRTL
```

#### Paso 2: Crear Corrientes de Entrada
```
Corriente 1 (Aceite):
  - Etanol puro
  - Flujo: 1000 kg/h
  - T = 25°C, P = 1 atm

Corriente 2 (Metanol):
  - Metanol puro
  - Flujo: 300 kg/h (3:1 molar típico)
  - T = 25°C, P = 1 atm

Corriente 3 (Catalizador):
  - Agua con KOH disuelto (representado como "Water")
  - Flujo: 10 kg/h
  - T = 25°C, P = 1 atm
```

#### Paso 3: Mixer (Mezcla Reactivos)
```
Entradas: Corrientes 1, 2, 3
Salida: Mezcla homogénea
Propósito: Preparar reactivos para reactor
```

#### Paso 4: Reactor CSTR
```
Entrada: Mezcla del Mixer
Configuración:
  - Volumen: 1000 L
  - Conversión especificada: 99% Metanol (reactante limitante)
  - Temperatura: 60°C (óptima para transesterificación)

Reacción: MeOH + Ethanol → Ethyl acetate + Water (1:1:1:1)

Salida: Productos de reacción
```

#### Paso 5: Separador (Decantación)
```
Entrada: Salida reactor (productos mixtos)
Operación: Separación gravimétrica por densidad

Salida 1 (Fase biodiesel):
  - Ethyl acetate principal
  - Composición: ~95% Ethyl acetate, 5% Water/impurezas

Salida 2 (Fase glicerol):
  - Water + Glicerol
  - Composición: ~70% Water, 30% Glicerol
```

#### Paso 6: Lavador (Secuencial, 2-3 etapas)
```
Entrada: Fase biodiesel del separador
Reactivo de lavado: Water destilada (3 etapas a 50°C)
Objetivo: Remover catalizador disuelto

Salida: Biodiesel lavado (pureza ↑ 99.5%)
Efluente: Agua de desecho
```

#### Paso 7: Secador (Deshidratador)
```
Entrada: Biodiesel lavado
Operación: Evaporación al vacío (50°C, 10 mmHg)
Objetivo: Humedad final <50 ppm

Salida: **Biodiesel especificación EN 14214**
```

#### Paso 8: Análisis Global
```
Balance de materia general:
  Entrada total = 1000 + 300 + 10 = 1310 kg/h
  Salida total = ? (debe ser 1310 kg/h)

Rendimiento:
  kg Biodiesel / kg Aceite = ?

Pureza final:
  % Ethyl acetate en Biodiesel = ?

Eficiencia global:
  Basada en masa, energía, economía
```

### 2. Cálculos Integrados Independientes

```bash
python practica8/py_alone.py
```

Sin ASPEN HYSYS:
- Define composición sustitutos y masas molares
- Integra balance de materia por unidad (Mixer → Reactor → Sep → Lavador → Secador)
- Rastrea distribución de cada componente
- Calcula rendimiento global por unidad
- Produce tabla con resultados en cada etapa

### 3. Diagrama Sankey de Flujos

```bash
python practica8/visualiza1.py
```

Genera visualización mostrando:
- **Entrada:** 1000 kg aceite + 300 kg metanol + 10 kg catalizador
- **Flujos por unidad:**
  - Mixer: mezcla homogénea
  - Reactor: conversión de metanol (→ %)
  - Separador: 2 fases (biodiesel vs glicerol)
  - Lavador: pérdidas en agua de lavado
  - Secador: pérdida de agua residual

- **Salida final:**
  - Biodiesel (~950 kg)
  - Glicerol (~100 kg)
  - Pérdidas/Efluentes (~160 kg)

Identifica cuál unidad tiene mayor pérdida de materia prima valiosa.

### 4. Análisis de Sensibilidad Económico

```bash
python practica8/visualiza2.py
```

Varía parámetros clave y calcula impacto:

| Parámetro | Rango | Impacto |
|-----------|-------|--------|
| Conversión reactor | 85%-99% | Rendimiento final |
| Eficiencia separador | 90%-99% | Pérdida biodiesel |
| Temperatura reactor | 50-70°C | Conversión, energía |
| Ciclos lavado | 1-5 | Pureza, agua residual |
| Presión secador | 10-100 mmHg | Tiempo proceso |

Genera gráficas: Rendimiento vs Conversión, Pureza vs Ciclos Lavado, Costo relativo vs Parámetros.

---

## Ejercicios Sugeridos

### Ejercicio 8.1: Balance de Materia Manual Planta Simplificada (30 min)
**Nivel:** ⭐⭐

Suponga planta simplificada (sin lavado, solo Mixer-Reactor-Separador):

**Datos:**
```
Entrada:
  Aceite (sustituto Ethanol): 1000 kg/h, MW = 92 kg/kmol
  Metanol: 300 kg/h, MW = 32 kg/kmol
  Conversión Metanol: 99%

Reacción: MeOH + Aceite → Biodiesel (sustituto Ethyl acetate) + Water
          32 + 92 → 120 + 4 (masas molares aproximadas)

Separador: 99% biodiesel en fase superior, 95% agua/glicerol en fase inferior
```

**Calcula:**
1. Moles de entrada de Metanol y Aceite
2. Moles de reacción (limitante = Metanol)
3. Moles de Biodiesel producido
4. Rendimiento = kg Biodiesel / kg Aceite
5. Destino del Metanol no reaccionado

**Luego verifica** ejecutando `py_alone.py` y comparando resultados.

### Ejercicio 8.2: Impacto de Lavado (25 min)
**Nivel:** ⭐⭐

Modificar `aspython.py` para incluir **ciclos variables de lavado**:
- 1 ciclo: Biodiesel + 300 L agua destilada
- 2 ciclos: Repetir con 150 L agua
- 3 ciclos: Repetir con 100 L agua

**Registrar:**
1. Pureza de biodiesel (% Ethyl acetate) vs ciclos
2. Volumen de agua residual generada
3. Pérdida de biodiesel por arrastre en agua (típicamente 0.1-0.5%)

**Pregunta:** ¿Vale la pena 3 ciclos vs 1? (Análisis costo/beneficio)

### Ejercicio 8.3: Efecto de Temperatura del Reactor (25 min)
**Nivel:** ⭐⭐⭐

Simular reactor a diferentes temperaturas:
```
Casos: 30°C, 40°C, 50°C, 60°C, 70°C

Parámetros cinéticos (Arrhenius):
  A = 5e7 s⁻¹
  Eₐ = 55 kJ/mol
  Conversión se calcula con k(T)
```

**Para cada temperatura calcular:**
1. Constante de velocidad k(T)
2. Conversión alcanzada (considerando τ = 30 min)
3. Energía requerida para calentar
4. Costo relativo (energía vs rendimiento)

**Gráfica:** Conversión vs T. ¿Hay óptimo económico?

### Ejercicio 8.4: Optimización Económica Simulada (40 min)
**Nivel:** ⭐⭐⭐⭐

Objetivo: **Maximizar ganancia = Ingresos - Costos**

**Definir costos aproximados:**
```
Aceite (entrada): $1.50/kg
Metanol: $0.50/kg
Agua de lavado: $0.10/kg
Energía: $0.05/kWh

Ingresos:
Biodiesel: $1.80/kg (mercado)
Glicerol: $1.50/kg (subproducto)

Parámetros a optimizar:
1. Conversión reactor: 85%-99%
2. Temperatura reactor: 40-70°C
3. Ciclos de lavado: 1-3
4. Recuperación metanol: 80%-95% (cantidad reciclada)
```

**Procedimiento:**
1. Para cada combinación de parámetros, simular planta
2. Calcular balance de materia completo
3. Estimar costos operacionales
4. Calcular ingresos por biodiesel y glicerol
5. Ganancia neta = Ingresos - Costos entrada - Costos operación

**Resultado esperado:**
- Conversión óptima: ~95% (no siempre 99%)
- Temperatura óptima: ~60°C (balance cinética-energía)
- Ciclos lavado: 2 (1 es insuficiente, 3 es exceso)

---

## Notas Técnicas

### Selección de Componentes Sustitutos

En ASPEN HYSYS, no están disponibles todos los componentes reales:

| Real | Sustituto HYSYS | Por qué |
|------|-----------------|--------|
| Triglicérido (TG) | Ethanol | Similar MW, solubilidad |
| Biodiesel (FAME) | Ethyl acetate | Similar polarity, Tb, densidad |
| Glicerol (GLY) | Water | Miscibilidad, punto fusión |

**Limitaciones:**
- Propiedades termodinámicas NO son exactamente iguales
- Balance de materia SÍ es correcto (estequiometría no cambia)
- Conclusiones cualitativas válidas, cuantitativas aproximadas

### Recirculación del Metanol

En realidad, el metanol sin reaccionar se recupera:
```
Reactor → Separador → Destilación → Recirculación al Reactor

En HYSYS simple: ignoramos, asumimos pérdida de metanol
En HYSYS avanzado: agregar unidad Distillation con reciclo
```

### Catalizador Disuelto

El catalizador (NaOH/KOH) se asume disuelto en agua:
```
Entra como "catalizador" → Se disuelve en reactor
→ Arrastrado a separador → Removido con agua de lavado

En nuestro modelo simplificado: representado como fracción en "Water"
```

---

## Referencias

- ASPEN HYSYS: Flowsheet Simulation, Recycle Streams
- Gerpen, J.V. "Biodiesel Processing and Production" (Critical Reviews in Environmental Science and Technology)
- Freedman, B. et al. "Variables Affecting the Yields of Fatty Esters from Transesterified Vegetable Oils"
- EN 14214: "Biodiesel (FAME) Standard"
- ASTM D6866: "Biodiesel Specifications"

---

**Anterior:** [Práctica 7 - Batch vs CSTR](../practica7/README.md)

**Fin de Serie:** Prácticas completadas (1-8). Temas avanzados: Destilación, Extracción, Control automático, Optimización económica.
