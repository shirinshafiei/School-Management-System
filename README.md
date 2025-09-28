#  School API

This project is a **Django REST API** backend for managing schools, teachers, and students.  
It includes features like news, assignments, chat, and optional GIS-based location services.  

---

##  Features
###  Admin
- Create new schools with name + geographic coordinates  
- Approve/reject teacher & student registrations  
- Manage all lessons, classes, news, and assignments  
- Assign teachers to classes  

###  Teacher
- Register & login with username, password, and national ID  
- Update profile (bio + location)  
- Add students using national ID  
- Create/manage **news** and **assignments** (text, deadline, PDF/ZIP upload)  
- Chat with students (send/receive messages)  
- View nearby schools (GIS)  

### Student
- Register & login with username, password, and national ID  
- View assigned classes, related news, and assignments  
- Submit assignment answers (text, PDF/ZIP)  
- Edit answers before deadline  
- Chat with teachers  
- View nearby schools (GIS)  

---

## 🚀 Deployment Guide  

1. **Install dependencies**  
   Make sure you have the following installed on your system:  
   - [Docker](https://docs.docker.com/get-docker/)  
   - [Docker Compose](https://docs.docker.com/compose/install/)  

2. **Configure environment**  
   - Open the file `settings.template`  
   - Replace the placeholders with your actual values:  
     - `SECRET_KEY`  
     - `DB_NAME`  
     - `DB_USER`  
     - `DB_PASSWORD`  
     - `DB_HOST`  
   - Save it as:  
     ```
     settings.py
     ```  

   - Do the same for `docker-compose.yml.template`:  
     - Replace placeholders with your values  
     - Save it as:  
       ```
       docker-compose.yml
       ```

3. **Initialize your database**  
   Run the migrations inside the container to set up schema:  
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser

### Build & run
   ```bash
   docker-compose up --build
