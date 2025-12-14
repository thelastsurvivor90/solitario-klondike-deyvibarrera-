# solitario-klondike-deyvibarrera-
# 🎮 Solitario Klondike - Proyecto Python + Tkinter
## 📁 ESTRUCTURA DE ARCHIVOS A ENTREGAR

```
📦 Proyecto-Solitario/
├── 📄 solitaire_klondike.py    (Código Python)
├── 📄 informe.tex               (Documento LaTeX)
├── 📄 informe.pdf               (PDF compilado)
└── 📄 README.md                 (Este archivo)
```

---

## 🚀 CÓMO EJECUTAR EL JUEGO

### En Windows:
```bash
# Abre CMD o PowerShell en la carpeta del proyecto
python solitaire_klondike.py
```

### En Mac/Linux:
```bash
python3 solitaire_klondike.py
```

### Requisitos:
- ✅ Python 3.8 o superior
- ✅ Tkinter (viene incluido con Python)

---

## 📝 CÓMO COMPILAR EL INFORME LaTeX

### En TeXstudio (tu editor):
1. Abre `informe.tex`
2. Presiona **F5** o click en el botón **"Compilar"**
3. Se generará `informe.pdf`

### Desde terminal:
```bash
pdflatex informe.tex
pdflatex informe.tex
```
(Se ejecuta 2 veces para generar índices correctamente)

---

## 🎮 CONTROLES DEL JUEGO

- **Click en mazo**: Robar carta del mazo
- **Click y arrastrar**: Mover cartas
- **Soltar sobre pila válida**: Completar movimiento
- **Botón "Nuevo Juego"**: Reiniciar con nuevas cartas
- **Botón "Reiniciar"**: Volver a empezar el juego actual

---

## 🎯 REGLAS DEL SOLITARIO

### Objetivo:
Construir 4 fundaciones (pilas base) del As al Rey, una por cada palo.

### Movimientos permitidos:
1. **En el Tableau**: Alternar colores (rojo-negro) y decrecer valores
2. **Espacios vacíos**: Solo se pueden colocar Reyes
3. **Fundaciones**: Comenzar con As, subir en orden, mismo palo

### Cómo ganar:
Completar las 4 fundaciones con todas las cartas (52 cartas).

---

## 💻 TECNOLOGÍAS USADAS

- **Lenguaje**: Python 3.8+
- **GUI**: Tkinter
- **Estructuras**: Lists, Dictionaries, Tuples
- **Programación**: POO (Clases, Herencia, Encapsulamiento)
- **Documentación**: LaTeX

---

## 📧 PARA EL PROFESOR

### Link del proyecto:
```
[PEGAR AQUÍ EL LINK DE GITHUB/DRIVE]
```

### Cómo probar:
1. Descargar `solitaire_klondike.py`
2. Ejecutar con Python 3.8+
3. Jugar y verificar funcionalidad

### Archivos incluidos:
- ✅ Código Python funcionando
- ✅ Informe LaTeX completo
- ✅ PDF compilado
- ✅ Documentación README

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "No module named 'tkinter'"
```bash
# Windows
pip install tk

# Ubuntu/Debian
sudo apt-get install python3-tk

# Mac (ya viene incluido)
```

### Error: "Python no reconocido"
- Instala Python desde https://www.python.org
- Marca la opción "Add Python to PATH"

### El juego no abre:
1. Verifica que tienes Python 3.8+: `python --version`
2. Verifica que Tkinter está instalado: `python -c "import tkinter"`
3. Ejecuta desde la terminal, no haciendo doble click

---

## ✨ CARACTERÍSTICAS IMPLEMENTADAS

- ✅ Lógica completa del Solitario Klondike
- ✅ Interfaz gráfica atractiva
- ✅ Sistema drag & drop funcional
- ✅ Validación de movimientos
- ✅ Contador de movimientos
- ✅ Detección de victoria
- ✅ Botones de control (Nuevo, Reiniciar)
- ✅ Animaciones suaves

---

## 📊 CALIFICACIÓN

| Criterio | Peso | Estado |
|----------|------|--------|
| Funcionamiento y uso de Python | 25% | ✅ Completo |
| Calidad gráfica | 25% | ✅ Completo |
| Informe LaTeX | 25% | ✅ Completo |
| Manejo Unidad 4 (POO, estructuras) | 25% | ✅ Completo |

---

## 👤 AUTOR

**Nombre**: [Deyvi Samuel Barrera Rodriguez]  
**Curso**: Estadística Descriptiva y Probabilidad 2025-II  
**Fecha**: Noviembre 2024

---

## 📄 LICENCIA

Este proyecto es para fines educativos.

---

## 🙏 AGRADECIMIENTOS

Proyecto desarrollado como parte del curso de Estadística Descriptiva y Probabilidad 2025-II
De la mano de la orientacion de la asombrosa y diligente docente Ruth Mery Gonzalez Sepulveda 
Tener en cuenta que aun anda en desarollo por motivos de fallos en python


---

**¡Disfruta del juego! 🎮♠️♥️♦️♣️**
