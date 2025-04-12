# CSCTF Portal
A simple VueJS and FastAPI based platform to present CTF challenges to a single group of ctf
participants. Challenge data is provided through a single json file that is read in at the
first start of the application. Participants receive a group account that they can use to login
to the portal and start solving CTF challenges. Flags are also submitted through the portal.
For each challenge, the following information is displayed:
- Title
- Description
- Degreee of difficulty
- Story of the challenge

## Deployment
### Requirements
- Python3
- Docker

### Presquisites - Backend
**Prepare the challenge data**  
Copy the example challenge file
```bash
cp backend/challenges.json.example backend/challenges.json
```
and fill in the challenge data for each challenge.  

**Prepare the docker.env file**  
Copy the example .env file
```bash
cp backend/.env.example backend/docker.env
```
and fill in the requirement environment variables.  
To generate a password hash, run the `hash.py` script from the `util` folder:
```bash
pip install argon2-cffi
python3 util/hash.py changeMe
```
and copy it to the `FASTAPI_CSCTF_USER_PASSWORD` environment variable.  
Be sure to escape all 5 dollar sings `$` in the hash using another dollar sign to prevent them from being interpreted
as variables by docker.

### Presquisites - Frontend
Copy the example .env file
```bash
cp frontend/.env.production.example frontend/.env.production
```
and fill in the requirement environment variables.

### Actual deployment
Build the docker containers and run them using docker compose
```bash
docker compose build
docker compose up -d
```