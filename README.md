# MiniOffice

## Description

For my final project, I chose a simple but very helpful idea: a web app to manage a small company. This app is designed to run locally and provides basic functionality for managing people, tasks, and projects within a small office environment.

## Features

This web app includes six pages that allow the user to:

- View a dashboard with summaries (Home Page)
- Edit the information of the admin user
- Add, modify, delete, and track employees — with the ability to contact them via WhatsApp
- Add, modify, delete, and track tasks
- Add, modify, delete, and track projects
- Add, modify, delete, and track contacts — also with WhatsApp integration

## Technologies Used

- HTML
- CSS
- JavaScript
- Python (Flask)
- SQL (SQLite)

## File Overview

- `app.py`: The main Flask application that handles routes and logic.
- `database.db`: SQLite database with tables for employees, tasks, projects, and contacts.
- `templates/`: HTML files rendered via Jinja2.
- `static/css/`: Custom CSS styles for each page.
- `static/js/`: JavaScript used for front-end interactions.
- `static/imgs/`: Images used across the site.

## How It Works

When the app is run locally using `app.py`, Flask starts a local development server. The home page shows statistics and summaries. Navigation links allow access to tasks, contacts, employees, and projects. Each page allows CRUD operations (Create, Read, Update, Delete). Data is stored in a local SQLite database. Communication with employees or contacts is done through WhatsApp links.

## Design Decisions

I chose Flask for its simplicity and flexibility. Using SQLite allows easy local storage without needing a server. Font Awesome was used for consistent icons. I used separate stylesheets for each page to make the CSS easier to manage. Jinja2 templates made it easier to reuse layout components across multiple pages.

## Challenges

One challenge was designing a database schema that supports relationships between tasks, projects, and contacts. Another issue was updating the frontend dynamically without reloading the whole page. Debugging Flask route issues also required time and trial/error.

## Future Work

In the future, I would like to add:
- Authentication with admin login
- Hosting the app online
- File upload support for employee records
- Progress tracking for tasks and projects

## What I Learned

This project helped me practice everything from front-end design to server-side logic. I improved my Flask skills, understood SQL relationships better, and gained confidence in debugging full-stack apps. I also learned how to organize larger codebases and work with templates and routing.


## Credits

- Icons by [Font Awesome](https://fontawesome.com/)
- Special thanks to [Elzero Web School](https://elzero.org) and the CS50 team for providing the knowledge that helped me build this project.

