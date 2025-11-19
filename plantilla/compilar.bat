@echo off
REM ============================================================================
REM Script de compilacion para documentos LaTeX con XeLaTeX y BibTeX
REM ============================================================================

echo ====================================
echo Compilacion de documento LaTeX
echo ====================================
echo.

REM Verificar si se proporciono un archivo como argumento
if "%1"=="" (
    echo Error: Debe proporcionar el nombre del archivo .tex
    echo Uso: compilar.bat nombre_archivo
    echo Ejemplo: compilar.bat template
    echo.
    pause
    exit /b 1
)

set ARCHIVO=%1

echo [1/5] Primera compilacion con XeLaTeX...
xelatex -interaction=nonstopmode %ARCHIVO%.tex
if errorlevel 1 (
    echo Error en la primera compilacion
    pause
    exit /b 1
)

echo.
echo [2/5] Procesando bibliografia con BibTeX...
bibtex %ARCHIVO%
if errorlevel 1 (
    echo Advertencia: BibTeX reporto errores
)

echo.
echo [3/5] Segunda compilacion con XeLaTeX...
xelatex -interaction=nonstopmode %ARCHIVO%.tex
if errorlevel 1 (
    echo Error en la segunda compilacion
    pause
    exit /b 1
)

echo.
echo [4/5] Tercera compilacion con XeLaTeX (final)...
xelatex -interaction=nonstopmode %ARCHIVO%.tex
if errorlevel 1 (
    echo Error en la tercera compilacion
    pause
    exit /b 1
)

echo.
echo [5/5] Limpiando archivos temporales...
del %ARCHIVO%.aux 2>nul
del %ARCHIVO%.log 2>nul
del %ARCHIVO%.out 2>nul
del %ARCHIVO%.bbl 2>nul
del %ARCHIVO%.blg 2>nul
del %ARCHIVO%.toc 2>nul
del %ARCHIVO%.run.xml 2>nul
del %ARCHIVO%-blx.bib 2>nul
del %ARCHIVO%.bcf 2>nul

echo.
echo ====================================
echo Compilacion completada exitosamente
echo Archivo generado: %ARCHIVO%.pdf
echo ====================================
echo.

REM Abrir el PDF si existe
if exist %ARCHIVO%.pdf (
    echo Abriendo el PDF...
    start %ARCHIVO%.pdf
)

pause
