## Project Overview
This is a Django REST Framework API that processes user data from a CSV file. It validates fields for name, email, and age, and handles duplicate email addresses gracefully.

## Setup and How to Run
**Clone the repository**
git clone https://github.com/ThomasBaby27/django-csv-api-task.git
cd api_assessment

**Set up the virtual environment**
python -m venv env
env\Scripts\activate

**Install Dependencies**
pip install django djangorestframework

**Run Migrations**
python manage.py makemigrations
python manage.py migrate

**Start the Server**
python manage.py runserver

**Features**
Validation: Ensures non-empty names, valid emails, and age between 0-120.
Constraints: Accepts only .csv files and skips duplicate emails.
Others: Uses DRF Serializers and includes unit tests.

**Testing**
python manage.py test

**API Testing (Postman)**
Method: POST
URL: http: //127.0.0.1:8000/api/upload-csv/
Body Type: form-data
Key: files (change the type from text to file)
Value: Select .csv file
