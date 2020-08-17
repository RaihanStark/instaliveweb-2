from flask_assets import Bundle

bundles = {
    'app_js': Bundle(
        'js/app.js',
        output='gen/home.js'),
}