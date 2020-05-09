# syncing setup.py with pipfile
set -xe
cd "$(dirname "$0")"
cd ../
pipenv shell || true
pipenv-setup sync --dev --pipfile
