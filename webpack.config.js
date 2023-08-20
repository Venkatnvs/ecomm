const path = require('path');
const fs = require('fs');
const JavaScriptObfuscator = require('webpack-obfuscator');

// Directory containing your JavaScript files
const jsFilesDir = path.resolve(__dirname, './staticfiles/main/js');

// Generate entry points for all JavaScript files in the directory
const entryPoints = {};
fs.readdirSync(jsFilesDir).forEach(file => {
    if (file.endsWith('.js')) {
        const fileName = file.replace('.js', '');
        entryPoints[fileName] = path.join(jsFilesDir, file);
    }
});

module.exports = {
    mode: 'production', // or 'development'
    entry: entryPoints,
    output: {
        filename: '[name].obfuscated.js',
        path: path.resolve(__dirname, 'staticfiles/main/js')
    },
    module: {
        rules: [
            // Add any necessary loaders here
        ],
    },
    plugins: [
        new JavaScriptObfuscator({
            rotateUnicodeArray: true,
        }),
    ],
};

