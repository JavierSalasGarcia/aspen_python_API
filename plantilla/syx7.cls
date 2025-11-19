\NeedsTeXFormat{LaTeX2e}[1999/12/01]
\ProvidesClass{syx7}[2024/03/23 v3.8 Syntaxis Abstracta Journal Class for LaTeX]
% Carga la clase base
\LoadClass[a4paper,12pt,oneside,onecolumn,final]{memoir}
\AtEndOfClass{%
	\let\openbox\relax
	\let\endopenbox\relax
}

% Paquetes necesarios
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[spanish]{babel}
\selectlanguage{spanish}
\RequirePackage{newpxtext,eulerpx}
\RequirePackage{amsthm}
\RequirePackage{amsmath}
\RequirePackage{xcolor}
\RequirePackage{graphicx}




\RequirePackage{hyperref}
\RequirePackage{ragged2e}
\RequirePackage[normalem]{ulem}

\RequirePackage[
a4paper,
left=2.5cm,
right=2.5cm,
top=2.5cm,
bottom=2.5cm,
headheight=15pt,
includeheadfoot,
heightrounded,
% showframe  % Puedes quitar esta línea después, es solo para ver los márgenes
]{geometry}




\setlength{\footskip}{1cm}

\RequirePackage{tikz}

\RequirePackage{pgfplots}
\pgfplotsset{compat=newest}


\RequirePackage{calc}
\RequirePackage{thmtools}
\RequirePackage{abstract}
\RequirePackage{varwidth}
% JSG \RequirePackage{authblk}
\RequirePackage{fancyhdr}
\RequirePackage{csquotes}
\RequirePackage{caption}
\RequirePackage{subcaption}

\RequirePackage{float}
\RequirePackage{etoolbox}
\RequirePackage[ruled,vlined]{algorithm2e}
\RequirePackage{atbegshi}
\RequirePackage{lastpage}
\RequirePackage{refcount}
\RequirePackage{multicol}
\RequirePackage{hyphenat}

% Configuración de colores
\definecolor{light-gray}{gray}{0.95}
\definecolor{pythonblue}{RGB}{0,0,255}
\definecolor{pythongreen}{RGB}{0,128,0}
\definecolor{pythonpurple}{RGB}{128,0,128}

% Configuración del documento
\linespread{1.069}
% \setlength\textwidth{432pt}
\setlength\oddsidemargin{18pt}
\setlength\evensidemargin{18pt}

