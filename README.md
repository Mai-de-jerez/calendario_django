# Calend-Art™ 📅

Este proyecto es un trabajo real que hice para la subdirectora de la cárcel de Granada. Es un calendario realizado con **Django** y **Full Calendar**. Tiene la peculiaridad de que funciona **sin internet** porque así lo requería el centro. Tiene todos los estilos y fuentes descargados dentro del ejecutable así que no llama a la web en ningún momento conservando los estilos responsivos de **Boostrap** y las fuentes de **Google fonts**. Se compiló con pyinstaller y gracias a la lógica interna implementada no se conecta a internet en ningún momento. Meter aplicaciones que se conecten a la intranet de la cárcel es muy delicado así que me lo pidieron así y asi lo hice.

## Funcionalidades:

- Gestión de Eventos y profesionales que los organiza.
- Cada evento esta ligado a un espacio y uno o varios módulos y cada profesional a un departamento y su vez a un evento.
- Puedes listar, crear, editar o borrar profesionales y eventos desde la interfaz o el admin.
- Distintos roles de usuario.
- Paginación y filtros de búsqueda.
- Renderizado de un fantástico calendario donde mostrar los eventos registrados y cada evento en el calendario se puede clicar y lleva al detalle del mismo.
- Apps para instaurar un sistema de mensajería entre los usuarios registrados.
- Formulario de registro con login y logout.
- Perfil para cada usuario.
- Preguntas de seguridad para recuperación de contraseña.
- Editor de texto enriquecido para los formularios.
  

![Este es el home](capturas/home.png)
![Este es el formulario de registro](capturas/registro.png)
![Perfiles](capturas/perfiles.png)
![Este es el login](capturas/login.png)
![Recuperación de la contraseña](capturas/recuperacion_contraseña.png)
![Vista del día](capturas/vista_dia_calendario.png)
![Vista semana](capturas/vista_semana_calendario.png)
![Calendario con eventos clicables](capturas/calendario_eventos_clicables.png)
![Detalle del evento](capturas/detalle_evento.png)
![Formulario editar evento](capturas/editar_evento.png)
![Listado de eventos con filtros](capturas/filtros_listar_eventos.png)
![Paginación](capturas/paginación.png)


## 💻 Backend
- ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)  
  El corazón del proyecto, un framework de desarrollo web en Python.  

- ![Django CKEditor](https://img.shields.io/badge/Django_CKEditor-5-green?style=for-the-badge&logo=ckeditor&logoColor=white)  
  Para un editor de texto enriquecido en los campos de observaciones de tus modelos.  

- ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)  
  La base de datos ligera para almacenar toda la información de eventos y empleados.  

---

## ✨ Frontend
- ![Bootstrap](https://img.shields.io/badge/Bootstrap_4-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)  
  El framework CSS para un diseño responsivo y profesional.  

- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)  
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)  
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)  
  Los tres pilares de cualquier interfaz web.  

---

## 🗄️ Otros
- ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)  
  Sistema de control de versiones para gestionar los cambios en tu código.  

- ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)  
  Plataforma para hospedar tu repositorio, colaborar y mostrar tu trabajo.


## Úsalo en vivo!!

Para ver el calendario pulsa [aquí](https://may1985.pythonanywhere.com/)

Si quieres acceder como superuser introduce el nombre "superuser" y la contraseña "contraseña". Desde ese acceso podrás acceder al panel de admin y gestionar todo. Puedes crear 
eventos, empleados, nuevos usuarios sin que tengan que pasar por el formulario de registro....barra libre.
Si quieres crearte un usuario y crearte un perfil ve a "Registro" y crea tu perfil, luego accede con tus credenciales.

- Puedes registrar profesionales, departamentos, módulos y lugares, luego puedes registar un evento eligiendo un día y una hora, un módulo o lugar de los existentes, y un responsable
de los existentes en Profesionales.
- El evento se refleajará en el calendario (enlace Calend-Art) y allí podrás ver tus eventos por día, semana o mes, además de pulsarlo y ver el detalle del evento.
- Cada evento y cada profesional tienen su ficha dedicada y cada usuario registrado podrá crear, modificar o borrar solo sus propios eventos, aunque puede ver los de otros
usuarios registrados.
- Diviértete creando eventos, profesionales...p más cosas si accedes como superuser.

## Derechos de autor 🏆

Copyright © 2025 María del Carmen Martín Rodríguez 

Todos los derechos reservados.

[COPYRIGHT](COPYRIGHT)
