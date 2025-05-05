
# 📘 Dahua ANPR / LPR API - Documentación esencial

Este documento resume las principales APIs HTTP/CGI disponibles en cámaras Dahua compatibles con reconocimiento de patentes (LPR / ANPR), como la **DHI-ITC431-RW1F-IRL8**. Las cámaras ITC utilizan comandos CGI estándares y permiten integración avanzada con sistemas externos mediante HTTP, incluyendo modo push.

---

## ✅ 1. Captura de imagen instantánea

```http
GET /cgi-bin/snapshot.cgi
```

- Captura una imagen en tiempo real desde la cámara.
- Requiere autenticación Digest.
- Puede utilizarse para guardar imágenes de respaldo junto con eventos ANPR.

---

## 📤 2. Envío automático de eventos ANPR (modo push)

> Usado cuando la cámara envía automáticamente información de patentes detectadas a un servidor externo (middleware).

### 🔹 Configuración general

- Interfaz web Dahua > **ANPR / Data Upload / HTTP**
- URL del servidor: `http://[IP]:[PORT]/evento-lpr`

### 🔹 Ejemplo de JSON enviado

```json
{
  "plate": "ABC123",
  "timestamp": "2025-05-05T12:34:56Z",
  "image_url": "http://192.168.1.108/snapshot.jpg",
  "channel": 1,
  "confidence": 95,
  "lane": 2
}
```

> Este JSON puede ampliarse según la configuración de la cámara (color del auto, marca, etc.).

---

## 🔍 3. Consulta de eventos históricos (recordFinder)

```http
POST /cgi-bin/recordFinder.cgi?action=find&name=TrafficSnap
```

- Permite buscar eventos ANPR anteriores por fecha, placa, canal, etc.
- Se usa para recuperar información puntual desde la memoria de la cámara.

---

## 📋 4. Gestión de lista blanca / negra de vehículos

Permite registrar o eliminar placas autorizadas directamente en la cámara (útil si no se usa una base de datos externa).

### 🔹 Agregar vehículo

```http
POST /cgi-bin/vehicle.cgi?action=add
```

Cuerpo:
```json
{
  "plate": "ABC123",
  "enable": true,
  "group": "Autorizados"
}
```

### 🔹 Eliminar vehículo

```http
POST /cgi-bin/vehicle.cgi?action=delete
```

Cuerpo:
```json
{
  "plate": "ABC123"
}
```

---

## 🔄 5. Búsqueda de vehículos registrados

```http
POST /cgi-bin/vehicle.cgi?action=find
```

Permite buscar por número de placa, grupo, tipo, etc.

---

## 🛠️ 6. Configuración de imagen / enfoque

```http
GET /cgi-bin/configManager.cgi?action=getConfig&name=VideoInMode
POST /cgi-bin/configManager.cgi?action=setConfig&name=VideoInMode
```

Permite ajustar brillo, contraste, foco, exposición y otros parámetros de la cámara.

---

## 🔒 Autenticación

Todas las llamadas requieren autenticación Digest:

- Usuario: el configurado en la cámara (ej: `admin`)
- Contraseña: definida por el integrador
- Algunas cámaras pueden requerir certificado SSL o habilitar CORS en modo seguro

---

## 🧠 Consideraciones generales

- Asegurarse de que el firmware tenga habilitado el módulo ANPR.
- Verificar si se requiere configurar reglas de disparo (líneas, zonas, velocidad).
- Algunos endpoints pueden variar según la región o firmware específico.

---

## 📚 Referencias

- Dahua HTTP API v3.26
- Manuales de usuario de cámaras ITC Dahua
- Documentación oficial: [https://dahuawiki.com](https://dahuawiki.com)