% Configuración de notas al pie
\renewcommand\@makefntext[1]{%
	\noindent\makebox[10pt][r]{\@thefnmark.\,}#1}

% Configuración de la numeración de páginas
\pagenumbering{arabic}
\setcounter{page}{4}

% Definición de teoremas y entornos
\declaretheoremstyle[bodyfont=\fontshape{it}\selectfont]{normalbody}
\declaretheorem[style=normalbody,name=Problem]{pro}
\newtheorem{claim}{Claim}
\newtheorem{definition}{Definition}
\newtheorem{lemma}{Lemma}
\newtheorem{theorem}{Theorem}
\newtheorem{example}{Example}
\newtheorem{assumption}{Assumption}

% Nuevos comandos para metadatos
\newcommand{\shorttitle}[1]{\def\@shorttitle{#1}}
\newcommand{\volumeinfo}[3]{\def\@year{#1}\def\@volumenum{#2}\def\@issuenumber{#3}}
\newcommand{\publicationperiod}[1]{\def\@pubperiod{#1}}
\newcommand{\receiveddate}[1]{\def\@receiveddate{#1}}
\newcommand{\accepteddate}[1]{\def\@accepteddate{#1}}
\newcommand{\keywords}[1]{\def\@keywords{#1}}

% Configuración de secciones
\maxsecnumdepth{section}
\setsecnumdepth{section}
\setcounter{secnumdepth}{1}
\renewcommand{\thesection}{\arabic{section}}

% Configuración de autores y correos electrónicos
\providecommand{\Authsep}{; }
\renewcommand{\Authsep}{; }
\makeatletter
 \newcounter{author}
\renewcommand*\author[1]{%
	\stepcounter{author}%
	\ifnum\c@author=1
	\gdef\@author{#1}%
	\else
	\xdef\@author{\unexpanded\expandafter{\@author\Authsep#1}}%
	\fi
	\csgdef{author@\the\c@author}{#1}}
\newcommand*\email[1]{%
	\csgdef{email@\the\c@author}{#1}}
\newcommand*\address[1]{%
	\csgdef{address@\the\c@author}{#1}}

\newcommand{\printauthoremails}{%
	\xdef\author@count{\the\c@author}%
	\c@author=1
	\subsection*{Direcciones de correo de los autores}
	\print@authors}


\newcommand*\print@authors{%
	\ifnum\c@author>\author@count
	\else
	\print@author{\the\c@author}%
	\advance\c@author by 1
	\expandafter\print@authors
	\fi}
\newcommand*\print@author[1]{%
	\par\medskip
	\small
	\noindent
	\begin{tabular}{@{}l@{}}%
		\textsc{\csuse{author@#1}}:
		\csuse{address@#1}
		{\footnotesize\href{mailto:\csuse{email@#1}}{\csuse{email@#1}}}
\end{tabular}}

% Configuración del resumen y palabras clave
\renewcommand{\abstractname}{Abstract}
\newcommand{\keywordsname}{Palabras clave}



\newlength{\abstractwidth}
\setlength{\abstractwidth}{\dimexpr\textwidth+45mm}
\setlength{\oddsidemargin}{-22.5mm}




\newlength{\abstractcolumnsep}
\setlength{\abstractcolumnsep}{1cm}

\renewenvironment{abstract}{%
	\hyphenpenalty=1000
	\tolerance=1000
	\emergencystretch=0.5em
	\justifying
	\hyphenation{}
	\noindent
	\begin{minipage}{\abstractwidth}
		\scriptsize
		\hrule height 0.2pt
		\vspace{0.8em}
		\begin{minipage}[t]{\dimexpr0.33\abstractwidth-0.5\abstractcolumnsep}
			\centering\textbf{\footnotesize Información del Artículo}
			\vspace{0.5em}
			\hrule height 0.4pt
			\vspace{0.5em}
			Recibido: \@receiveddate\\
			Aceptado: \@accepteddate
			\vspace{0.5em}
			\hrule height 0.4pt
			\vspace{0.5em}
			\textbf{\footnotesize\keywordsname:}
			\@keywords
		\end{minipage}%
		\hfill
		\begin{minipage}[t]{\dimexpr0.67\abstractwidth-0.5\abstractcolumnsep}
			\centering\textbf{\footnotesize\abstractname}
			\vspace{0.5em}
			\hrule height 0.4pt
			\vspace{0.5em}
			\begin{minipage}{\linewidth}
				\hyphenpenalty=1000
				\tolerance=1000
				\emergencystretch=0.5em
				\justifying
				\hyphenation{}
				
			}{%
			\end{minipage}
		\end{minipage}
		\hrule height 0.4pt
	\end{minipage}
	\vspace{-1em}
}

% Redefinición de \emph
\renewcommand{\emph}[1]{\textit{#1}}

% Comando para establecer el tamaño de fuente de las secciones
\newcommand{\sectionfontsize}[1]{%
	\setsecheadstyle{\bfseries\LARGE}
	\ifcase#1\relax
	\setsecheadstyle{\bfseries\Large}
	\fi
}

% Configuración de la numeración de figuras
\counterwithout{figure}{chapter}
\renewcommand{\thefigure}{\arabic{figure}}

% Definición del logo
\newcommand{\syxlogo}{%
	\begin{tikzpicture}[
		>=stealth,
		node distance=3.5cm,
		auto
		]
		\def\wdim{1.7cm}
		\node (A) at ({0cm},{0cm}) {\includegraphics[width=\wdim]{fuentes/logoia-3.eps}};
		\node (B) [right of=A, xshift=0.5cm, yshift=0cm, text width=5cm]{
			\scriptsize
			\begin{tabular}{l}
				Informaticae Abstracta\\
				Año \@year, Vol. \@volumenum, No. \@issuenumber, pp. \MakeUppercase{\@startpage}-\MakeUppercase{\getpagerefnumber{LastPage}}
				\@pubperiod
			\end{tabular}
		};
	\end{tikzpicture}%
}

% Configuración de encabezados y pies de página
\fancypagestyle{firstpage}{%
	\fancyhf{}
	\renewcommand{\headrulewidth}{0pt}
	\renewcommand{\footrulewidth}{0pt}
	\fancyhead[L]{%
		\raisebox{-\height}{\syxlogo}%
	}
}

\fancypagestyle{otherpage}{%
	\fancyhf{}
	\renewcommand{\headrulewidth}{0.4pt}
	\fancyhead[R]{\footnotesize\thepage}
	\fancyhead[L]{\footnotesize\@shorttitle}
	\fancyfoot[C]{\footnotesize Informaticae Abstracta.  Año \@year, Vol.
	\setlength{\headwidth}{\textwidth}	
     \@volumenum, No. \@issuenumber}
}

\pagestyle{otherpage}

% Redefinir \maketitle
\renewcommand\maketitle{%
	\thispagestyle{firstpage}%
	\vspace*{0.5cm}%
	\begin{center}%
		\let \footnote \thanks
		{\LARGE \@title \par}%
		\vskip 1em%
		{\small \@author \par}%
	\end{center}%
	\gdef\@startpage{\thepage}%
	\@abstract
}

% Ajustar indentación después de subtemas
\newcommand{\subtema}[1]{%
	\subsection*{#1}%
	\aftergroup\@afterindentfalse
	\aftergroup\@afterheading
}

% Inicialización de variables al comienzo del documento
\AtBeginDocument{%
	\@ifundefined{@shorttitle}{\shorttitle{\@title}}{}%
	\@ifundefined{@year}{\volumeinfo{2024}{2}{2}}{}%
	\@ifundefined{@pubperiod}{\publicationperiod{JUL | DIC 20244}}{}%
	\@ifundefined{@startpage}{\gdef\@startpage{1}}{}%
	\@ifundefined{@receiveddate}{\receiveddate{\today}}{}%
	\@ifundefined{@accepteddate}{\accepteddate{\today}}{}%
	\@ifundefined{@keywords}{\keywords{}}{}%
	\@ifundefined{@abstract}{\gdef\@abstract{}}{}%
	\AtEndDocument{\label{LastPage}}
}

\setlength{\abstractcolumnsep}{0.4cm}


% Comando para ajustar el espacio vertical antes de la %\renewcommand{\adjustbibliographyspace}{}


\renewenvironment{thebibliography}[1]{%
	\par\vspace{-1.5em}% Reducir el espacio antes del título
	{\Large\bfseries\refname}\par% Título de la bibliografía
	\vspace{0.5em}% Espacio después del título
	\list{\@biblabel{\@arabic\c@enumiv}}{%
		\settowidth\labelwidth{\@biblabel{#1}}%
		\leftmargin\labelwidth
		\advance\leftmargin\labelsep
		\itemsep2pt
		\parsep2pt
		\@openbib@code
		\usecounter{enumiv}%
		\let\p@enumiv\@empty
		\renewcommand\theenumiv{\@arabic\c@enumiv}}%
	\sloppy\parfillskip=0pt plus 1fil%
	\emergencystretch=1em
}{%
	\def\@noitemerr
	{\@latex@warning{Empty `thebibliography' environment}}%
	\endlist
}










\makeatother

\usepackage{silence}
\WarningFilter{latex}{Command \openbox already defined}

\newcommand{\setpythonpath}[1]{
	\lstset{inputpath=#1}
}


\RequirePackage[T1]{fontenc}
\RequirePackage{listings}
% Definición del color de fondo
\definecolor{light-gray}{gray}{0.95}


% Configurar los colores para la sintaxis de Python
\definecolor{pythonblue}{RGB}{0,0,255}
\definecolor{pythongreen}{RGB}{0,128,0}
\definecolor{pythonpurple}{RGB}{128,0,128}

% Definición del estilo Python con mejor soporte para UTF-8
\lstdefinestyle{pythonstyle}{
	language=Python,
	basicstyle=\ttfamily\fontsize{9}{10}\selectfont,
	backgroundcolor=\color{light-gray},
	breaklines=true,
	postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space},
	showstringspaces=false,
	commentstyle=\color{green!40!black},
	keywordstyle=\color{blue},
	stringstyle=\color{red},
	numbers=left,
	numberstyle=\tiny\color{gray},
	numbersep=5pt,
	tabsize=4,
	extendedchars=true,
	literate={
		á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1
	{Á}{{\'A}}1 {É}{{\'E}}1 {Í}{{\'I}}1 {Ó}{{\'O}}1 {Ú}{{\'U}}1
	{ñ}{{\~n}}1 {Ñ}{{\~N}}1
	{¡}{{!`}}1 {¿}{{?`}}1
	{ü}{{\"u}}1 {Ü}{{\"U}}1
}

% Configuración global de listings
\lstset{
	style=pythonstyle,
	captionpos=b,
	breaklines=true,
	breakatwhitespace=false,
	extendedchars=true
}

% Comando para importar archivos Python
\newcommand{\inputpython}[1]{
	\lstinputlisting[language=Python]{#1}
}

\counterwithout{table}{chapter}
% Cambiar "Cuadro" por "Tabla"
\renewcommand{\tablename}{Tabla}
\renewcommand{\thetable}{\arabic{table}}

% Si estás usando babel con español, también necesitas esto:
\addto\captionsspanish{
	\renewcommand{\tablename}{Tabla}
}




\endinput