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
<hr>

###### Note: make sure you put your fb group api access token in hosting provider environment variable

variable name : `ACCESS_TOKEN` & value : `your_access_token`

### To Get FB Access Token

- make an app and visit https://developers.facebook.com/tools/explorer/
- select your app name & select `user token`
- add these permissions = 
  - user_photos
  - user_posts
  - user_managed_groups
  - groups_show_list
  - publish_to_groups
  - groups_access_member_info
  - public_profile
- make sure you have Graph api advanced previlage access
- now generate access token (extend your access token validity -- google it how)


# Now use any hosting you want.