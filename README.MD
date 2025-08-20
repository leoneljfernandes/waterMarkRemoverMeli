# Watermark Removal Processor

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Development-yellow)

Una aplicación Python para procesar imágenes con marcas de agua utilizando la API de Kaze para eliminarlas y generar reportes con los resultados.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura de Archivos](#-estructura-de-archivos)
- [Formato de Entrada](#-formato-de-entrada)
- [Salida](#-salida)
- [Funcionamiento Interno](#-funcionamiento-interno)
- [Notas Importantes](#-notas-importantes)
- [Posibles Mejoras](#-posibles-mejoras)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

- Procesamiento por lotes de imágenes con marcas de agua
- Integración con la API de Kaze para eliminación de marcas de agua
- Generación de reportes en formato CSV
- Manejo de múltiples MLAs por SKU
- Procesamiento eficiente de datos agrupados por SKU

## 📋 Requisitos

- Python 3.6 o superior
- Biblioteca `requests`
- Conexión a internet
- API key de Kaze (incluida en el código)

## 🔧 Instalación

1. Clona o descarga el repositorio
2. Navega al directorio del proyecto
3. Instala las dependencias necesarias: pip install requests

## 🚀 Uso

1. Prepara tu archivo `listPrueba.txt` con los datos necesarios
2. Ejecuta el script: python main.py


3. El script procesará las imágenes y generará el archivo `resultado.csv` con los resultados

## 📁 Estructura de Archivos
```
.
├── main.py                 # Script principal
├── list.txt         # Archivo de entrada con datos (ejemplo)
├── resultado.csv          # Archivo de salida (se crea automáticamente)
├── README.md              # Este archivo
└── requirements.txt       # Dependencias del proyecto
```

## 📥 Formato de Entrada

El archivo `listPrueba.txt` debe tener el siguiente formato:

```
MLA123456789,SKU001,https://ejemplo.com/imagen1.jpg
MLA987654321,SKU001,https://ejemplo.com/imagen2.jpg
MLA555555555,SKU002,https://ejemplo.com/imagen3.jpg
```

Cada línea debe contener tres campos separados por comas:
1. MLA (identificador de producto)
2. SKU (código único de stock)
3. URL de la imagen con marca de agua

## 📤 Salida

El archivo `resultado.csv` generado tendrá el siguiente formato:

```csv
skuPerteneciente,listadoMlas,newUrl
SKU001,"['MLA123456789', 'MLA987654321']",https://nueva-url-imagen-procesada.jpg
SKU002,"['MLA555555555']",https://otra-url-imagen-procesada.jpg
```


## ⚠️ Notas Importantes

- Deberá utilizar su API key de Kaze
- El procesamiento de imágenes puede tomar tiempo dependiendo del tamaño y cantidad
- La aplicación procesa un SKU a la vez en la versión actual
- Se recomienda verificar los términos de servicio de Kaze antes de usar en producción


## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.


**Nota**: Este software es para fines educativos y de desarrollo. Asegúrate de cumplir con los términos de servicio de cualquier API utilizada y respetar los derechos de autor de las imágenes procesadas.