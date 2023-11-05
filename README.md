# UniVerse

<!-- Repository Information & Links-->
<br />

![GitHub repo size](https://img.shields.io/github/repo-size/LeandervanAarde/diasyncserver)
![GitHub watchers](https://img.shields.io/github/watchers/LeandervanAarde/diasyncserver)
![GitHub language count](https://img.shields.io/github/languages/count/LeandervanAarde/diasyncserver)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/LeandervanAarde/diasyncserver)

<!-- HEADER SECTION -->
<h5 align="center" style="padding:0;margin:0;">Leander van Aarde - 200211</h5>
<h6 align="center">DV300 - Term 4 | 2023</h6>
</br>
<p align="center">

  <a href="https://github.com/LeandervanAarde/diasyncserver">
    <img src="https://drive.google.com/uc?export=view&id=1li8QOPWr_fjSb-7JsWC3EIQ4r8Hj5AdW" alt="Logo" width="140">
  </a>

  <p align="center">
   Diasync is an AI-driven self management application for Diabetics. <br>

   <br />
   <br />
    <a href="https://github.com/https://github.com/LeandervanAarde/diasync">Report Bug</a>
    ·
    <a href="https://github.com/https://github.com/LeandervanAarde/diasync">Request Feature</a>
</p>
<!-- TABLE OF CONTENTS -->

## Table of Contents

- :hospital: [About the Project](#about-the-project)
  - :syringe: [Project Description](#project-description)
  - :syringe:[Built With](#built-with)
- :hospital: [Getting Started](#getting-started)
  - :syringe: [Prerequisites](#prerequisites)
  - :syringe: [How to install](#how-to-install)
- :hospital: [Features and Functionality](#features-and-functionality)
- :hospital: [Concept Process](#concept-process)
  - :syringe: [Ideation](#ideation)
  - :syringe: [Wireframes](#wireframes)
- :hospital: [Development Process](#development-process)
  - :syringe: [Implementation Process](#implementation-process)
    - :syringe: [Highlights](#highlights)
    - :syringe: [Challenges](#challenges)
  - :syringe: [Future Implementation](#peer-reviews)
- :hospital: [Conclusion](#conclusion)
- :hospital: [License](#license)
- :hospital: [Contact](#contact)
- :hospital: [Acknowledgements](#acknowledgements)

<!--PROJECT DESCRIPTION-->

## About the Project

<!-- header image of project -->

### Project Description

Diasync is a new and AI-driven self-management web application created with NEXT.JS and Django frameworks to create an exciting and cutting-edge application. This aims at educating and catering a diverse group of Diabetics in order to simplify and ease their management in order to live a long and healthy life

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=15&pause=1000&color=F71D1D&multiline=true&random=false&width=800&height=300&lines=+DISCLAIMER%3A+Diasync+is+not+an+official+or+registered+health+application+if+you+are+having+;problems+with+effective+Diabetes+management%2C+consult+a+healthcare+professional;+Furthermore%2C+this+application+does+not+aim+to+replace+healthcare+professionals%2C;rather+assist+patients+in+gaining+a+better+understanding+of+their+diabetes)](https://git.io/typing-svg)

### Built With

- [NEXT](https://nextjs.org/)
- [Django](https://www.djangoproject.com/)
- [DjangoRestFramework](https://www.django-rest-framework.org/)
- [Pandas](https://pandas.pydata.org/)
- [OpenAiApi](https://openai.com/)
- [TypeScript]()
- [PostgreSQL](https://www.postgresql.org/)
- [pgAdmin](https://www.pgadmin.org/)
- [Aiven](https://aiven.io/)

<!-- GETTING STARTED -->
<!-- Make sure to add appropriate information about what prerequesite technologies the user would need and also the steps to install your project on their own mashines -->

## Getting Started

To get a copied file of this repository, follow the steps below to get it installed on your local machine.

### Prerequisites

Ensure that you [Python 3](https://www.python.org/) installed on your machine. The [GitHub Desktop](https://desktop.github.com/) program will also be required.

### How to install

### Installation

Here are a couple of ways to clone this repo:

1. **GitHub Desktop**
   - Enter `https://github.com/LeandervanAarde/diasyncserver.git` into the URL field and press the `Clone` button.

2. **Clone Repository**
   - Run the following in the command-line to clone the project:
     ```sh
     git clone https://github.com/LeandervanAarde/diasyncserver.git
     ```
   - Open `Software` and select `File | Open...` from the menu. Select the cloned directory and press the `Open` button.

3. **Activate the Virtual Environment**
   Before running the project and installing the dependencies, run the following commands to activate the virtual environment:

   ```sh
   env\Scripts\activate
   ```

   #### NOTE IF YOU ARE RUNNING ON MACOS:
    ```sh
   chmod +x env/Scripts/activate
    ```
then
    ```sh
   bash
    ```
  ```sh
cd path/to/DiasyncServer
```

lastly
  ```sh
source env/Scripts/activate
```

5.  Install Dependencies </br>
    Run the following in the command-line to install all the required dependencies:

    ```sh
    pip install djangorestframework, djangorestframework-simplejwt, openai, python-dotenv faiss-cpu openai huggingface_hub psycopg_binary, pandas, labgchain,django-cors-headers, InstructorEmbedding sentence_transformers, tiktoken
    ```

6.  Contact the [Developer](mailto:200211@virtualwindow.co.za) for API keys that are required or create an OPENAI account for API access or if there are any issues with the dependancies.
7.  Contact the [Developer](mailto:200211@virtualwindow.co.za) for access to the database that is required or create a PostgresSQL database.
8.  if you create your own databases, be sure to add all the migrations with the following commands
    ```sh
       python manage.py makemigrations
    ```
    After migrations are staged, you can run
    ```sh
      python manage.py migrate
    ```
9. If you would like to view your data on the admin panel you can start the project using
    ```sh
      python manage.py runserver
    ```
10. You can then navigate to the admin panel here [AdminPanelLocalLink](HTTP://localhost:8000/admin)
11. Be sure that you have an admin account, you can do that through running
```sh
python manage.py createsuperuser
```
12. Create your super user and remember the credentials, this is how you can view the data!

13.  Ensure that you have Postgres and PgAdmin installed on your machine.
14.  NB: In the env file, make sure your variable name is set equal to OPENAI_API_KEY, otherwise the application will break


## Features and Functionality

<!-- note how you can use your gitHub link. Just make a path to your assets folder -->

## Custom Authentication

### Register new account 
  Registering a new account is fairly straight forward, the user data is collected from the body, but the Users model is extended from the base User class found in Django, here there are a few added fields that are added onto the already existing fields such as email and password

  #### Password hasing 
  All passwords are hashed before users are saved with built in python methods. 

### Custom Login 
  Because Djangos base login is done with a username and password, the login needed a function that overides that and finds the user based on their email, this is because when logging in, the users information is retrieved from the auth_user and not the users table. 

### Token authentication
  Each user has a JWT token assigned to their session based on their email and password, this token is valid for 30 min and once that time expires with no activity, the user will be re-routed to login.
  
### CSV upload 
  Contour testers data is downloadable through their application, however, it is a csv
  - The backend receives a base64 encoded file that is decoded in python and converted to a dataframe using the pandas dependency
  - Once that is done, each instance will created in a for loop and add a row in the database with the relevant formatting of data.
  - This becomes important for the AI integration and the overall application. 



## Models 
 Different models were created for Users and glucose readings, this determines the data structures for all of my data. 

 
## Views 
  Views are essentially the functions that handle of the the data processing from the database to the server, these are defined in the urls.py file to create the API endpoints, by using the HTTP Response and response, I am able to effectively create endpoints that return the correct 
  Http Response with the correct data that the front end needs. 

## AI INTEGRATION 
  The AI integration on this application was achieved through the OPENAI GPT-4 model API, this NLP was queried through a long string and a desired JSON structure that needed to be returned, ofcourse all responses are based off of the users data 
  and example endpoint for this would be : 

  ```sh 
    http://localhost:8000/analyse/?userid=36 <-- Specifyng the user who is currently logged in. 
  ```

### Readings View
  All readings are retrieved by getting the readings and prefetching the related user to all the readings, after all readings are fetched the data can then be filtered correctly based on the url parameter that contains the userid. 

### LANGCHAIN

LangChain was integrated slightly for the chat aspect of the project to keep the AI as content-aware as possible and to return responses based on the logged-in users data. 

<!-- CONCEPT PROCESS -->
<!-- Briefly explain your concept ideation process -->
<!-- here you will add things like wireframing, data structure planning, anything that shows your process. You need to include images-->

## Concept Process

The `Conceptual Process` is the set of actions, activities and research that was done when starting this project.
 - To see the conceptual process and front end outcome of this project, go see the README file on [frontend](https://github.com/LeandervanAarde/diasync)



<!-- DEVELOPMENT PROCESS -->

## Development Process

The `Development Process` is the technical implementations and functionality done in the frontend and backend of the application.
If you would like information about the backend implementation, you can go view the [Server Repo](https://github.com/LeandervanAarde/diasyncserver)

### Implementation Process

<!-- stipulate all of the functionality you included in the project -->
<!-- This is your time to shine, explain the technical nuances of your project, how did you achieve the final outcome!-->

#### The backend

In the backend development process:

1. **DATABASE** In order for this project to work correctly, I decided to use PostGresSQL for the backend implementation. SQL was a better choice as opposed to a document-based approach due to its scalability and relational nature.
2. **DJANGO** Django was a new technology that I wanted to explore considering that python has had such a huge impact on the programming world, this decision was also influenced by my recent exposure to Django in industry. Although I believe
   Django is not very scalable, it was a easy and quick way to build a robust backend and REST API.
3. **ALL ABOUT USERS** This whole project depends on two things, Users and AI. So the creation of users and their data was extremely important, the use of Data science techniques to let users upload their data was extremely useful
4. **Password hashing** Password hashing is extremely important to respect a users rights and data, luckily Django has built in password hashing.
5. **JWT** To ensure user safety, JWTS were incorporated using the simple-jwt dependency for Django, an easy to use and batteries-included dependency.



<!-- stipulated the highlight you experienced with the project -->
### Highlights

- Django was an easy-to-use python web framework that made the process of building a back end fairly easy and quick.
- This is an impactful project I've wanted to do for a long while.
- I enjoyed the simplicity of creating relations between tables.

#### Challenges

<!-- stipulated the challenges you faced with the project and why you think you faced it or how you think you'll solve it (if not solved) -->

- Data upload was probably my biggest challenge, with some inconsistencies still bein there.
- AI integration was a challenge due to its incosistent responses, OpenAI is not considered an AI for this kind of application, however, it did give me the versatility that I needed. Adapting to that was a challenge. However, it still gives extremely valuable insight.
- Syntax adjustment between Python and TypeScript.
- Next and Django are both new technologies that I have not used in the past, so learning these as I went along was a challenge.

### Future Implementation

<!-- stipulate functionality and improvements that can be implemented in the future. -->

- Refinement of the Django code
- Extracting code into methods that I can use throughout the project.
- Code extraction in general
- Better models
- Possibly moving away from Django into something a bit more maintainable like ASP .NET 

<!-- MOCKUPS -->

See the [open issues](https://github.com/LeandervanAarde/diasyncserver/issues) for a list of proposed features (and known issues).

<!-- AUTHORS -->

## Authors

- **Leander van Aarde** - [LeanderVanAarde](https://github.com/LeandervanAarde)

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.\

<!-- LICENSE -->

## Contact

- **Leander van Aarde** - [200211@virtualwindow.co.za](mailto:200211@virtualwindow.co.za)

- **Project Link** - https://github.com/LeandervanAarde/diasync
- **Project Link** - https://github.com/LeandervanAarde/diasyncserver

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

<!-- all resources that you used and Acknowledgements here -->

- [Maxamillian](https://www.udemy.com/course/python-django-the-practical-guide)
- [Django Rest framework](https://www.django-rest-framework.org/)
- [Djamgo Docs](https://www.djangoproject.com/)
- [DjangoJWT](https://www.freecodecamp.org/news/how-to-use-jwt-and-django-rest-framework-to-get-tokens/)
- [DjangoJWT](https://medium.com/@poorva59/implementing-simple-jwt-authentication-in-django-rest-framework-3e54212f14da)
- [StackOverflow](https://stackoverflow.com/)
- [ReinhardtDeBeer](https://github.com/EpicYellow)
