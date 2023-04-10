import acme
import firewall
import network
import nginx
import racknerd
import software
import ssh
import time_and_region
import utils
import zsh
from xray import xray

add_user = 'xxx'
add_user_password = 'xxxpassword'
add_user_groups = ['sudo']

ssh_key = 'xxx'
ssh_port = 22

domain = 'example.com'
cf_token = 'xxx'
cf_account_id = 'xxx'


def run1():
    racknerd.add_missing_groups()
    racknerd.enable_ipv6()

    utils.add_user(add_user, add_user_password, add_user_groups)

    ssh.add_ssh_key(add_user, ssh_key)
    ssh.add_ssh_key('root', ssh_key)
    ssh.change_port(ssh_port)
    ssh.disable_password_authentication()
    ssh.enable_public_key_authentication()

    network.enable_bbr()
    network.restart()

    time_and_region.set_timezone_to_shanghai()

    firewall.enable()
    firewall.allow_ssh(ssh_port)
    firewall.allow_cf()

    software.apt_update()
    software.apt_upgrade()


def run2():
    software.apt_auto_remove_packages(['vim'])
    software.apt_install_packages(['ranger', 'curl', 'git', 'neovim', 'python3-pip'])
    software.install_pip_packages(['virtualenv', 'autopep8'], add_user)

    zsh.install()
    zsh.set_zsh_as_default_shell(add_user)
    zsh.set_zsh_as_default_shell('root')
    zsh.install_zimfw(add_user)
    zsh.install_zimfw('root')
    zsh.set_zimfw(add_user)
    zsh.set_zimfw('root')
    zsh.set_editor(add_user, 'nvim')
    zsh.set_editor('root', 'nvim')

    nginx.install()
    nginx.add_websocket_support()
    nginx.del_default_site()
    nginx.create_site_dir(add_user)
    nginx.start_in_boot()

    xray.install(add_user)
    xray.creat_xray_files(add_user)
    xray.write_config(add_user)
    xray.restart()

    acme.install(add_user)
    acme.apply_cert(add_user, domain, cf_token, cf_account_id)
    acme.install_cert(add_user, domain)


if __name__ == '__main__':
    run1()
    # run2()
    pass
