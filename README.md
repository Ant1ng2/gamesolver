# Gamesolver
## Setup
We'll be using [```virtualenv```](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) to load all the dependencies. 

From there you can execute the following commands from the root directory:
```
python -m venv <name of venv>
source venv/bin/activate
pip install -r requirements.txt
cd web
python manage.py runserver <port-number>
```

If all goes well, you should be able to see the web app on your `localhost`.
