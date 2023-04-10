import subprocess

import utils


def enable():
    # 启动一个交互式Shell
    p = subprocess.Popen(['ufw', 'enable'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # 发送命令并获取输出
    output, _ = p.communicate(b'y\n')
    print(output.decode())

    # 关闭进程
    p.terminate()


def allow_ssh(port):
    utils.execute_command_as_root(f'ufw allow {port}/tcp')


def allow_cf():
    import requests
    ipv4_ips = requests.get('https://www.cloudflare.com/ips-v4').text.splitlines()
    ipv6_ips = requests.get('https://www.cloudflare.com/ips-v6').text.splitlines()
    for ip in ipv4_ips:
        utils.execute_command_as_root(f'ufw allow from {ip} to any port 80,443 proto tcp')
    for ip in ipv6_ips:
        utils.execute_command_as_root(f'ufw allow from {ip} to any port 80,443 proto tcp')


def show():
    utils.execute_command_as_root('ufw status')
