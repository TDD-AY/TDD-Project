# Plantilla del curso programación para QA

Plantilla para el [curso de desarrollo para QA](https://jj.github.io/curso-tdd)

## Descripción del proyecto

Problema que queremos resolver: Nos ha interesado estudiar la evolución de una recuperación, estudiando para ello, cómo evoluciona
la capacidad de recorrer una determinada ruta en días consecutivos. 

Solución que proponemos: Utilizar la API de telegram y las funcionalidades que ofrece para recoger información de recorridos
y procesarlas para mostrar información al usuario.

## Herramientas que se usan en el proyecto

- Lenguaje: Python y JS
- Librerias de python para telegram: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Configuración remota: [etcd](https://etcd.io/)
- Web server para la API: [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- Base de datos: Postgresql
- Frontend: [Vue.js](https://vuejs.org/) SPA hosteado en Github Pages. [Tailwind](https://tailwindcss.com/) como framework de CSS.
- Sistema de logging: [LogDNA](https://logdna.com/)

Discutido en este [issue](https://github.com/TDD-AY/TDD-Project/issues/5)

## Estructura del proyecto

Hemos separado nuestro proyecto en dos carpetas siguiendo un estilo de monorepo.

- En la carpeta [frontend](https://github.com/TDD-AY/TDD-Project/tree/yabir-skeleton/frontend) 
hemos colocado todos los archivos relativos al frontend que por ahora es un archivo de js 
básico y un html con las librerías de js que necesitamos.

- En la carpeta [src](https://github.com/TDD-AY/TDD-Project/tree/yabir-skeleton/src) hemos
colocado nuestro código del servidor donde tenemos el código de nuestro bot y el código de 
nuestra API. Además se incluye el módulo común para comunicarse con la abstracción en la 
base de datos y el archivo de dependencias del proyecto.

## Miembros del equipo

- Yábir García [@yabirgb](https://github.com/yabirgb)
- Alejandro Alonso Membrilla [@aalonso99](https://github.com/aalonso99)
- Pilar Navarro Ramírez [@pilarnavarro](https://github.com/pilarnavarro)
- Juan José Herrera Aranda [@KieDie](https://github.com/Kiedie)

