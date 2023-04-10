import os

import utils


def get_my_config_path(user):
    return f'{utils.get_user_home(user)}/xray/config/config.json'


default_config = '/usr/local/etc/xray/config.json'


def install(user):
    utils.execute_command_as_root(
        f'bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install -u {user}')


def creat_xray_files(user):
    utils.mkfile(get_my_config_path(user), user)
    utils.execute_command_as_root(f'rm {default_config}')
    utils.execute_command_as_root(f'ln -s {get_my_config_path(user)} {default_config}')


def write_config(user):
    file_dir, _ = os.path.split(__file__)
    file_path = os.path.join(file_dir, 'config.json')
    with open(file_path, 'r') as f:
        config = f.read()
    with open(f'{get_my_config_path(user)}', 'w') as f:
        f.write(config)


def restart():
    utils.execute_command_as_root(f'systemctl restart xray')
