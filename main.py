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

normal_user = 'uaername'
normal_user_password = 'password'
normal_user_groups = ['group1', 'group2']

ssh_key = 'ssh-ed25519 ssh_key user@host'
ssh_port = 22

domain = 'example.com'
cf_token = 'cf token'
cf_account_id = 'cd account id'


def run1():
    racknerd.add_missing_groups()
    racknerd.enable_ipv6()

    utils.add_user(normal_user, normal_user_password, normal_user_groups)

    ssh.add_ssh_key(normal_user, ssh_key)
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
    software.install_pip_packages(['virtualenv', 'autopep8'], normal_user)

    zsh.install()
    zsh.set_zsh_as_default_shell(normal_user)
    zsh.set_zsh_as_default_shell('root')
    zsh.install_zimfw(normal_user)
    zsh.install_zimfw('root')
    zsh.set_up_zimfw(normal_user)
    zsh.set_up_zimfw('root')
    zsh.set_editor(normal_user, 'nvim')
    zsh.set_editor('root', 'nvim')

    nginx.install()
    nginx.add_websocket_support()
    nginx.disable_default_site()
    nginx.create_site_dir(normal_user)
    nginx.start_in_boot()

    xray.install(normal_user)
    xray.creat_xray_files(normal_user)
    xray.write_config(normal_user)
    xray.restart()

    acme.install(normal_user)
    acme.apply_cert_with_cfdns(normal_user, domain, cf_token, cf_account_id)
    acme.install_cert(normal_user, domain)


if __name__ == '__main__':
    run1()
    # run2()
    pass
