import utils


def enable_ipv6():
    utils.add_lines_to_file('/etc/sysctl.conf',
                            ['net.ipv6.conf.all.autoconf = 0',
                             'net.ipv6.conf.all.accept_ra = 0',
                             'net.ipv6.conf.eth0.autoconf = 0',
                             'net.ipv6.conf.eth0.accept_ra = 0'])


def add_missing_groups():
    utils.add_groups(['adm', 'sudo'])


if __name__ == '__main__':
    enable_ipv6()
    add_missing_groups()
