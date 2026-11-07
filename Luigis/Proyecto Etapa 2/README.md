# LUIGI'S - Sistema de Seguimiento de Entrenamientos (Etapa 2)

Bienvenido al sistema de persistencia y seguimiento de entrenamientos del club Luigi's. Esta versión (Etapa 2) incorpora lectura/escritura de archivos (CSV y JSON), manejo de diccionarios, validación con Expresiones Regulares, recursividad y un menú interactivo con control de excepciones.

---

## 1. Archivos Requeridos para la Ejecución
Para que el sistema inicie correctamente, necesitás tener estos tres archivos ubicados en la misma carpeta que tus scripts de Python:

1. `configuracion.json`: Contiene los límites del negocio (máximo 180 min, objetivo 150 min, categorías).
2. `usuarios.csv`: Contiene las credenciales para el Login.
3. `atletas.csv` y `registros.csv`: (Opcionales) El sistema los creará automáticamente si no existen para guardar el padrón y el historial de entrenamientos.

## 2. Credenciales de Acceso (Login)
Al ejecutar el programa, te solicitará un usuario y contraseña válidos (hasta 3 intentos).
Podés utilizar cualquiera de estos usuarios predefinidos:

* **Usuario:** `admin123`  | **Contraseña:** `secreta1`
* **Usuario:** `luigi123`  | **Contraseña:** `clave2`

## 3. Instrucciones de Ejecución

### Desde tu IDE (VS Code, PyCharm, IDLE, etc.)
Simplemente abrí el archivo `main_2.py` y presioná el botón de "Run" o "Play".

### Desde la Terminal (Recomendado)
Si estás usando la terminal de tu Mac o PC, es importante navegar correctamente hasta la carpeta del proyecto antes de ejecutarlo para evitar el error `[Errno 2] No such file or directory`.

**Paso a paso en Terminal:**
1. Abrí la terminal.
2. Usá el comando `cd` para ingresar a la carpeta exacta donde guardaste los archivos (por ejemplo: `cd Desktop/Luigis/Etapa\ 2`).
3. Una vez posicionado en la carpeta correcta, ejecutá el programa con el siguiente comando:
   ```bash
   python3 main_2.py
   ```
*(Nota: Nunca arrastres el archivo directamente a la terminal rodeándolo con múltiples comillas simples y dobles, ya que la consola no podrá leer la ruta correctamente).*

---

## 4. Pruebas Unitarias Automatizadas
El sistema incluye 7 pruebas exigidas por la rúbrica. Para ejecutarlas y validar que ninguna funcionalidad matemática o de validación se haya roto, asegurate de tener instalada la librería `pytest` y corré este comando en la terminal (estando dentro de la carpeta del proyecto):

```bash
pytest test_operaciones.py
```
Si todo está correcto, la consola imprimirá `7 passed`.
