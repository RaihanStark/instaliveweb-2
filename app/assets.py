from flask_assets import Bundle

bundles = {
    'app_js': Bundle(
        'js/sidebarmenu.js',
        'js/bootstrap-pincode-input.js',
        'js/custom.js',
        'js/app.js',
        output='dist/app.js',filters="jsmin"),
    'app_scss': Bundle(
        'scss/app.scss',
        output='dist/app.css',filters="pyscss")
}