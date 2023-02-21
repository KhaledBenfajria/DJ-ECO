from setuptools import setup, find_packages


setup(
    name='Django-ecommerce',
    version="1.1.136",
    description='Django Ecommerce',
    author='Khaled Benfajria',
    author_email='benfajria.khaled11@gmail.com',
    url='https://github.com/KhaledBenfajria/DJ-ECO.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'autopep8==1.4.4', 'certifi==2019.3.9', 'chardet==3.0.4', 'defusedxml==0.6.0', 'Django==2.2.14',
        'django-allauth==0.39.1', 'django-countries==5.3.3', 'django-crispy-forms==1.7.2', 'django-debug-toolbar==1.10.1',
        'idna==2.8', 'oauthlib==3.0.1', 'pep8==1.7.1', 'pycodestyle==2.5.0', 'python-decouple==3.1', 'python3-openid==3.1.0',
        'pytz==2018.5', 'requests==2.21.0', 'requests-oauthlib==1.2.0', 'sqlparse==0.2.4' ,'stripe==2.27.0',
        'urllib3==1.24.2', 'Pillow'
    ],
)
