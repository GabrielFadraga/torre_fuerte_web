cd link_bio
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
rm -rf public
export REFLEX_LOGLEVEL=default
reflex init
API_URL=https://torrefuerteweb-production.up.railway.app reflex export --frontend-only
unzip frontend.zip -d public
rm -f frontend.zip
deactivate