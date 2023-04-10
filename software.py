import utils


def apt_update():
    utils.execute_command_as_root('apt update')


def apt_upgrade():
    utils.execute_command_as_root('apt upgrade -y')


def apt_install_packages(packages):
    utils.execute_command_as_root(f'apt install -y {" ".join(packages)}')


def apt_auto_remove_packages(packages):
    utils.execute_command_as_root(f'apt autoremove -y {" ".join(packages)}')


def install_pip_packages(packages, user):
    utils.execute_command_as_user(user, f'pip install {" ".join(packages)}')
