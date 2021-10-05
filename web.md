Belenios Web Server
===================


Guía del administrador electoral
------------------------------

### Configurar una nueva elección

Una vez que el servidor está en funcionamiento (vea a continuación), cualquier persona que pueda iniciar sesión en el servidor como administrador puede crear una elección. Primero el administrador tiene que elegir cómo se manejarán las credenciales:

 * En el modo automático, el servidor generará credenciales y envíará por correo los códigos privados a cada votante. Recuperación de credenciales (es decir, un votante que  pierde / no recibe su credencial): no es posible en este caso;
 * en el modo manual, un tercero generará credenciales utilizando una interfaz web o la herramienta de la línea de comandos (command-line tool), y carga las credenciales públicas al servidor. Depende de este tercero enviar credenciales privadas a cada votante e implementar la recuperación de credenciales.

Además, el administrador tiene que elegir el modo de autenticación para los votantes:

 * Con el modo de contraseña, el servidor generará contraseñas y las enviará por correo a los votantes, este es el modo más común;
 * el otro usa un servidor [CAS](https://www.apereo.org/projects/cas).

Luego, el administrador debe:

 * establecer el nombre y la descripción de la elección;
 * editar preguntas;
 * editar votantes, y hacer que el servidor les envíe su contraseña si se ha elegido este modo de autenticación;
 * hacer que la autoridad de credenciales genere credenciales y envíe correos electrónicos. En el modo automático, esto se hace simplemente haciendo clic en un botón.En el modo Manual, se genera un enlace para la autoridad de credenciales;
 * (Opcionalmente) Editar fedatarios. Para una mejor seguridad, debe haber al menos dos fedatario. Se genera un enlace para cada fedatario;
 * Validar la elección.

Cada "enlace" anterior debe ser enviado por el administrador a su destinatario previsto.Cada enlace conduce a una interfaz que ayudará a su destinatario a lograr su tarea.

La *huella digital de elecciones*, que se muestra en la página electoral, es la codificación Base64 compacta del SHA256 del archivo 'election.json`. Se puede calcular a partir de una shell POSIX:

    sha256sum | xxd -r -p | base64 | election.json

### Ciclo de vida electoral

Una elección comienza por estar en preparación (o "modo de borrador"), entonces se valida. Luego, se abre inmediatamente y se puede cerrar y volver a abrir a voluntad.Cuando está cerrada, el administrador de elecciones puede iniciar el proceso de escrutinio. La cuenta cifrada se calcula y se publica. Después de que cada fedatario haya calculado su parte del descifrado, el administrador activa la liberación del resultado.

En cualquier momento, se puede archivar una elección validadada. Esto libera algunos recursos en el servidor y hace que la elección sea de solo lectura. En particular, ya no es posible votar en  una elección archivada. Tenga cuidado, esta operación no es revertible.

### Auditando una elección

Durante la elección, se publican los siguientes archivos:

 * `election.json`: election parameters
 * `trustees.json`: claves públicas de los fedatarios
 * `public_creds.txt`: las claves públicas asociadas a credenciales válidas.
 * `ballots.jsons`: boletas aceptadas

Los archivos son accesibles desde la parte inferior de la página electoral. Juntos, permiten a alguien auditar la elección. Al final de la elección, se publica un archivo  adicional `result.json` con el resultado y otras pruebas criptográficas para que se pueda comprobar que todo salió bien.

Consulte la guía del auditor en la documentación de la herramienta de línea de comandos para obtener más información.


Guía del administrador del servidor
----------------------------

Un servidor web de muestra se puede ejecutar con el script `demo/run-server.sh`, desde el árbol de origen compilado.

Aquí hay un extracto del archivo de configuración de muestra:

    <eliom module="_build/src/web/server.cma">
      <auth name="demo"><dummy/></auth>
      <auth name="local"><password db="demo/password_db.csv"/></auth>
      <source file="../belenios.tar.gz"/>
      <log file="_RUNDIR_/log/security.log"/>
      <spool dir="_RUNDIR_/spool"/>
    </eliom>

Los elementos `<auth>` configuran la autenticación para todo el sitio. Métodos de autenticación disponibles:

 * `<dummy>`: solo pregunta por un nombre. No se pretende ninguna seguridad. Esto es útil para fines de depuración o demostración, pero obviamente no es adecuado para la producción.
 * `<password>`: autenticación basada en contraseña. Toma como parámetro un archivo, en formato CSV, donde cada línea consiste en:
    + un nombre de usuario
    + un "salt"
    + SHA256 ("salt" concatenado con contraseña)

  Se ignoran campos adicionales. En el archivo de muestra `password_db.csv`, se incluye un cuarto campo con la contraseña de texto simple. El archivo de muestra se ha generado con el siguiente comando Shell:

   `for u in $(seq 1 5); do SALT=$(pwgen); PASS=$(pwgen); echo "user$u,$SALT,$(echo -n "$SALT$PASS" | sha256sum | read a b; echo $a),$PASS"; done`

 * `<cas>`: autenticar con un servidor [CAS](https://www.apereo.org/projects/cas). Por ejemplo:

   `<auth name="example"><cas server="https://cas.example.com/cas"/></auth>`

   Si el servidor web está detrás de un proxy inverso, es posible que se necesite para reescribir las URL pasadas al servidor CAS.Esto se puede hacer con la siguiente directiva:

   `<rewrite-prefix src="https://backend-server" dst="https://frontend-server/belenios"/>`

 * `<oidc>`:autenticar con un servidor [OpenID Connect](http://openid.net/connect/). Por ejemplo:

   `<auth name="google"><oidc server="https://accounts.google.com" client_id="client-id" client_secret="client-secret"/></auth>`

   En lo anterior, `client-id` y `client-secret` debe ser reemplazado por credenciales válidas emitidas por el proveedor OpenID Connect.

   La directiva `<rewrite-prefix>` también se aplica a este esquema de autenticación.

El elemento`<source>` da el path al tarball. Tenga en cuenta que esta es una ruta en el sistema de archivos local y no es una URL. 

El elemento `<log>` indica un archivo donde se registrarán algunos eventos sensibles a la seguridad. Es opcional.

El elemento `<spool>` indica un directorio con datos de elecciones. Este directorio debe estar vacío cuando el servidor se inicie por primera vez, y se rellenará con los datos de las elecciones. Una ubicación típica sería `/var/lib/belenios`. ADVERTENCIA: Puede contener datos confidenciales (por ejemplo, la clave privada cuando no se establecen fedatarios externos).