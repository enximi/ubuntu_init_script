import software
import utils


def set_timezone(timezone):
    utils.execute_command_as_root(f'timedatectl set-timezone {timezone}')


def set_timezone_to_shanghai():
    set_timezone('Asia/Shanghai')


def set_language(language):
    utils.execute_command_as_root(f'update-locale LANG={language}')


def set_language_to_chinese():
    software.apt_install_packages(['language-pack-zh-hans'])
    set_language('zh_CN.UTF-8')


def set_language_to_english():
    set_language('en_US.UTF-8')


def reboot():
    utils.execute_command_as_root('reboot')
