# Práctica 1: Conexión Básica con ASPEN HYSYS

⭐ **Dificultad**: Principiante
⏱️ **Duración**: 30 minutos
🎯 **Objetivo**: Establecer conexión COM entre Python y ASPEN HYSYS

---

## 📚 Conceptos Teóricos

### ¿Qué es COM (Component Object Model)?

COM es una tecnología de Microsoft que permite que diferentes programas se comuniquen entre sí:

```
Python Script
     ↓ (pywin32)
   COM API
     ↓
ASPEN HYSYS
```

### ¿Por qué automatizar HYSYS?

1. **Reproducibilidad**: Scripts ejecutables idénticamente
2. **Rapidez**: Cientos de simulaciones en minutos
3. **Integración**: Combinar HYSYS con análisis de datos
4. **Parametrización**: Estudios de sensibilidad automatizados

---

## 🎯 Objetivos de Aprendizaje

Al completar esta práctica, serás capaz de:

1. ✅ Importar biblioteca `win32com.client` en Python
2. ✅ Iniciar ASPEN HYSYS desde Python
3. ✅ Obtener versión de HYSYS programáticamente
4. ✅ Cerrar HYSYS de forma segura
5. ✅ Manejar errores comunes de conexión

---

## 💻 Código Ejemplo

Ver archivo: `script.py`

**Conceptos clave**:
```python
import win32com.client as win32

# Crear conexión COM
hysys = win32.Dispatch('HYSYS.Application')

# Hacer visible
hysys.Visible = True

# Obtener información
version = hysys.Version

# Cerrar
hysys.Quit()
```

---

## 🔧 Ejercicios Guiados

### Ejercicio 1.1: Conexión Básica (5 min)

**Tarea**: Ejecutar `script.py` sin modificaciones

**Resultado esperado**:
- HYSYS se abre
- Muestra versión en consola
- Se cierra automáticamente

### Ejercicio 1.2: Modo Invisible (5 min)

**Tarea**: Modificar para que HYSYS no se muestre

```python
hysys.Visible = False  # Cambiar True → False
```

**Pregunta**: ¿Cuándo es útil el modo invisible?

### Ejercicio 1.3: Manejo de Errores (10 min)

**Tarea**: Intentar conectar sin tener HYSYS instalado o sin licencia activa

**Analiza el error** y propón soluciones

---

## 🚀 Retos Adicionales

### Reto 1.A: Verificar Licencia (⭐⭐)

Investiga cómo verificar si la licencia de HYSYS está activa antes de ejecutar simulaciones

### Reto 1.B: Múltiples Instancias (⭐⭐⭐)

¿Es posible abrir 2 instancias de HYSYS simultáneamente desde Python?

---

## 📝 Preguntas de Reflexión

1. ¿Qué diferencia hay entre `Dispatch` y `DispatchEx`?
2. ¿Qué pasa si no cierras HYSYS con `Quit()`?
3. ¿Por qué es importante el `try-except` en automatización?

---

## ✅ Criterios de Éxito

- [ ] Script ejecuta sin errores
- [ ] HYSYS abre y cierra correctamente
- [ ] Entiendes concepto de COM API
- [ ] Puedes modificar Visible True/False

---

## ⏭️ Siguiente Paso

**👉 [Práctica 2: Componentes y Paquetes](../practica2/README.md)**
