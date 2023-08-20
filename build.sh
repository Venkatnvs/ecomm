set -o errexit

pip install -r requirements.txt
npm install webpack webpack-cli webpack-obfuscator --save-dev
npx webpack --config webpack.config.js
python manage.py makemigrations
python manage.py migrate
