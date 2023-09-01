set -o errexit

pip install -r requirements.txt
npm install webpack webpack-cli webpack-obfuscator --save-dev
npm install javascript-obfuscator --save-dev
npm fund
npx webpack --config webpack.config.js
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
