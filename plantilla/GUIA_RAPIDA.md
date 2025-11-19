# 🚀 Guía Rápida - Plantilla Informaticae Abstracta

## ⚡ Inicio Rápido (5 minutos)

### 1. Copie los archivos necesarios
```
✓ syx7.cls
✓ template.tex
✓ biblio.bib (o biblio_template.bib)
✓ fuentes/logoia-3.eps
```

### 2. Compile el documento

**Opción A: Usando el script (Windows)**
```bash
compilar.bat template
```

**Opción B: Comandos manuales**
```bash
xelatex template.tex
bibtex template
xelatex template.tex
xelatex template.tex
```

### 3. Edite template.tex con su contenido

---

## 📝 Checklist de Personalización

### ✅ Metadatos Obligatorios
- [ ] Título del artículo (`\title{}`)
- [ ] Título corto (`\shorttitle{}`)
- [ ] Autores y correos (`\author{}` + `\email{}`)
- [ ] Palabras clave (`\keywords{}`)
- [ ] Fechas (`\receiveddate{}` y `\accepteddate{}`)

### ✅ Contenido
- [ ] Resumen (`\begin{abstract}...\end{abstract}`)
- [ ] Introducción
- [ ] Desarrollo (secciones principales)
- [ ] Resultados
- [ ] Conclusiones

### ✅ Referencias
- [ ] Archivo biblio.bib configurado
- [ ] Referencias citadas en el texto con `\cite{}`

---

## 🔧 Soluciones Rápidas

### ❌ "File not found: syx7.cls"
**Solución:** Copie `syx7.cls` a la misma carpeta que su documento `.tex`

### ❌ "File not found: logoia-3.eps"
**Solución:** Cree la carpeta `fuentes/` y copie el logo allí

### ❌ "Undefined references"
**Solución:** Ejecute la secuencia completa de compilación (3 veces xelatex + 1 vez bibtex)

### ❌ "Empty bibliography"
**Solución:**
1. Verifique que `biblio.bib` existe
2. Agregue al menos una cita con `\cite{}` en el texto
3. Recompile

---

## 📦 Estructura Mínima de Archivos

```
mi_articulo/
├── syx7.cls           ← Clase (obligatorio)
├── mi_articulo.tex    ← Su documento
├── biblio.bib         ← Sus referencias
└── fuentes/
    └── logoia-3.eps   ← Logo (obligatorio)
```

---

## 🎯 Elementos Más Usados

### Figura
```latex
\begin{figure}[htb!]
    \centering
    \includegraphics[width=0.5\textwidth]{img/figura.png}
    \caption{Descripción}
    \label{fig:mi_figura}
\end{figure}
```

### Tabla
```latex
\begin{table}[htb!]
    \caption{Mi tabla}
    \label{tab:mi_tabla}
    \centering
    \begin{tabular}{cc}
        \toprule
        Col1 & Col2 \\
        \midrule
        A & B \\
        \bottomrule
    \end{tabular}
\end{table}
```

### Ecuación
```latex
\begin{equation}
    y = mx + b
    \label{eq:linea}
\end{equation}
```

### Cita
```latex
Según \cite{autor2024}, ...
```

### Referencias cruzadas
```latex
ver Figura \ref{fig:mi_figura}
ver Tabla \ref{tab:mi_tabla}
ver Ecuación \ref{eq:linea}
```

---

## 💡 Tips

1. **Compile 3 veces** después de agregar referencias o citas
2. **Use etiquetas descriptivas**: `fig:motor`, `tab:resultados`, `eq:energia`
3. **Guarde imágenes en** `img/` para mantener orden
4. **Cite antes de compilar** bibtex, o la bibliografía estará vacía
5. **Use UTF-8** como codificación del archivo

---

## 📞 ¿Necesita ayuda?

1. Revise [README_PLANTILLA.md](README_PLANTILLA.md) para documentación completa
2. Consulte [Artx.tex](Artx.tex) como ejemplo de uso
3. Verifique que tiene instalado XeLaTeX y BibTeX

---

**¡Listo para comenzar!** Abra `template.tex` y empiece a escribir su artículo.
