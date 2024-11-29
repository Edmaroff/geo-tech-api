<img src="https://img.shields.io/badge/python-3.12-blue" alt="Python version"/> <img src="https://img.shields.io/badge/django-5.1-blue" alt="Django Version"/> <img src="https://img.shields.io/badge/Django%20REST%20framework-3.15-blue" alt="Django REST Framework Version"/> <img src="https://img.shields.io/badge/Pandas-2.2-blue" alt="Pandas Version"/>

<h1>GeoTech API</h1>

<h2>Описание</h2>
<p>GeoTech API — это API приложение для работы с данными станций. Приложение позволяет загружать данные через Excel-файлы, предоставлять их в формате JSON, а также визуализировать данные на HTML-странице</p>



<h2>Функциональность</h2>
<ul>
  <li>Загрузка данных станций через Excel-файл (пример файла: <code>example.xlsx</code>)</li>
  <li>Получение списка станций в формате JSON с поддержкой пагинации</li>
  <li>Визуализация данных в HTML-таблицах</li>
  <li>Документация Swagger для API</li>
</ul>


<details>
  <summary><h2>Технологии</h2></summary>
<ul>
  <li><a href="https://www.djangoproject.com/">Django</a></li>
  <li><a href="https://www.django-rest-framework.org/">Django REST Framework</a></li>
  <li><a href="https://www.postgresql.org/">PostgreSQL</a></li>
  <li><a href="https://pandas.pydata.org/">Pandas</a></li>
  <li><a href="https://drf-spectacular.readthedocs.io/">drf-spectacular</a></li>
  <li><a href="https://www.docker.com/">Docker</a></li>
</ul>
</details>


<h2>Запуск проекта с Docker</h2>
<ol>
  <li>Клонируйте репозиторий:
    <pre><code>git clone https://github.com/Edmaroff/geo-tech-api</code></pre>
  </li>
  <li>Перейдите в директорию проекта:
    <pre><code>cd geo-tech-api</code></pre>
  </li>
  <li>Создайте и заполните файл <code>.env</code> на основе <code>.env.template</code></li>
  <li>Выполните сборку и запуск контейнеров:
    <pre><code>docker-compose up --build</code></pre>
  </li>
</ol>

<h2>Дополнительная информация</h2>
<ul>
  <li>Суперпользователь для административной панели создаётся автоматически:
    <ul>
      <li>Логин: <code>admin</code></li>
      <li>Пароль: <code>admin</code></li>
    </ul>
  </li>
  <li><strong>Django API</strong> доступен по адресу: 
    <a href="http://localhost:8000" target="_blank">http://localhost:8000</a>
  </li>
  <li>Документация Swagger доступна по адресу: 
    <a href="http://localhost:8000/api/docs/" target="_blank">http://localhost:8000/api/docs/</a>
  </li>
</ul>
