import software
import utils


def install():
    software.apt_install_packages(['nginx'])


def start_in_boot():
    utils.execute_command_as_root('systemctl enable nginx')
    utils.execute_command_as_root('systemctl start nginx')


def add_websocket_support():
    # 定义要添加的配置项
    websocket_config = """
    # WebSocket支持配置
    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }
"""

    # 读取nginx配置文件
    with open('/etc/nginx/nginx.conf', 'r') as f:
        nginx_conf = f.read()

    # 判断是否已经添加过WebSocket支持
    if 'WebSocket支持配置' not in nginx_conf:
        # 在http块中添加WebSocket支持配置
        nginx_conf = nginx_conf.replace('http {', f'http {{\n{websocket_config}\n')

        # 保存修改后的配置文件
        with open('/etc/nginx/nginx.conf', 'w') as f:
            f.write(nginx_conf)

        # 重启nginx服务
        utils.execute_command_as_root('service nginx restart')

        print('WebSocket支持已成功添加！')
    else:
        print('WebSocket支持已经存在，无需重复添加。')


def del_default_site():
    if os.path.exists('/etc/nginx/sites-enabled/default'):
        utils.execute_command_as_root('unlink /etc/nginx/sites-enabled/default')


def create_site_dir(user):
    utils.mkdir(f'{utils.get_user_home(user)}/nginx/site', user)
