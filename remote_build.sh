cd link_bio
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
rm -rf public
export REFLEX_LOGLEVEL=default
reflex init
API_URL=gabriel-20mrw5de.b4a.run/ reflex export --frontend-only
unzip frontend.zip -d public
rm -f frontend.zip
deactivate