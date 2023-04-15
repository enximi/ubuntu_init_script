import os

import acme
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


def disable_default_site():
    if os.path.exists('/etc/nginx/sites-enabled/default'):
        utils.execute_command_as_root('unlink /etc/nginx/sites-enabled/default')


def create_dirs_and_files(user, domain):
    utils.mkdir(f'{utils.get_user_home(user)}/nginx/site-available', user)
    utils.mkdir(f'{utils.get_user_home(user)}/nginx/site-enabled', user)
    utils.execute_command_as_root(f'rm -rf /etc/nginx/sites-enabled')
    utils.execute_command_as_root(f'ln -s {utils.get_user_home(user)}/nginx/site-enabled /etc/nginx/sites-enabled')
    ssl_config_path = f'{utils.get_user_home(user)}/nginx/ssl_config/ssl.conf'
    utils.mkfile(ssl_config_path, user)
    with open(ssl_config_path, 'w') as f:
        paths = acme.get_cert_paths(user, domain)
        f.write(f"ssl_certificate {paths['fullchain']};\n"
                f"ssl_certificate_key {paths['key']};\n")

    file_dir, _ = os.path.split(__file__)
    file_path = os.path.join(file_dir, 'default.conf')

    with open(file_path, 'r') as f:
        default_site = f.read()

    default_site = default_site.replace('__my_domain__', domain)
    default_site = default_site.replace('__ssl_config_path__', ssl_config_path)

    utils.mkfile(f'{utils.get_user_home(user)}/nginx/site/default.conf', user)
    with open(f'{utils.get_user_home(user)}/nginx/site-available/default.conf', 'w') as f:
        f.write(default_site)
    if os.path.exists(f'{utils.get_user_home(user)}/nginx/site-enabled/default.conf'):
        utils.execute_command_as_root(f'unlink {utils.get_user_home(user)}/nginx/site-enabled/default.conf')
    utils.execute_command_as_user(user,
                                  f'ln -s '
                                  f'{utils.get_user_home(user)}/nginx/site-available/default.conf '
                                  f'{utils.get_user_home(user)}/nginx/site-enabled/default.conf')


def make_reload_no_password(user):
    path = '/etc/sudoers.d/nginx'
    utils.mkfile(path, 'root')
    utils.add_lines_to_file(path, [f'{user} ALL=(ALL) NOPASSWD: /usr/sbin/service nginx force-reload'])
