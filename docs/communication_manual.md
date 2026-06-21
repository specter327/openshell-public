# SimpleX Chat: Plataforma de Mensajería sin Identificadores

Este repositorio contiene la documentación, arquitectura y guías de despliegue para **SimpleX Chat**, la primera plataforma de comunicación diseñada bajo el paradigma de **cero identificadores de usuario**[cite: 1].

---

## 📋 Índice
1. [Introducción](#-introducción)
2. [Pilares Fundamentales](#-pilares-fundamentales)
   - [Seguridad](#seguridad)
   - [Privacidad](#privacidad)
   - [Anonimato](#anonimato)
3. [Arquitectura Técnica y Funcionamiento](#%EF%B8%8F-arquitectura-técnica-y-funcionamiento)
4. [Matriz de Compatibilidad](#%EF%B8%8F-matriz-de-compatibilidad)
5. [Guía de Instalación Multiplataforma](#-guía-de-instalación-multiplataforma)
   - [Windows](#windows)
   - [GNU/Linux](#gnulinux)
   - [macOS](#macos)
   - [Android](#android)
   - [iOS](#ios)
6. [Guía de Inicio Rápido](#-guía-de-inicio-rápido)

---

## 🚀 Introducción

A diferencia de las herramientas de mensajería convencionales (como Signal, WhatsApp o Telegram), **SimpleX Chat** no utiliza números de teléfono, direcciones de correo electrónico, ni identificadores únicos globales (IDs) asignados a los usuarios[cite: 1]. Su arquitectura se basa en **enlaces de comunicación unidireccionales y efímeros**, lo que destruye la capacidad de los servidores de compilar grafos de relaciones sociales o mapear metadatos de tráfico[cite: 1].

---

## 🔒 Pilares Fundamentales

### Seguridad
* **Cifrado E2EE Post-Cuántico:** Implementa el protocolo *Double Ratchet* utilizando primitivas criptográficas resistentes a la computación cuántica para garantizar la confidencialidad a largo plazo (*Forward Secrecy*)[cite: 1].
* **Cifrado en Reposo:** La base de datos local del cliente está protegida mediante algoritmos criptográficos robustos bajo una frase de paso definida por el usuario[cite: 1].
* **Aislamiento de Redes:** Soporte nativo para el enrutamiento de tráfico a través de redes de anonimato como **Tor** o **I2P**, ocultando la dirección IP de origen de los nodos de transporte[cite: 1].

### Privacidad
* **Eliminación de Metadatos de Tráfico:** Los servidores intermedios de mensajería (relays) actúan de forma aislada para cada dirección de un canal de comunicación[cite: 1]. No conocen la contraparte ni pueden vincular flujos entrantes y salientes[cite: 1].
* **Zero-Knowledge por Diseño:** Los perfiles de usuario, listas de contactos y configuraciones de grupos residen exclusivamente de manera local en los dispositivos de los extremos de la comunicación[cite: 1].
* **Padding de Mensajes:** Todo el tráfico es ajustado a tamaños de bloque fijos para mitigar los ataques de análisis de tráfico basados en el tamaño de los paquetes de datos[cite: 1].

### Anonimato
* **Modo Incógnito Dinámico:** Permite la asignación automática de nombres de perfil aleatorios y efímeros para cada nueva conexión establecida, impidiendo la correlación de identidad entre contactos[cite: 1].
* **Perfiles Ocultos (Hidden Profiles):** Capacidad de configurar perfiles secundarios protegidos por contraseñas independientes, los cuales permanecen invisibles en la interfaz de usuario estándar[cite: 1].
* **Mitigación Absoluta de Spam:** Es físicamente imposible recibir mensajes no solicitados[cite: 1]. Un usuario solo puede iniciar una comunicación si posee un enlace de invitación único generado por el destinatario[cite: 1].

---

## 🛠️ Arquitectura Técnica y Funcionamiento

En lugar de un servidor centralizado con una base de datos de usuarios, SimpleX opera mediante **Relés de Mensajería (Messaging Relays)**[cite: 1].