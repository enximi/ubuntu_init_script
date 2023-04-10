import utils


def enable_bbr():
    utils.add_lines_to_file('/etc/sysctl.conf',
                            ['net.core.default_qdisc = fq',
                             'net.ipv4.tcp_congestion_control = bbr'])


def ipv4_first():
    utils.add_lines_to_file('/etc/gai.conf',
                            ['precedence ::ffff:0:0/96 100'])


def restart():
    utils.execute_command_as_root('systemctl restart networking')
