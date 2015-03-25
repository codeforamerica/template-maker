from flask.ext.assets import Bundle, Environment

less = Bundle(
    'less/main.less',
    filters='less',
    output='css/app/main.css',
    depends=('less/*.less', 'less/**/*.less', 'less/**/**/*.less')
)

assets = Environment()
assets.register('css_all', less)