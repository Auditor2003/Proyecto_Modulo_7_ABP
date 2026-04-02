# Alke Wallet – Proyecto Módulo 7 (ABP)

Aplicación web desarrollada con Django que simula una billetera digital, permitiendo la gestión de usuarios, beneficiarios, monedas y transacciones financieras.

---

## Descripción del Proyecto

Alke Wallet es una aplicación fintech desarrollada como proyecto final del módulo de Desarrollo Web con Django.  
Permite a los usuarios gestionar sus activos financieros mediante operaciones seguras y controladas.

El sistema implementa funcionalidades clave como:

- Creación y gestión de usuarios financieros
- Administración de beneficiarios
- Gestión de monedas
- Transferencias entre usuarios
- Depósitos de dinero
- Visualización de cartola (historial financiero)
- Autenticación de usuarios (login/logout)

---

## Objetivo

Desarrollar una aplicación web funcional que:

- Utilice el ORM de Django correctamente
- Implemente operaciones CRUD completas
- Integre autenticación de usuarios
- Maneje relaciones entre entidades
- Garantice la integridad de los datos
- Presente una experiencia de usuario clara y consistente

---

## Tecnologías utilizadas

- Python 3
- Django
- MySQL
- HTML5 + CSS3
- Django Templates
- Git & GitHub

---

## Funcionalidades principales

### Autenticación
- Login y logout con Django auth
- Protección de vistas con sesión activa
- Uso de request.user en interfaz

### Gestión de Usuarios
- Crear, editar, eliminar usuarios financieros
- Visualización de saldo
- Acceso a cartola individual

### Transacciones
- Envío de dinero entre usuarios
- Validación de saldo insuficiente
- Asociación a moneda

### Depósitos
- Carga de saldo a usuarios
- Registro como movimiento financiero

### Cartola (Historial)
- Vista tipo bancaria
- Identificación de ingresos y egresos
- Visualización de saldo actual

### Beneficiarios
- CRUD completo
- Restricción de eliminación si existen transacciones asociadas

### Monedas
- CRUD completo
- Relación con transacciones

---

## Modelo de Datos

El sistema implementa relaciones reales utilizando el ORM de Django:

- Usuario → Transacciones
- Beneficiario → Transacciones
- Moneda → Transacciones

Se utilizan claves foráneas (ForeignKey) para representar relaciones del mundo real.

---

## Migraciones

- Uso de makemigrations y migrate
- Sincronización correcta de la base de datos
- Estructura consistente y versionada

---

## Lógica de negocio implementada

- Validación de saldo antes de transferir
- Moneda obligatoria en transacciones
- Restricción de eliminación de entidades con historial
- Diferenciación entre depósitos y transferencias

---

## Experiencia de Usuario (UX/UI)

Se implementaron mejoras visuales para simular una aplicación fintech real:

- Navbar interactivo con botones
- Dashboard con indicadores y acciones rápidas
- Formularios consistentes y alineados
- Mensajes visuales (feedback al usuario)
- Cartola estilo banco
- Footer con identidad del autor
- Microinteracciones (hover, focus)

---

## Arquitectura del Proyecto

Separación clara de responsabilidades:

- Django User → Autenticación
- Modelo Usuario → Lógica financiera

---

## Acceso al sistema

- Crear usuario desde la opción "Registrarse"
- Iniciar sesión
- Acceder al dashboard

---

## Repositorio

https://github.com/Auditor2003/Proyecto_Modulo_7_ABP

---

## Evaluación del Proyecto

Este proyecto cumple con los requerimientos del módulo:

- Configuración de base de datos
- Uso del ORM con relaciones
- Migraciones correctas
- Operaciones CRUD completas
- Uso de Django Auth
- Implementación de formularios con CSRF
- Buenas prácticas de desarrollo

Además, incorpora elementos adicionales:

- Mejora de experiencia de usuario (UX)
- Interfaz visual consistente
- Lógica de negocio real (wallet)

---

## Reflexión

Durante el desarrollo se priorizó:

- Separación de responsabilidades
- Consistencia visual
- Validaciones reales de negocio
- Simulación de un entorno fintech

---

## Autor

Diego Muñoz Lasanta


