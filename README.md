# Catalyst-count application
## Installation

### Prerequisites

#### 1. Install Python
Install ```python-3.7.2``` and ```python-pip```. Follow the steps from the below reference document based on your Operating System.
Reference: [https://docs.python-guide.org/starting/installation/](https://docs.python-guide.org/starting/installation/)

#### 2. Install Postgrsql on windows
Install any versiobn of ```postgrsql```. Follow the steps form the below reference document based on your Operating System.
Reference: [https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql/](https://www.postgresqltutorial.com/postgresql-getting-started/install-postgresql/)
#### 3. Setup virtual environment
```bash
# Install virtual environment
pip install virtualenv
```

#### 4. Clone git repository
```bash
git clone "https://github.com/SanketJagadale/Catalyst-Count.git"

# Create virtual environment
py -m venv env

# Activate virtual environment
env\Scripts\activate
```

#### 5. Install requirements
```bash
pip install -r requirements.txt
```

#### 6. Edit project settings
```bash
# open settings file
catalyst_count_main/settings.py

# create .env file in your main folder catalyst-count
SECRET_KEY='your_secret_key'
DEBUG=on

Database Configuration
DB_NAME=your_DB_name
DB_USER=your_DB_user
DB_PASSWORD=your_DB_password
DB_HOST=localhost
DB_PORT=5432

#google Oauth
GOOGLE_OAUTH_CLIENT_ID=your_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret_key


# Edit Database configurations with your postgrSQl configurations.
# Search for DATABASES section.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}
```
#### 7. Run the server
```bash
# Make migrations
python manage.py makemigrations
python manage.py migrate

# Run the server
python manage.py runserver

# your server is up on port 8001
```
Try opening [http://127.0.0.1:8000](http://127.0.0.1:8000) in the browser.
Now you are good to go.
