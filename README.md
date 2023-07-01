### Create a venv

```bash
python -m venv venv/
```
or if You have multiple python version installed
```bash
py -3.11 -m venv venv/
```
### Activate the venv

```bash
.\venv\Scripts\activate
```
### install this

```bash
pip install flask httpx datetime
```
### Create a requirements.txt

```bash
pip freeze > requirements.txt
```
### Create a Procfile & add this in the file (for heroku host)

```bash
web: gunicorn greeting:app
```

# Now use any hosting you want.