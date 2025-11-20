# Tutorial Progresivo: ASPEN HYSYS + Python

Tutorial pedagógico con 8 prácticas progresivas para aprender automatización de ASPEN HYSYS con Python. Incluye comparación sistemática entre automatización de ASPEN y cálculos con Python puro.

**Autor:** Salas-García, et. al
**Versión:** 2.0 | **Fecha:** 2025-01-15

## 🎯 Objetivo

Enseñar a estudiantes de posgrado e ingenieros químicos cómo integrar ASPEN HYSYS con Python mediante COM API, con aplicación en producción de biodiesel. El tutorial compara dos enfoques: automatización de ASPEN y cálculos termodinámicos puros en Python.

## 📋 Estructura de Prácticas

| Práctica | Tema | Duración | Dificultad | Estado |
|----------|------|----------|------------|--------|
| **1** | Conexión básica con HYSYS | 30 min | ⭐ | ✅ Completa |
| **2** | Componentes y paquetes termodinámicos | 45 min | ⭐ | ✅ Completa |
| **3** | Corrientes de materia y energía | 1 hora | ⭐⭐ | ✅ Completa |
| **4** | Operación unitaria: Mixer | 1 hora | ⭐⭐ | ✅ Completa |
| **5** | Reactor CSTR (conversión fija) | 1.5 horas | ⭐⭐⭐ | ✅ Completa |
| **6** | Reactor con cinética de Arrhenius | 2 horas | ⭐⭐⭐⭐ | ✅ Completa |
| **7** | Reactores Batch vs Continuos | 2 horas | ⭐⭐⭐⭐ | ✅ Completa |
| **8** | Planta completa de biodiesel | 3 horas | ⭐⭐⭐⭐⭐ | ✅ Completa |

**Total**: ~10.5 horas

## 📁 Estructura de Archivos

Cada práctica contiene 4 archivos:

- **`aspython.py`**: Automatización de ASPEN HYSYS mediante Python y COM API
- **`py_alone.py`**: Cálculos equivalentes usando solo Python (thermo, chemicals, CoolProp)
- **`visualiza1.py`**: Visualización de resultados de ASPEN
- **`visualiza2.py`**: Comparación Python puro vs ASPEN

Además, cada práctica incluye:
- **`README.md`**: Teoría, objetivos, conceptos clave y ejercicios

## 🚀 Inicio Rápido

### Instalación de Dependencias

#### Opción 1: Instalación con Miniconda (Recomendado)

**Paso 1: Instalar Miniconda**

Descargar e instalar Miniconda desde: https://docs.conda.io/en/latest/miniconda.html

- **Windows**: Descargar y ejecutar `Miniconda3-latest-Windows-x86_64.exe`
- **Linux**: `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh`
- **macOS**: `curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh && bash Miniconda3-latest-MacOSX-x86_64.sh`

**Paso 2: Crear y activar entorno virtual**

```bash
# Crear entorno con Python 3.10
conda create -n entornoAsPy python=3.10 -y

# Activar entorno
conda activate entornoAsPy
```

**Paso 3: Instalar dependencias desde requirements.txt**

```bash
# Navegar al directorio del repositorio
cd aspen_python_API

# Instalar todas las dependencias
pip install -r requirements.txt
```

**Paso 4: Verificar instalación**

```bash
# Verificar librerías de termodinámica
python -c "import thermo; import chemicals; import CoolProp; print('Librerías instaladas correctamente')"

# Verificar COM API (solo Windows)
python -c "import win32com.client; print('COM API disponible')"
```

#### Opción 2: Instalación manual (sin entorno virtual)

```bash
# Instalar librerías requeridas
pip install pywin32 numpy scipy matplotlib pandas
pip install thermo chemicals CoolProp
```

### Ejecutar una Práctica

```bash
# Navegar a la práctica
cd practica1

# Ejecutar automatización de ASPEN
python aspython.py

# Ejecutar cálculo con Python puro
python py_alone.py

# Generar visualizaciones
python visualiza1.py  # Resultados de ASPEN
python visualiza2.py  # Comparación Python vs ASPEN
```

## 📖 Requisitos

### Software
- **Python 3.7+**
- **ASPEN HYSYS v10+** (para aspython.py)
- **Windows** (requerido por COM API)

### Librerías Python
- `pywin32`: Interfaz COM para Windows
- `numpy`, `scipy`: Cálculos numéricos
- `matplotlib`: Visualización
- `pandas`: Manejo de datos
- `thermo`: Propiedades termodinámicas
- `chemicals`: Base de datos de componentes químicos
- `CoolProp`: Ecuaciones de estado de precisión

## 🎓 Progresión Pedagógica

### Etapa 1: Fundamentos (Prácticas 1-3)
Establecer comunicación Python-HYSYS, configurar termodinámica, crear corrientes.

### Etapa 2: Operaciones Unitarias (Prácticas 4-5)
Mezcladores, reactores con conversión fija, balances de materia.

### Etapa 3: Modelado Avanzado (Prácticas 6-7)
Cinética de Arrhenius, comparación batch vs continuo, optimización.

### Etapa 4: Integración (Práctica 8)
Planta completa de biodiesel con múltiples operaciones unitarias.

## 📄 Artículo Científico

El repositorio incluye un artículo científico en LaTeX en la carpeta `plantilla/`:

- **`articulo_aspen_python.tex`**: Artículo completo sobre la metodología
- **`biblio.bib`**: Referencias bibliográficas

Para compilar el artículo:

```bash
cd plantilla
xelatex articulo_aspen_python.tex
bibtex articulo_aspen_python
xelatex articulo_aspen_python.tex
xelatex articulo_aspen_python.tex
```

El artículo describe la metodología, compara enfoques, presenta resultados de validación y discute aplicaciones en optimización de procesos.

## 💡 Conceptos Clave Cubiertos

- Integración Python-ASPEN mediante COM API
- Modelos termodinámicos (NRTL, UNIFAC, Peng-Robinson)
- Balances de materia y energía
- Cinética química y ecuación de Arrhenius
- Diseño de reactores (batch, CSTR)
- Optimización de procesos
- Análisis de sensibilidad paramétrica
- Producción de biodiesel por transesterificación

## 🔬 Comparación: Python Puro vs ASPEN

| Aspecto | Python Puro | ASPEN HYSYS |
|---------|-------------|-------------|
| **Precisión** | Alta para componentes puros | Muy alta para mezclas |
| **Velocidad** | Rápida | Media (lanzar HYSYS) |
| **Equipos** | Limitado (balances simples) | Completo (columnas, etc.) |
| **Costo** | Gratuito (código abierto) | Licencia comercial |
| **Plataforma** | Multiplataforma | Solo Windows |
| **Uso recomendado** | Prototipos, cálculos rápidos | Diseño riguroso, validación industrial |

## 🔗 Recursos Adicionales

- **Proyecto Relacionado**: `mod_esterificacion` (sistema completo de modelado)
- **Documentación de librerías**:
  - [thermo](https://github.com/CalebBell/thermo)
  - [chemicals](https://github.com/CalebBell/chemicals)
  - [CoolProp](http://www.coolprop.org/)

## 🤝 Contribuciones

Este repositorio está diseñado como recurso educativo abierto. Se aceptan contribuciones mediante pull requests.

## 📧 Contacto

**Javier Salas-García**
Email: jsalas@institucion.edu

---

*Tutorial diseñado para cursos de posgrado, investigación y autoaprendizaje en ingeniería química*
