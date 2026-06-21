# SimpleX Chat

## ¿Qué es SimpleX?

SimpleX Chat es una plataforma de mensajería diseñada con un objetivo radical: **permitir comunicación privada sin requerir identificadores globales**.

A diferencia de la mayoría de aplicaciones de mensajería modernas, SimpleX no utiliza:

* Números telefónicos
* Correos electrónicos
* Nombres de usuario globales
* Directorios centrales de usuarios

Cada conversación utiliza identificadores y colas independientes, reduciendo drásticamente la capacidad de correlación entre usuarios.

---

# Principios de Diseño

SimpleX fue construido alrededor de tres objetivos fundamentales:

## 1. Privacidad

Ningún servidor conoce:

* Tu lista de contactos
* Tus grupos
* Con quién hablas
* Cuántas conversaciones tienes

Los servidores únicamente observan tráfico cifrado asociado a colas temporales.

---

## 2. Seguridad

Todo el contenido está protegido mediante:

* Cifrado de extremo a extremo (E2EE)
* Intercambio seguro de claves
* Verificación criptográfica de identidad
* Perfect Forward Secrecy (PFS)

Incluso si un servidor es comprometido:

* No puede leer mensajes
* No puede modificar mensajes sin detección
* No puede reconstruir relaciones sociales completas

---

## 3. Anonimato

SimpleX elimina uno de los problemas más comunes de la mensajería moderna:

> El identificador permanente.

Aplicaciones tradicionales requieren:

* Número telefónico
* Correo electrónico
* Username global

Esto permite rastrear usuarios a través del tiempo.

SimpleX utiliza:

* Invitaciones únicas
* Direcciones efímeras
* Colas independientes por conversación

Lo que dificulta significativamente la correlación de actividad.

---

# Características de Seguridad

## Sin Identificadores Globales

No existe una base de datos central con:

```text
Usuario -> Identidad
```

Cada conexión se establece mediante enlaces o códigos de invitación.

---

## End-to-End Encryption

Todos los mensajes son cifrados localmente.

Los servidores únicamente retransmiten datos cifrados.

---

## Perfect Forward Secrecy

La exposición futura de una clave no permite descifrar conversaciones anteriores.

---

## Protección contra Correlación

SimpleX utiliza:

* Múltiples colas
* Diferentes servidores
* Identificadores independientes

Esto dificulta construir un grafo social de usuarios.

---

## Código Abierto

Todo el proyecto es auditable.

Permite:

* Revisión independiente
* Auditorías de seguridad
* Compilación propia

---

# Características de Privacidad

## No requiere teléfono

No es necesario proporcionar:

* Número móvil
* SIM
* Operadora

---

## No requiere correo electrónico

Puede utilizarse sin:

* Gmail
* Outlook
* ProtonMail

---

## Sin libreta de contactos obligatoria

No necesita acceder a:

* Agenda telefónica
* Contactos del sistema

---

## Servidores descentralizados

Puede utilizar:

* Servidores públicos
* Servidores propios
* Infraestructura privada

---

# Compatibilidad

SimpleX ofrece clientes para múltiples plataformas.

## Escritorio

| Plataforma | Soporte |
| ---------- | ------- |
| Windows    | ✅       |
| GNU/Linux  | ✅       |
| macOS      | ✅       |

---

## Móviles

| Plataforma   | Soporte |
| ------------ | ------- |
| Android      | ✅       |
| iPhone / iOS | ✅       |

---

# Casos de Uso

SimpleX es especialmente útil para:

* Administración remota
* Operaciones de seguridad
* Equipos distribuidos
* Comunicaciones sensibles
* Infraestructura autogestionada
* Proyectos de privacidad

---

# Instalación

## Windows

1. Descargar el instalador oficial.
2. Ejecutar el instalador.
3. Completar el asistente.
4. Abrir SimpleX Chat.

---

## GNU/Linux

### AppImage

```bash
chmod +x simplex-desktop.AppImage

./simplex-desktop.AppImage
```

---

### Debian / Ubuntu

```bash
sudo dpkg -i simplex-desktop.deb
```

---

### Arch Linux

Instalar mediante AUR:

```bash
yay -S simplex-chat
```

---

## macOS

### Apple Silicon / Intel

1. Descargar el paquete oficial.
2. Abrir el archivo `.dmg`.
3. Arrastrar la aplicación a `Applications`.
4. Ejecutar SimpleX Chat.

---

## Android

### Google Play

Instalar desde:

[Google Play Store](https://play.google.com/store/apps/details?id=chat.simplex.app&utm_source=chatgpt.com)

---

### APK Directo

También puede instalarse mediante APK firmado descargado desde las publicaciones oficiales.

---

## iPhone / iOS

Instalar desde:

[Apple App Store](https://apps.apple.com/app/simplex-chat/id1605771084?utm_source=chatgpt.com)

---

# Primer Contacto

## Crear Perfil

Al iniciar por primera vez:

1. Elegir nombre local.
2. Configurar fotografía (opcional).
3. Crear perfil.

---

## Añadir Contacto

Puede realizarse mediante:

* Código QR
* Enlace de invitación
* Cadena de conexión

Ejemplo:

```text
https://simplex.chat/contact#...
```

---

## Crear Grupo

1. Crear grupo.
2. Compartir enlace de invitación.
3. Los miembros se unen directamente.

---

# Ventajas para OpenShell

SimpleX resulta especialmente atractivo para OpenShell debido a que:

* No requiere infraestructura adicional.
* Funciona sobre Internet convencional.
* Está disponible en escritorio y móvil.
* Permite comunicaciones seguras entre operadores.
* Reduce dependencia de correo electrónico.
* Reduce dependencia de números telefónicos.
* Facilita intercambio de identidades Ed25519.
* Puede utilizarse para distribuir UIDs, PIKs, pasaportes y códigos de verificación.

Ejemplo:

```text
UID:
019edee2-3fc0-7fc1-ad7f-96cafd18aaa2

PIK:
508fa4c72c6e14a20d60fec653fb1c143c4501fce787af7b5177fbfbcc1efcd4
```

Sin preocuparse por problemas de codificación PEM, saltos de línea o incompatibilidades entre plataformas.

---

# Conclusión

SimpleX proporciona una combinación poco común de:

* Seguridad
* Privacidad
* Anonimato
* Código abierto
* Multiplataforma
* Facilidad de uso

Para proyectos donde la identidad criptográfica es más importante que la identidad personal, SimpleX representa una de las opciones de comunicación más sólidas disponibles actualmente.
