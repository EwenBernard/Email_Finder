# Email_Finder  

**Email_Finder** is a web application for finding and validating email addresses. It reconstructs potential email addresses based on a user’s name and company, checks their validity, and provides a user-friendly Vue.js interface for easy management and visualization.  

![](https://github.com/EwenBernard/Email_Finder/blob/main/demo_gif.gif)

## Features  
- **User-Friendly Interface**: Built with Vue.js, HTML, CSS, and JavaScript for a clean and efficient front-end.  
- **Email Reconstruction and Validation**: Automatically generates and tests possible email addresses from user and company information.  
- **Database Integration**: Stores names, reconstructed emails, and validation flags in SQLite.  
- **API-Driven Backend**: A Django-based RESTful API handles all operations between the front-end and the database.  
- **Containerized for Portability**: Fully containerized with Docker, making it easy to deploy and run.  

## Tech Stack  
- **Frontend**: Vue.js, HTML, CSS, JavaScript  
- **Backend**: Django  
- **Database**: SQLite  
- **Containerization**: Docker
- **CI/CD Pipeline**: Github Action for automated build, deployment and testing using selenium

## How to Run  
1. **Clone the Repository**  

2. **Build and Run with Docker**  
   - Build the Docker image:  
     ```bash  
     docker build -t email_finder .  
     ```  
   - Run the container:  
     ```bash  
     docker run -p 8000:8000 email_finder  
     ```  

3. Alternatively, pull and run from Docker Hub:  
   ```bash  
   docker pull email_finder  
   docker run -p 8000:8000 email_finder  
   ```  

4. Open your browser and navigate to `http://localhost:8000` to access the application.  

## Authors  
Nathan WANDJI - Ewen BERNARD



