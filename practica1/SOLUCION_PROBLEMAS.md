# Solución de Problemas - Práctica 1

## Error: "Operación no disponible" (-2147221021)

Este es el error más común al intentar conectar Python con ASPEN HYSYS. Aquí está la guía completa para solucionarlo.

---

## 🔍 Diagnóstico Rápido

Ejecuta el script de diagnóstico incluido:

```bash
python diagnostico_hysys.py
```

Este script verificará automáticamente:
- ✅ Versión de Python y arquitectura
- ✅ Instalación de pywin32
- ✅ Registro de HYSYS en Windows
- ✅ Diferentes métodos de conexión

---

## ❌ Causas Comunes del Error

### 1. **Incompatibilidad de Arquitectura (32-bit vs 64-bit)**

**EL PROBLEMA MÁS COMÚN**

Python y HYSYS deben tener la misma arquitectura:
- Python 64-bit ↔ HYSYS 64-bit ✅
- Python 32-bit ↔ HYSYS 32-bit ✅
- Python 64-bit ↔ HYSYS 32-bit ❌
- Python 32-bit ↔ HYSYS 64-bit ❌

#### Verificar arquitectura de Python:
```bash
python -c "import sys; print('64-bit' if sys.maxsize > 2**32 else '32-bit')"
```

#### Verificar arquitectura de HYSYS:
1. Abre el Administrador de Tareas (Ctrl+Shift+Esc)
2. Ve a la pestaña "Detalles"
3. Busca "hysys.exe"
4. Si dice "(32 bits)" al lado, es 32-bit
5. Si no dice nada, probablemente es 64-bit

#### Solución:
Instala la versión correcta de Python que coincida con tu HYSYS.

---

### 2. **HYSYS no está registrado en el sistema**

HYSYS necesita registrarse en el registro de Windows la primera vez que se ejecuta.

#### Solución:
1. **Ejecuta HYSYS como administrador**
   - Clic derecho en el icono de HYSYS
   - "Ejecutar como administrador"
   - Cierra HYSYS normalmente

2. **Prueba el script de nuevo**

---

### 3. **HYSYS no está instalado o está mal instalado**

#### Verificación:
- ¿Puedes abrir HYSYS manualmente?
- ¿Aparece HYSYS en tus programas instalados?

#### Solución:
1. Repara la instalación desde "Programas y características"
2. O reinstala HYSYS completamente
3. Asegúrate de ejecutarlo al menos una vez como administrador

---

### 4. **Problema con pywin32**

#### Solución:
```bash
# Desinstalar pywin32
pip uninstall pywin32

# Reinstalar
pip install pywin32

# Ejecutar post-instalación
python -m win32com.client.makepy
```

---

### 5. **No hay licencia activa de HYSYS**

HYSYS necesita una licencia válida para funcionar.

#### Verificación:
1. Abre HYSYS manualmente
2. Si ves un mensaje de licencia, ese es el problema
3. Contacta a tu administrador de licencias

---

## 🔧 Soluciones Paso a Paso

### Solución 1: Método Completo (RECOMENDADO)

Sigue estos pasos en orden:

#### Paso 1: Verificar instalación básica
```bash
# Verificar Python
python --version
python -c "import sys; print('64-bit' if sys.maxsize > 2**32 else '32-bit')"

# Verificar pywin32
python -c "import win32com.client; print('pywin32 OK')"
```

#### Paso 2: Ejecutar diagnóstico
```bash
python diagnostico_hysys.py
```

#### Paso 3: Aplicar solución según diagnóstico
Lee el resultado del diagnóstico y aplica la solución correspondiente.

---

### Solución 2: Método Alternativo (TEMPORAL)

Si no puedes solucionar el problema principal, usa este método temporal:

#### Paso 1: Abre HYSYS manualmente
- Inicia ASPEN HYSYS normalmente desde Windows

#### Paso 2: Ejecuta el script alternativo
```bash
python aspython_activeobject.py
```

Este script se conecta a HYSYS que ya está abierto en lugar de intentar abrirlo.

**Ventajas:**
- ✅ Funciona incluso si `Dispatch()` falla
- ✅ Útil para aprender y debugging

**Desventajas:**
- ❌ No es automático
- ❌ Tienes que abrir HYSYS manualmente cada vez

---

## 📋 Checklist de Solución

Marca cada paso conforme lo completes:

- [ ] Verificar que HYSYS está instalado y funciona manualmente
- [ ] Verificar compatibilidad de arquitectura (Python y HYSYS deben coincidir)
- [ ] Ejecutar HYSYS como administrador al menos una vez
- [ ] Reinstalar pywin32
- [ ] Ejecutar `python diagnostico_hysys.py`
- [ ] Si todo falla, usar `aspython_activeobject.py` como alternativa temporal

---

## 🆘 Soluciones Específicas por Código de Error

### Error -2147221021: "Operación no disponible"
- **Causa:** HYSYS no está registrado
- **Solución:** Ejecutar HYSYS como administrador

### Error -2147221005: "Clase no registrada"
- **Causa:** Instalación corrupta de HYSYS
- **Solución:** Reparar o reinstalar HYSYS

### Error -2147352567: "Error de excepción"
- **Causa:** HYSYS se abrió pero falló internamente
- **Solución:** Verificar licencia, cerrar otras instancias de HYSYS

---

## 💡 Preguntas Frecuentes

### P: ¿Por qué funciona HYSYS manualmente pero no desde Python?
**R:** Probablemente es un problema de arquitectura (32/64-bit) o de registro COM.

### P: ¿Necesito ser administrador para ejecutar el script?
**R:** No necesariamente, pero HYSYS debe haberse ejecutado como administrador al menos una vez.

### P: ¿Puedo usar versiones antiguas de HYSYS?
**R:** Sí, pero el ProgID podría ser diferente. Prueba 'Hysys.Application' en lugar de 'HYSYS.Application'.

### P: ¿Funciona con Aspen Plus?
**R:** No, este código es específico para HYSYS. Aspen Plus usa 'Apwn.Document'.

---

## 📞 Ayuda Adicional

Si ninguna solución funciona:

1. **Revisa el archivo de log completo del error**
   - Copia TODO el mensaje de error
   - Busca el código numérico del error

2. **Información del sistema**
   - Versión de Windows
   - Versión de HYSYS
   - Versión de Python
   - Arquitectura de ambos (32/64-bit)

3. **Consulta con tu administrador de sistemas**
   - Puede haber políticas de seguridad que bloqueen COM
   - Puede necesitar permisos especiales

---

## ✅ Verificación Final

Cuando todo funcione, deberías ver:

```
============================================================
PRÁCTICA 1: CONEXIÓN BÁSICA CON ASPEN HYSYS
============================================================

[1/4] Iniciando ASPEN HYSYS...
   ✓ HYSYS iniciado correctamente

[2/4] Obteniendo información del sistema...
   ✓ HYSYS Versión: 14.0

[3/4] HYSYS está abierto. Observa la ventana...
   ⏳ Esperando 3 segundos...

[4/4] Cerrando ASPEN HYSYS...
   ✓ HYSYS cerrado correctamente
```

Si ves esto, ¡felicidades! La conexión funciona correctamente.

---

## 🎯 Próximos Pasos

Una vez que soluciones el problema:

1. **Ejecuta aspython.py exitosamente**
2. **Continúa con Práctica 2: Componentes**
3. **Explora las demás prácticas**

---

**Última actualización:** 2025-01-15
**Autor:** Salas-García, et. al
