import utils
from nginx import nginx


def install(user):
    utils.execute_command_as_user(user, 'curl https://get.acme.sh | sh -s email=my@example.com')


def apply_cert_with_cfdns(user: str, domain: str, cf_token: str, cf_account_id: str):
    cmd = f'export CF_Token="{cf_token}"' \
          f' && export CF_Account_ID="{cf_account_id}"' \
          f' && {utils.get_user_home(user)}/.acme.sh/acme.sh --issue' \
          f' --dns dns_cf' \
          f' -d {domain} -d "*.{domain}"' \
          f' --keylength ec-256'
    utils.execute_command_as_user(user, cmd)


def install_cert(user: str, domain: str):
    nginx.make_reload_no_password(user)
    cert_floder = f'{utils.get_user_home(user)}/cert/{domain}'
    utils.mkdir(cert_floder, user)
    cmd = f'{utils.get_user_home(user)}/.acme.sh/acme.sh --install-cert -d {domain} --ecc' \
          f' --key-file {cert_floder}/key.key' \
          f' --fullchain-file {cert_floder}/fullchain.cer' \
          f' --reloadcmd "sudo service nginx force-reload"'
    utils.execute_command_as_user(user, cmd)


def get_cert_paths(user: str, domain: str):
    cert_floder = f'{utils.get_user_home(user)}/cert/{domain}'
    return {'fullchain': f'{cert_floder}/fullchain.cer', 'key': f'{cert_floder}/key.key'}
