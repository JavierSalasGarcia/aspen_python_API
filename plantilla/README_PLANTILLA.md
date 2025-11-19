# Plantilla para Artículos Científicos - Informaticae Abstracta

Esta plantilla está basada en la clase `syx7.cls` para la revista Informaticae Abstracta y proporciona una estructura completa para la elaboración de artículos científicos.

## 📋 Requisitos

Para utilizar esta plantilla necesita tener instalado:

- **XeLaTeX** (recomendado) o **LaTeX**
- **BibTeX** para las referencias bibliográficas
- Los siguientes paquetes LaTeX:
  - amsmath, amsthm, amssymb
  - graphicx, caption, subcaption
  - tikz, pgfplots
  - algorithm2e
  - biblatex
  - fontspec, unicode-math (para XeLaTeX)
  - babel (español)

## 📁 Estructura de Archivos

```
plantilla/
├── syx7.cls                    # Clase del documento (NO MODIFICAR)
├── template.tex                # Plantilla principal (ARCHIVO PRINCIPAL)
├── biblio_template.bib         # Archivo de bibliografía de ejemplo
├── biblio.bib                  # Su archivo de bibliografía
├── fuentes/
│   └── logoia-3.eps           # Logo de la revista (REQUERIDO)
└── img/                        # Carpeta para sus imágenes
```

## 🚀 Uso Rápido

### 1. Compilación

Para compilar el documento, ejecute los siguientes comandos en orden:

```bash
xelatex template.tex
bibtex template
xelatex template.tex
xelatex template.tex
```

**Nota:** Es necesario ejecutar `xelatex` tres veces para que se resuelvan correctamente todas las referencias cruzadas y la bibliografía.

### 2. Personalización Básica

Edite las siguientes secciones en `template.tex`:

#### Metadatos del Documento

```latex
\receiveddate{01-ene-2024}      % Fecha de recepción
\accepteddate{01-dic-2024}       % Fecha de aceptación
\title{Título de su artículo}   % Título completo
\shorttitle{Título corto}        % Título para el encabezado
\keywords{palabra1, palabra2}    % Palabras clave
```

#### Autores

```latex
\author{Nombre del Autor}
\email{correo@institucion.edu}
```

Puede agregar tantos autores como necesite repitiendo estos comandos.

#### Resumen

```latex
\begin{abstract}
    Escriba aquí su resumen (150-250 palabras)
\end{abstract}
```

## 📝 Elementos del Documento

### Secciones

```latex
\section{Nombre de la Sección}
\subsection{Nombre de la Subsección}
```

### Figuras

```latex
\begin{figure}[htb!]
    \centering
    \includegraphics[width=0.5\textwidth]{img/nombre_imagen.png}
    \caption{Descripción de la figura}
    \label{fig:etiqueta}
\end{figure}
```

Para referenciar: `ver Figura \ref{fig:etiqueta}`

### Tablas

```latex
\begin{table}[htb!]
    \caption{Título de la tabla}
    \label{tab:etiqueta}
    \centering
    \begin{tabular}{cc}
        \toprule
        Columna 1 & Columna 2 \\
        \midrule
        Dato 1 & Dato 2 \\
        \bottomrule
    \end{tabular}
\end{table}
```

Para referenciar: `ver Tabla \ref{tab:etiqueta}`

### Ecuaciones

```latex
\begin{equation}
    E = mc^2
    \label{eq:etiqueta}
\end{equation}
```

Para referenciar: `ver Ecuación \ref{eq:etiqueta}`

### Gráficos con TikZ

```latex
\begin{figure}[htb!]
    \centering
    \begin{tikzpicture}
        \draw (0,0) -- (2,2);
    \end{tikzpicture}
    \caption{Gráfico con TikZ}
    \label{fig:tikz}
\end{figure}
```

### Algoritmos

```latex
\begin{algorithm}[htb!]
    \SetAlgoLined
    \KwIn{Entrada del algoritmo}
    \KwOut{Salida del algoritmo}
    instrucción 1\;
    instrucción 2\;
    \caption{Nombre del algoritmo}
    \label{alg:etiqueta}
\end{algorithm}
```

## 📚 Gestión de Referencias Bibliográficas

### 1. Crear el archivo de bibliografía

Edite `biblio.bib` o renombre `biblio_template.bib` a `biblio.bib` y agregue sus referencias.

Ejemplo de entrada:

```bibtex
@article{clave_unica,
  title={Título del Artículo},
  author={Apellido, Nombre},
  journal={Nombre de la Revista},
  year={2024}
}
```

### 2. Citar en el documento

Use `\cite{clave_unica}` para citar la referencia en el texto.

Ejemplos:
- `según \cite{autor2024}` → según [1]
- `varios estudios \cite{autor1,autor2,autor3}` → varios estudios [1-3]

### 3. Tipos de referencias comunes

Consulte `biblio_template.bib` para ver ejemplos de:
- Artículos de revista (`@article`)
- Libros (`@book`)
- Conferencias (`@inproceedings`)
- Sitios web (`@online`)
- Tesis (`@phdthesis`)
- Reportes técnicos (`@techreport`)

## 🎨 Características del Formato

### Fuentes
- La plantilla utiliza **Latin Modern** como fuente principal
- Se requiere compilar con **XeLaTeX** para soporte completo de fuentes

### Geometría de Página
- Papel: A4
- Márgenes: 25mm (izq/sup), 20mm (der/inf)

### Idioma
- Configurado para **español**
- Soporte completo de acentos y caracteres especiales

## ⚠️ Solución de Problemas

### Error: "File not found"
- Verifique que el archivo `syx7.cls` esté en la misma carpeta que `template.tex`
- Verifique que exista la carpeta `fuentes/` con el logo `logoia-3.eps`

### Error: "Undefined references"
- Ejecute la secuencia completa de compilación (xelatex → bibtex → xelatex → xelatex)

### Error: "Bibliography empty"
- Verifique que el archivo `biblio.bib` exista
- Verifique que haya citado al menos una referencia con `\cite{}`
- Ejecute `bibtex template` después de la primera compilación

### Warnings de fuentes
- Asegúrese de compilar con XeLaTeX
- Si usa otro compilador, comente las líneas de `fontspec` y `unicode-math`

## 📖 Ejemplo Completo

El archivo `Artx.tex` contiene un ejemplo completo de un artículo científico utilizando esta plantilla. Puede consultarlo como referencia para:

- Estructuración de contenido
- Uso de figuras y tablas
- Gráficos con TikZ
- Referencias bibliográficas
- Ecuaciones matemáticas

## 📞 Soporte

Para reportar problemas o sugerir mejoras, consulte la documentación de la revista Informaticae Abstracta o contacte con los editores.

## 📄 Licencia

Esta plantilla se proporciona para uso académico y de investigación. Los derechos del formato pertenecen a Informaticae Abstracta.

---

**Versión:** 1.0
**Fecha:** Noviembre 2024
**Basado en:** syx7.cls v3.8
