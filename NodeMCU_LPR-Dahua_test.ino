// Código para NodeMCU ESP8266 - Control de LED por comandos seriales
// Compatible con comandos enviados desde middleware Dahua LPR

// Define el pin del LED integrado en NodeMCU
#define LED_BUILTIN 2  // En NodeMCU ESP8266, el LED integrado suele estar en el pin 2

// Buffer para almacenar datos seriales
byte receivedData[5];
int dataIndex = 0;

void setup() {
  // Inicializar comunicación serial
  Serial.begin(9600);
  
  // Configurar LED como salida
  pinMode(LED_BUILTIN, OUTPUT);
  
  // Asegurarse de que el LED esté apagado al inicio
  digitalWrite(LED_BUILTIN, HIGH);  // En NodeMCU el LED es activo en bajo
  
  Serial.println("NodeMCU listo para recibir comandos de activación");
}

void loop() {
  // Verificar si hay datos disponibles en el puerto serial
  while (Serial.available() > 0) {
    // Leer byte recibido
    byte inByte = Serial.read();
    
    // Almacenar en buffer
    if (dataIndex < 5) {
      receivedData[dataIndex] = inByte;
      dataIndex++;
    }
    
    // Si hemos recibido 5 bytes, verificar si es nuestro comando
    if (dataIndex == 5) {
      // Verificar si el comando recibido es el esperado: \xA0\x01\x01\x03\xA4
      if (receivedData[0] == 0xA0 && 
          receivedData[1] == 0x01 && 
          receivedData[2] == 0x01 && 
          receivedData[3] == 0x03 && 
          receivedData[4] == 0xA4) {
        
        // Comando reconocido - activar LED
        Serial.println("Comando reconocido: Activando LED");
        activarLED(receivedData[3]); // El 4º byte (0x03) indica 3 segundos
      } else {
        Serial.println("Comando desconocido recibido");
      }
      
      // Reiniciar índice para recibir nuevo comando
      dataIndex = 0;
    }
  }
}

void activarLED(int segundos) {
  // Encender LED (activo en bajo en NodeMCU)
  digitalWrite(LED_BUILTIN, LOW);
  
  // Enviar confirmación por serial
  Serial.print("LED activado por ");
  Serial.print(segundos);
  Serial.println(" segundos");
  
  // Esperar el tiempo especificado
  delay(segundos * 1000);
  
  // Apagar LED
  digitalWrite(LED_BUILTIN, HIGH);
  
  Serial.println("LED desactivado");
}
