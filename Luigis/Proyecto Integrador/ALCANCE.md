# ALCANCE E IDEA DEL PROYECTO (Etapa 2)
## Sistema de Seguimiento de Entrenamientos - LUIGI'S

A partir del principio de continuidad, para esta segunda etapa mantenemos el dominio y las reglas de negocio de nuestro Sistema de Seguimiento de Entrenamientos. Sin embargo, el prototipo evoluciona para dejar de ser volátil y transformarse en un sistema capaz de conservar información, trabajar con datos históricos y recuperar datos de ejecuciones anteriores. Para lograrlo, reemplazamos la matriz de la primera etapa por el uso de diccionarios en memoria y persistencia en múltiples archivos.

### 1. Archivos, Configuración y Persistencia

El sistema incorpora un acceso inicial restringido mediante un login. Para ello, se leerá un archivo `usuarios.csv` con formato de texto separado por punto y coma, que contendrá estrictamente dos campos: `usuario` y `contraseña`.

Los parámetros del club dejarán de estar fijos en el código y se cargarán desde un archivo `configuracion.json` al iniciar el programa. Su estructura concreta contendrá las siguientes claves y valores:
* `"MAXIMO_DIARIO": 180`
* `"OBJETIVO_SEMANAL": 150`
* `"CATEGORIAS_ADMITIDAS": ["Infantiles", "Cadetes", "Juveniles", "Mayores"]`

En caso de que este archivo falte o su formato sea inválido, el sistema no lo reemplazará silenciosamente ni utilizará valores por defecto: atrapará la excepción (`FileNotFoundError`, `ValueError`, `OSError`), informará claramente el error crítico por pantalla al usuario y detendrá la ejecución del programa para resguardar la consistencia de las reglas del negocio.

Para solucionar la pérdida de datos y detectar a los atletas sin actividad, la persistencia se dividirá en dos estructuras:
* Un archivo `atletas.csv` que funcionará como padrón maestro. Almacenará a todos los deportistas registrados para no perder a aquellos con 0 minutos entrenados. Sus columnas serán: `codigo_atleta`, `nombre` y `categoria`.
* Un archivo `registros.csv` que funcionará como el historial de actividad. Para evitar inconsistencias y no duplicar información, sus columnas serán estrictamente: `codigo_atleta`, `fecha` y `minutos`. La categoría correspondiente a cada entrenamiento se obtendrá cruzando los datos en memoria con el archivo `atletas.csv`.

En memoria, estructuraremos la información convirtiendo cada fila leída en un diccionario de registro y utilizaremos diccionarios acumuladores para agrupar los totales. Asimismo, utilizaremos un conjunto (`set`) para almacenar de forma eficiente los códigos únicos de los atletas que registraron actividad.

### 2. Reglas de Negocio y Validaciones

Se mantiene el máximo diario de 180 minutos. Dejamos explícito que este límite corresponde al total acumulado por un atleta en un mismo día, y que el valor exacto de 180 minutos es válido. Si se registran varias sesiones para un mismo deportista en la misma jornada, la suma matemática de estas se rechazará únicamente si supera dicho tope (por ejemplo, si el acumulado llega a 181 minutos o más).

Las validaciones de formato incorporan el uso de expresiones regulares (`re`) para datos clave:
1. La estructura del código de atleta (una letra mayúscula y dos números, ej: `A01`).
2. El formato del nombre de usuario en el login, el cual exigirá un patrón estrictamente alfanumérico, sin espacios ni caracteres especiales, con una longitud de entre 4 y 10 caracteres (ej: `admin123`).
3. El formato de la fecha de entrenamiento, validando la estructura de fecha completa `DD/MM/AAAA` (ej: `05/10/2024`).

El ingreso de datos numéricos y la gestión de archivos contarán con el tratamiento obligatorio de excepciones (`try-except`) para atajar errores de lectura (`FileNotFoundError`, `OSError`), escritura y formatos inválidos (`ValueError`).

### 3. Reportes Requeridos

Adaptamos los informes a la nueva estructura histórica para ofrecer los cuatro reportes requeridos:
1. **Reporte filtrado:** Consulta detallada de la ficha e historial de un atleta puntual. Recuperará el Nombre y la Categoría desde el archivo `atletas.csv`, y consolidará el detalle de minutos por fecha y su total histórico cruzando los datos con `registros.csv`.
2. **Reporte general:** Totales e indicadores globales calculados sobre todo el historial por categoría admitida.
3. **Reporte de alertas:** Listado de atletas que no alcanzaron el objetivo semanal de 150 minutos. Para evaluar un período concreto sobre fechas reales, el sistema solicitará al usuario ingresar el rango semanal a través de una fecha de inicio y una fecha de cierre (período de 7 días, formato `DD/MM/AAAA`). El reporte incluirá explícitamente a todos los atletas que no alcancen la meta, contemplando a aquellos deportistas registrados en el padrón que tengan 0 minutos o no hayan registrado actividad en ese lapso. La salida de esta alerta se exportará a un archivo de texto `reporte.txt`.
4. **Resumen de únicos:** Listado y conteo de atletas únicos que han registrado entrenamientos, obtenido a través de las propiedades del conjunto (`set`).

### 4. Recursividad y Pruebas Unitarias

Para la localización cotidiana de atletas, el sistema utiliza el acceso directo por clave que brindan los diccionarios en memoria. No obstante, para cumplir con el contenido pedagógico de recursividad exigido por la cátedra de manera justificada, se implementa una función recursiva de búsqueda lineal sobre la lista de códigos registrados. Su caso base está claramente definido: retorna `False` si se recorrió la colección sin encontrarlo, y retorna `True` si el código en la posición actual coincide con el buscado, justificando el paso recursivo de avanzar al siguiente índice.

Por último, el sistema incorpora siete pruebas unitarias automatizadas mediante la librería `pytest` que verificarán, sin requerir interacción por pantalla (`input`) ni depender de impresiones (`print`):
1. Una validación de formato correcta (código de atleta con Regex).
2. Una validación incorrecta que produzca una excepción controlada (`TypeError`).
3. Un cálculo simple de cumplimiento del objetivo semanal.
4. La acumulación correcta de minutos agrupados por la clave del atleta.
5. La detección exitosa de la condición crítica (alerta de objetivo no cumplido).
6. La correcta ejecución y caso base de la función recursiva de búsqueda.
7. Un caso límite matemático: la validación del tope diario, comprobando que un acumulado exactamente igual a 180 minutos es aceptado, mientras que un valor superior (181 minutos) es rechazado.

Quedan fuera de alcance las interfaces gráficas, bases de datos externas o cualquier funcionalidad no especificada explícitamente en este documento.