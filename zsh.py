import software
import utils


def install():
    software.apt_install_packages(['zsh'])


def set_zsh_as_default_shell(user):
    utils.execute_command_as_root(f'usermod -s /bin/zsh {user}')


def install_zimfw(user):
    utils.comment_lines_in_file('/etc/zsh/zshrc',
                                ['  autoload -U compinit',
                                 '  compinit'], )
    utils.execute_command_as_user(user,
                                  'curl -fsSL https://raw.githubusercontent.com/zimfw/install/master/install.zsh | zsh')


def set_zimfw(user):
    utils.add_lines_to_file(f'{utils.get_user_home(user)}/.zimrc',
                            ['zmodule exa',
                             "zmodule ohmyzsh/ohmyzsh -f 'plugins/extract' -s 'plugins/extract/extract.plugin.zsh'",
                             "zmodule ohmyzsh/ohmyzsh -f 'plugins/sudo' -s 'plugins/sudo/sudo.plugin.zsh'"])


def set_editor(user, editor):
    utils.add_lines_to_file(f'{utils.get_user_home(user)}/.zshrc',
                            [f'export EDITOR={editor}'])
