
# 📘 Dahua ANPR / LPR - Documentación completa de APIs HTTP

Este documento resume las APIs más importantes que se pueden usar con **cámaras Dahua ANPR / LPR**, incluyendo el modelo **DHI-ITC431-RW1F-IRL8**. Se basa en el estándar HTTP API v3.26 de Dahua y contempla uso en modo **pull** y **push**, control de listas, captura de imágenes, búsqueda de eventos y configuración avanzada.

---

## 🧠 Categorías de APIs relevantes para ANPR / LPR

---

### 🔹 1. Captura de imagen y video

```http
GET /cgi-bin/snapshot.cgi
```
- Captura una imagen instantánea.
- Puede usarse desde cualquier cliente autenticado (Digest Auth).
- Ideal para respaldo visual al recibir un evento.

---

### 🔹 2. Eventos ANPR / LPR - Modo Push (HTTP Upload)

Estas APIs permiten que la cámara envíe los datos automáticamente a un servidor externo:

- **Configuración de evento HTTP Push:**
  - URL: `/cgi-bin/configManager.cgi?action=setConfig&name=NetApp.HTTPUpload.[index]`

- **Datos que se pueden recibir:**
```json
{
  "plate": "ABC123",
  "timestamp": "2025-05-05T12:34:56Z",
  "image_url": "http://192.168.1.100/snapshot.jpg",
  "channel": 1,
  "lane": 2,
  "confidence": 92
}
```

- **API involucrada:**
  - `ANPR Report Data Upload`
  - `NetApp.HTTPUpload.*`
  - `/ANPR/upload`

---

### 🔹 3. Búsqueda de eventos ANPR

```http
POST /cgi-bin/recordFinder.cgi?action=find&name=TrafficSnap
```

- Permite buscar eventos de patentes detectadas.
- Filtra por tiempo, canal, placa, etc.

---

### 🔹 4. Gestión de lista blanca / negra

Estas APIs permiten operar directamente sobre la base de placas almacenadas en la cámara:

- **Agregar vehículo:**
```http
POST /cgi-bin/vehicle.cgi?action=add
```

```json
{
  "plate": "ABC123",
  "enable": true,
  "group": "Autorizados",
  "beginTime": "2025-01-01T00:00:00",
  "endTime": "2025-12-31T23:59:59"
}
```

- **Eliminar vehículo:**
```http
POST /cgi-bin/vehicle.cgi?action=delete
```

- **Buscar vehículo:**
```http
POST /cgi-bin/vehicle.cgi?action=find
```

---

### 🔹 5. Configuración de imagen y lente

- `/cgi-bin/configManager.cgi?action=getConfig&name=VideoInMode`
- `/cgi-bin/configManager.cgi?action=setConfig&name=VideoInMode`

- Ajustes disponibles:
  - Brillo, contraste, exposición
  - Control de IR
  - Zoom y enfoque

---

### 🔹 6. Configuración de zonas de disparo (Reglas)

- `/cgi-bin/configManager.cgi?action=getConfig&name=Smart.*`
- `/cgi-bin/configManager.cgi?action=setConfig&name=Smart.*`

- Reglas disponibles:
  - Línea virtual
  - Área de entrada/salida
  - Cruce de carril

---

### 🔹 7. Base de datos de vehículos (completa)

- `/cgi-bin/vehicleDB.cgi?action=add`
- `/cgi-bin/vehicleDB.cgi?action=delete`
- `/cgi-bin/vehicleDB.cgi?action=find`

- Se puede trabajar con múltiples listas, grupos, horarios y atributos de vehículos.

---

### 🔹 8. Control y monitoreo de tráfico

- `/cgi-bin/trafficSnapManager.cgi` – Captura de tráfico
- `/cgi-bin/trafficCtrlManager.cgi` – Control de carriles
- `/cgi-bin/motorVehicleManager.cgi` – Información de vehículos

---

### 🔹 9. Diagnóstico y configuración general

- `/cgi-bin/magicBox.cgi?action=getSystemInfo` – Info del sistema
- `/cgi-bin/storageManager.cgi` – Ver estado del almacenamiento
- `/cgi-bin/machineStatus.cgi` – Estado de los módulos

---

### 🔹 10. Red y servicios externos

- `/cgi-bin/netApp.cgi?action=getConfig`
- `/cgi-bin/configManager.cgi?action=getConfig&name=NetApp.HTTPUpload.1`
- Configuración de NTP, HTTPS, DDNS, FTP, email

---

## 🔐 Autenticación requerida

Todas las API requieren **autenticación Digest**:

- Usuario: `admin` u otro definido
- Contraseña: la que esté configurada en la cámara

---

## 📚 Recomendaciones

- Usar siempre IP fija o DHCP reservado para la cámara.
- Probar cada API con herramientas como Postman o curl antes de integrarlas.
- Las rutas pueden cambiar según versión de firmware: siempre consultar `/cgi-bin/magicBox.cgi?action=getSystemInfo` para saber modelo exacto.

---

## 📄 Fuentes

- Dahua HTTP API v3.26 (documentación oficial)
- Experiencia práctica con cámaras ITC Dahua
- Wiki de Dahua: [https://dahuawiki.com](https://dahuawiki.com)
