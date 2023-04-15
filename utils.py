#!python3


import os
import pwd
import shlex
import subprocess


def get_login_user():
    return os.getlogin()


def get_process_user():
    return pwd.getpwuid(os.getuid()).pw_name


def get_user_home(username):
    return os.path.expanduser("~" + username)


root_homedir = get_user_home('root')


def __check_software_installed(software):
    cmd = f"dpkg-query -W -f='${{Status}}' {software}"
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf-8')
    if "install ok installed" in output.lower():
        return True
    else:
        return False


def __check_zsh_installed():
    return __check_software_installed('zsh')


def __check_bash_installed():
    return __check_software_installed('bash')


def execute_command_as_user(username, command):
    if __check_zsh_installed():
        sh = 'zsh'
    elif __check_bash_installed():
        sh = 'bash'
    else:
        sh = 'sh'
    subprocess.run(['sudo', '-u', username, sh, '-c', f'cd && {command}'])


def execute_command_as_root(command):
    execute_command_as_user('root', command)


def execute_command_as_current_user(command):
    execute_command_as_user(get_login_user(), command)


def is_group_exists(groupname):
    try:
        # 调用 getent 命令，获取组信息
        output = subprocess.check_output(['getent', 'group', groupname])
        # 如果命令输出不为空，则该组存在
        return bool(output.strip())
    except subprocess.CalledProcessError:
        # 如果命令返回非零退出代码，说明该组不存在
        return False


def is_user_exists(username):
    try:
        # 使用Linux命令查询给定的用户是否存在
        subprocess.check_output(['id', '-u', username])
        return True
    except subprocess.CalledProcessError:
        return False


def add_groups(groups):
    for group in groups:
        if not is_group_exists(group):
            execute_command_as_root(f'groupadd {group}')


def add_user(user, password, add_groups):
    if not is_user_exists(user):
        if add_groups:
            execute_command_as_root(f'useradd -m -G {",".join(add_groups)} {user}')
        else:
            execute_command_as_root(f'useradd -m {user}')
        execute_command_as_root(f'echo {user}:{password} | chpasswd')


def mkdir(dir_path, user):
    if (not os.path.exists(dir_path)) or (not os.path.isdir(dir_path)):
        execute_command_as_user(user, f'mkdir -p {dir_path}')


def mkfile(file_path, user):
    dir_path, _ = os.path.split(file_path)
    mkdir(dir_path, user)
    if (not os.path.exists(file_path)) or (not os.path.isfile(file_path)):
        execute_command_as_user(user, f'touch {file_path}')


def add_lines_to_file(file_path, lines):
    with open(file_path, 'r') as f:
        existing_lines = f.readlines()

    is_need_newline = False

    if len(existing_lines) > 0:
        if len(existing_lines[-1]) > 0:
            if existing_lines[-1][-1] != '\n':
                is_need_newline = True

    existing_lines = [line.strip() for line in existing_lines]

    lines = [line.strip() for line in lines]

    with open(file_path, 'a') as f:
        if is_need_newline:
            f.write('\n')
        for line in lines:
            if line not in existing_lines:
                f.write(line + '\n')


def comment_lines_in_file(file_path, lines):
    with open(file_path, 'r') as f:
        existing_lines = f.readlines()

    with open(file_path, 'w') as f:
        for line in existing_lines:
            if len(line) > 0 and line[:-1] in lines:
                f.write('#' + line)
            else:
                f.write(line)
