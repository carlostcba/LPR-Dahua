
# Dahua LPR Middleware

Este proyecto es un **middleware desarrollado en Python** que permite integrar **cámaras de reconocimiento automático de patentes (LPR)** del fabricante **Dahua** con una base de datos **Microsoft SQL Server (MSSQL)**.

Funciona como un componente **standalone** (ejecutable `.exe`), ideal para ser ejecutado en **entornos Windows 10/11 LTSC**, y se puede **invocar desde otras aplicaciones**, como software escrito en **Visual Basic 6**.

---

## 🎯 Objetivo

> Permitir que una cámara Dahua LPR (por ejemplo, el modelo `DHI-ITC431-RW1F-IRL8`) pueda enviar sus eventos de detección de patentes a un sistema central basado en MSSQL, sin necesidad de software adicional de terceros.

---

## ⚙️ Funcionamiento del sistema

### 1. 🔁 Consulta periódica a la cámara
Cada cierto intervalo (configurado en el código, por defecto 10 segundos), el middleware:
- Se conecta a la cámara Dahua vía HTTP usando autenticación **Digest**.
- Obtiene una imagen actual (`snapshot`) desde la cámara.

### 2. 📝 Registro en base de datos
Una vez capturada la imagen:
- Se guarda en una carpeta local configurada en la base de datos.
- Se registra en MSSQL un nuevo evento con:
  - La patente (simulada por ahora: `ABC123`).
  - Fecha y hora del evento.
  - Ruta del archivo de imagen guardado.

> En versiones futuras, puede integrarse directamente con eventos ANPR reales usando la API avanzada Dahua (`TrafficSnap`, `eventManager`, etc).

---

## 🧱 Componentes del proyecto

| Archivo                  | Función Principal |
|--------------------------|-------------------|
| `main.py`                | Loop principal que ejecuta el proceso cada X segundos |
| `config_reader.py`       | Lee los datos de conexión desde MSSQL (IP, usuario, contraseña de la cámara, ruta de imagen) |
| `dahua_lpr_client.py`    | Captura imagen desde la cámara Dahua usando autenticación Digest |
| `db_writer.py`           | Inserta el evento en la base de datos MSSQL |
| `requirements.txt`       | Lista de librerías necesarias |
| `README.md`              | Documentación completa del proyecto |

---

## 🗃️ Base de datos

### 1. 📋 Tabla de configuración de cámara

```sql
CREATE TABLE DahuaConfig (
    id INT PRIMARY KEY,
    cam_ip VARCHAR(100),
    cam_user VARCHAR(50),
    cam_password VARCHAR(50),
    snapshot_path VARCHAR(255)
);
```

### 2. 📋 Tabla de eventos LPR

```sql
CREATE TABLE LPR_Events (
    Id INT IDENTITY PRIMARY KEY,
    PlateNumber VARCHAR(20),
    EventTime DATETIME,
    ImagePath VARCHAR(255)
);
```

> ⚠️ Asegurate de insertar los datos iniciales en `DahuaConfig` para que el sistema funcione correctamente.

---

## 🖥️ Requisitos del sistema

- Python 3.10+
- Windows 10/11 (LTSC recomendado)
- SQL Server 2016 o superior
- Acceso de red a la cámara Dahua
- Puerto HTTP habilitado (80, 88, o el configurado en la cámara)

---

## 🚀 Instalación

```bash
# 1. Clonar o descomprimir el proyecto
cd dahua_lpr_reader

# 2. Instalar las dependencias
pip install -r requirements.txt

# 3. Ejecutar el middleware
python main.py
```

---

## 📦 Compilación a EXE

Para generar el `.exe` ejecutable standalone:

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

El archivo resultante se ubicará en: `dist/main.exe`

---

## 🔄 Integración con Visual Basic 6

Podés llamar al ejecutable desde tu aplicación VB6 de la siguiente forma:

```vb
Dim pid As Long
pid = Shell("C:\ruta\a\main.exe", vbNormalFocus)
```

Esto permite que el middleware funcione como un **subproceso externo**, encargado de registrar eventos sin bloquear tu aplicación principal.

---

## 🛡️ Seguridad y recomendaciones

- Se utiliza **autenticación Digest** para comunicarte con la cámara Dahua, lo cual es más seguro que Basic Auth.
- Los datos se insertan mediante **parámetros seguros** en MSSQL.
- Es recomendable configurar una cuenta SQL con permisos mínimos para operar esta función.

---

## 📌 Próximas mejoras

- Lectura real de eventos ANPR desde la API Dahua (`TrafficSnap`, `eventManager.cgi`).
- Captura de datos como velocidad del vehículo, carril, y dirección.
- Interfaz web de monitoreo y logs.
- Logs de errores y registros locales en archivo `.log`.
