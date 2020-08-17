from flask_assets import Bundle

bundles = {
    'app_js': Bundle(
        'js/app.js',
        output='dist/app.js',filters="jsmin"),
    'app_scss': Bundle(
        'scss/icons/material-design-iconic-font/css/materialdesignicons.min.css',
        'scss/icons/themify-icons/themify-icons.css',
        'scss/animate.css',
        'scss/spinners.css',
        'scss/style.css',
        'scss/app.scss',
        output='dist/app.css',filters="pyscss")
}