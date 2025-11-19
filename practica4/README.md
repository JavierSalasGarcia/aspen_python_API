# Práctica 4: Operación Unitaria - Mixer

Operación unitaria fundamental en procesos químicos. Un mezclador (mixer) combina dos o más corrientes de entrada en una única corriente de salida, realizando balance de materia y calculando propiedades de la mezcla resultante.

**Dificultad:** ⭐⭐ (Intermedio) | **Duración:** 1 hora

---

## Objetivos de Aprendizaje

Al completar esta práctica, serás capaz de:

1. ✅ Crear operaciones unitarias Mixer en ASPEN HYSYS desde Python
2. ✅ Conectar corrientes de entrada y salida en una unidad
3. ✅ Entender balance de materia en mezcladores ideales
4. ✅ Calcular propiedades de mezcla (densidad, entalpía, etc.)
5. ✅ Realizar estudios paramétricos variando flujos de entrada

---

## Conceptos Clave

### Mixer (Mezclador)
Operación unitaria que combina dos o más corrientes sin reaccionar. Balance de materia en estado estacionario:
```
Flujo de salida = Σ (Flujos de entrada)
Composición de salida = Σ (Fracciones molares ponderadas)
```

### Balance de Materia
Principio fundamental de conservación:
```
Entrada = Salida + Acumulación (en estado estacionario, Acumulación = 0)
```

### Propiedades de Mezcla
El paquete termodinámico calcula automáticamente:
- Densidad: promedio ponderado con correcciones no-ideales
- Entalpía: función de composición y temperatura
- Viscosidad: efectos de mezcla complejos

### Grados de Libertad en Mixer
Variables requeridas para definir completamente una operación:
```
Flujos y composiciones de entrada (conocidos)
→ Presión de salida (típicamente = Presión de entrada)
→ Propiedades de salida calculadas automáticamente
```

---

## Archivos de la Práctica

- **`aspython.py`**: Script completo que crea un mixer en ASPEN HYSYS combinando dos corrientes (Metanol puro y agua pura) con balance de materia automático
- **`py_alone.py`**: Implementación sin COM que calcula balance de materia del mixer usando Python puro (sin HYSYS)
- **`visualiza1.py`**: Gráficas de propiedades de la mezcla (densidad, viscosidad) vs composición
- **`visualiza2.py`**: Análisis de sensibilidad: cómo varían propiedades con relaciones de flujo de entrada

---

## Cómo Usar Esta Práctica

### 1. Ejecución Básica

```bash
python practica4/aspython.py
```

Este script:
- Abre ASPEN HYSYS
- Configura componentes (Metanol y Agua)
- Crea dos corrientes de entrada (Metanol puro, Agua pura)
- Crea operación Mixer
- Calcula propiedades de la mezcla
- Realiza balance de materia verificando conservación

### 2. Análisis sin HYSYS

```bash
python practica4/py_alone.py
```

Útil para verificar cálculos de balance de materia con herramientas externas (numpy, pandas).

### 3. Visualización de Propiedades

```bash
python practica4/visualiza1.py
```

Genera gráficas mostrando cómo cambian las propiedades termodinámicas de la mezcla (densidad, entalpía, viscosidad) en función de la composición.

### 4. Análisis de Sensibilidad

```bash
python practica4/visualiza2.py
```

Estudia cómo varían las propiedades de salida del mixer en función de los flujos de entrada.

---

## Ejercicios Sugeridos

### Ejercicio 4.1: Mixer Básico (15 min)
**Nivel:** ⭐

Ejecutar `aspython.py` sin modificaciones y verificar:
- Que el balance de materia se cumple (suma de entradas = salida)
- Que la composición de salida es promedio ponderado de entradas
- Que la temperatura de salida es cercana al promedio

**Pregunta de reflexión:** ¿Por qué la densidad de la mezcla no es simplemente el promedio de las densidades?

### Ejercicio 4.2: Variación de Composición (20 min)
**Nivel:** ⭐⭐

Modificar el script para crear 5 casos:
1. 100% Metanol, 0% Agua
2. 75% Metanol, 25% Agua
3. 50% Metanol, 50% Agua
4. 25% Metanol, 75% Agua
5. 0% Metanol, 100% Agua

Registrar densidad y entalpía de cada caso. ¿Hay cambios no-lineales?

### Ejercicio 4.3: Múltiples Entradas (30 min)
**Nivel:** ⭐⭐⭐

Modificar el mixer para combinar 3 corrientes:
1. Metanol puro (50 kmol/h)
2. Agua pura (30 kmol/h)
3. Mezcla 50/50 (20 kmol/h)

Calcular composición resultante manualmente y comparar con HYSYS.

### Ejercicio 4.4: Impacto de Presión (25 min)
**Nivel:** ⭐⭐

Variar la presión de entrada (101 kPa, 500 kPa, 1000 kPa) y observar efecto en propiedades de salida. ¿Cuáles propiedades cambian significativamente?

---

## Notas Técnicas

### Consideraciones Importantes

1. **Mixer Ideal vs Real**
   - Mixer en HYSYS asume operación ideal sin caídas de presión
   - En realidad, hay fricciones y pérdidas de energía
   - Para casos complejos, usar operación "Mixer" específica

2. **Conservación de Energía**
   - En mixer ideal: ΔH_salida = Σ(F_i * h_i) / F_total
   - HYSYS calcula automáticamente balances de energía
   - Temperatura de salida = f(composición, temperaturas entrada, Cp)

3. **Limitaciones**
   - Mixer asume mezcla instantánea y homogénea
   - No modela fenómenos de separación de fases parciales
   - Requiere paquete termodinámico consistente

4. **Selección de Paquete Termodinámico**
   - **NRTL**: Bueno para líquidos polares (metanol-agua)
   - **UNIFAC**: Predicción para compuestos sin parámetros
   - **SRK/PR**: Mejor para gases y compuestos apolares

---

## Referencias

- ASPEN HYSYS: Modelo de Mixer en documentación oficial
- Smith, Van Ness, Abbott. "Introducción a la Termodinámica en Ingeniería Química"
- Perry & Green. "Chemical Engineers' Handbook" - Sección de operaciones unitarias

---

**Anterior:** [Práctica 3 - Corrientes](../practica3/README.md)

**Siguiente:** [Práctica 5 - Reactor CSTR](../practica5/README.md)
