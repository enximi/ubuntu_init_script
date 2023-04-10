import utils


def add_ssh_key(user, ssh_key):
    authorized_keys_file = f'{utils.get_user_home(user)}/.ssh/authorized_keys'
    utils.mkfile(authorized_keys_file, user)
    utils.add_lines_to_file(authorized_keys_file, [ssh_key])


def change_port(port):
    config_file = '/etc/ssh/sshd_config.d/port.conf'
    utils.mkfile(config_file, 'root')
    with open(config_file, 'w') as f:
        f.write(f'Port {port}\n')


def enable_password_authentication():
    config_file = '/etc/ssh/sshd_config.d/password.conf'
    utils.mkfile(config_file, 'root')
    with open(config_file, 'w') as f:
        f.write('PasswordAuthentication yes\n')


def disable_password_authentication():
    config_file = '/etc/ssh/sshd_config.d/password.conf'
    utils.mkfile(config_file, 'root')
    with open(config_file, 'w') as f:
        f.write('PasswordAuthentication no\n')


def enable_public_key_authentication():
    config_file = '/etc/ssh/sshd_config.d/public_key.conf'
    utils.mkfile(config_file, 'root')
    with open(config_file, 'w') as f:
        f.write('PubkeyAuthentication yes\n')


def disable_public_key_authentication():
    config_file = '/etc/ssh/sshd_config.d/public_key.conf'
    utils.mkfile(config_file, 'root')
    with open(config_file, 'w') as f:
        f.write('PubkeyAuthentication no\n')


def restart():
    utils.execute_command_as_root('systemctl restart sshd')
