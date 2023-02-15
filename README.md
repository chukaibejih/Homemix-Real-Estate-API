
Homemix - A Real Estate API (This project is still a work in progress).
========

Homemix is a RESTful API that enables users to buy and sell properties with ease. It provides endpoints for CRUD operations on real estate listings, making it simple for users to create, read, update, and delete listings.

With Homemix, users can list properties with detailed information, including property type, address, price, size, number of bedrooms and bathrooms, description, photos, availability, and contact information. This makes it easy for potential buyers to search for properties that meet their specific needs and requirements.

Homemix also provides advanced search and filtering capabilities, allowing users to search for properties based on parameters such as location, price, number of bedrooms, and more. The API supports pagination for large datasets, with customizable page size and page number parameters, making it easy to view large amounts of data.

Users can register as either a buyer or seller and are provided with secure authentication and authorization through the use of token-based authentication. This ensures that only authorized users have access to sensitive information and the ability to manipulate data.

Homemix is built with Django Rest Framework (DRF), a powerful and flexible framework for building APIs in Django. This makes it easy to extend and customize the API to meet specific needs, and provides comprehensive documentation and examples to get you started quickly.

With its advanced search and filtering capabilities, secure authentication, and support for multiple media types, Homemix is the ideal solution for anyone looking to buy or sell properties with ease.

In addition to the features mentioned above, Homemix now also includes a referral system. Users can generate a unique referral code and share it with their friends or family. When a new user signs up using the referral code, both the referring user and the new user receive a reward or incentive.

Users can view a list of all the users they have referred, providing transparency and accountability. This encourages existing users to invite others to the platform and helps to grow the user base.

Overall, Homemix offers a comprehensive solution for buying and selling properties, with a user-friendly interface and advanced features to make the process as smooth and efficient as possible.

Technical Overview
------------------

The platform uses the following technologies to gather and display the pricing data:

-   Django: A web framework used to handle the back-end and interact with the database.
-   Uses Django RestFramework for building RESTful APIs
-   Implements standard HTTP methods (GET, POST, PUT, DELETE) for interacting with the API.
-   Database: To store the user and property data for quick and easy retrieval.
-   Supports authentication and authorization using Simple JWT. A JSON Web Token authentication plugin for the Django REST Framework.
-   Serialization of data using DRF's serializers
-   Supports pagination of results using DRF's built-in pagination classes
-   Provides documentation of the API using drf-yasg - Yet Another Swagger Generator. 

Why Homemix?
--------

The creation of Homemix is a personal project for me as it has roots in my family's background in the real estate industry. Growing up, my parents ran a traditional real estate business and I have always wanted to create something that would solve some of the problems they faced and make their work easier.

I saw an opportunity to use my skills in software development to build an API that would streamline the process of buying and selling properties. With Homemix, I aim to provide users with an intuitive and user-friendly platform that makes it easy to list properties and search for properties that meet their needs.

The project holds a special place in my heart because it allows me to give back to my parents and the real estate community. I am passionate about creating a clean, well-secured API that will make a positive impact on the industry. I believe that the features and capabilities offered by Homemix will greatly benefit both buyers and sellers, and I am excited to see the impact it will have.

In short, Homemix is a project that brings together my passion for real estate and my skills in software development. I am confident that it will make a positive difference in the industry and I look forward to seeing it grow and evolve over time.

Installation
------------

Here are the steps to install and set up the Homemix real estate API project locally:

1. Clone the repository: First, you will need to clone the Homemix repository to your local machine. This can be done using the following command in your terminal or command prompt:
    ```bash
    git clone https://github.com/[your-username]/homemix.git
    ```
2. Create a virtual environment: It is recommended to work with a virtual environment to keep the dependencies for this project separate from other projects on your system. To create a virtual environment, run the following command:
    ```bash
    python -m venv homemix-env
    ```
    Activate the virtual environment by running the following command:
    ```bash
    source homemix-env/bin/activate (for Mac or Linux)
    ```

    ```bash
    source homemix-env\Scripts\activate (for Windows)
    ```
3. Install dependencies: Next, you will need to install the dependencies required for the project. These dependencies are listed in the requirements.txt file. To install them, run the following command:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the database: The Homemix API uses the Django ORM to interact with a database. By default, the project uses PostgreSQL as the database or you could use any database of your choice. Run these commands to make migrations:
     ```bash
    python manage.py makemigrations
    ```
  
    ```bash
    python manage.py migrate
    ```
5. Create a superuser: To access the Django admin interface, you will need to create a superuser. You can do this by running the following command:
    ```bash
    python manage.py createsuperuser
    ```
6. Run the development server: Once the installation and setup are complete, you can start the development server by running the following command:
    ```bash
    python manage.py runserver
    ```
  
  The Homemix API should now be running at http://localhost:8000/. You can access the Django admin interface at http://localhost:8000/admin/.
  
Contributing / Reporting issues
------------

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License
-----

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

