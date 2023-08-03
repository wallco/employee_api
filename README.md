# Hired Employees Rest API - Coding Challenge (Globant)

This repository was built and documented as a proposed solution for Globant's Coding Challenge. All code described above can be viewed in this repository.

## Section 1 - REST API

The first section of the test consists in building an API to receive data and load it into a SQL Database in the context of DB migrations.

The data load is to be done via CSV files to be uploaded to the DB, and the transactions must be done in batches of up to 1000 records per HTTP Request.

For this solution, i have chosen to use the Python programming language, as well as the Django, a very robust and popular framework for API building. Django supports the use of simple Jinja2 HTML templates which were used to build an interface. I used a simple SQLite3 database for development purposes.

I considered the interface relevant because the case did not specify who would be in direct contact with the application, so i chose to make it friendly and independent from any external tools such as managing HTTP Requests or specialized Data Visualization Tool. This way, i built this app considering the principle of self service, so any non-technical member of the company could hypothetically upload said data and view the result endpoints.

Django works with the concept of Models (which represent database entities), Views (which dictate the business rules for processing the requests and delivering the results) and Templates (HTML files to render the results delivered by the Views - In this case, following the Jinja2 engine.)

For the first section, i built the Models for the database entities - Hired Employees, Departments and Jobs, reflecting the according fields. I then implemented the respective View (UploadView), which accepts both GET and POST requests. The GET requents shows a page prompting the user to upload the CSV file and click on the corresponding button (Departments/Jobs/Employees) to trigger the POST request, which is then processed accordingly by the same view. The CSV file is transformed into a list of Django Model objects in runtime (considering which type of data the user gave as input) which is then bulk upserted into the DB. I used the library django-bulk-update-or-create for this, as this method is not natively available in Django.

This endpoint's relative path is /upload.

## Section 2 - SQL

It was also a requirement to explore the data inserted in the previous section. As aforementioned, i decided to use HTML rendering so the data would be directly available to any possible stakeholder.

For the two endpoints required, i created two corresponding new Views and Jinja2 Templates. Both of the views only accept GET requests. On access, the views execute corresponding fixed queries (harnessing Django's functionality to import its default connection and execute raw SQL), and the requested data is then rendered and presented to the user in the form of a table.

## Bonus track - Cloud, testing and containers

I did not have the time to complete the bonus requirements, but i will briefly elaborate on what would be my approach.

* For hosting the architecture, my go-to cloud provider is AWS, simply because i currently have more experience in it. As this is a modulated REST API, there would be various ways to deploy this, such as ECS (After the conteinerization was done) or EC2. Of course, it would also be important to configure a webserver so the API could be accessed from outside the corresponding EC2/ECS instance. Just like with the database, Django allows this to be done in a relatively simple way with some tweaks in the settings.py file.

* For testing, i would use the PyTest library, as i find it has a nice balance between simplicity and robustness.

## Next steps

Finally, considering time was a considerable constraint in this challenge, there are some aspects that could have been done in a more robust way. I will list some changes that i recognize would make this API considerably better.

* Logging - Storing a controlled amount of files uploaded could allow easier debugging for data problems.

* Better treatment of null values - I noticed there are a considerable amount of null values in the files. Considering Section 2 involved aggregations and metrics, these null values may cause a severe impact if they go unacounted for. I manage to treat it partly, but it certainly could be improved upon.

* File validation - Both for security and data quality purposes, the uploaded files should be validated more strictly in regards to its extension, content and format to assure it follows correct csv syntax, as well as contains the expected fields and does not have malicious code.

* General feedback/responsiveness - I didn't have time to configure the correct HTTP errors in the Views, and this is important for both the users and developers to grasp a better understand of what's wrong whenever there is a problem. There also could be success and error messages when the user uploads a file so it feels more responsive.

This basically ends the documentation. As aforementioned, all the code described here is in this repository (except environment variables such as the Django Secret Key). Please feel free ask whatever may have been left unclear in our technical interview, where i can better explain the code and show the app working.
