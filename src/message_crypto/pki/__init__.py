import os
from fs import open_fs
import gnupg
import logging
from . import KeyManager, Encrypt, Decrypt 

home_fs = open_fs('.')

logger = logging.getLogger('init')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)


logger.addHandler(ch)

if not os.path.exists('signatures/'):
    home_fs.makedir(u'signatures')
    logger.info('Created signatures directory.')
else:
    logger.info('signatures directory already exists, skipping...')

if not os.path.exists('keys'):
    home_fs.touch(u'keys')
    logger.info('Created id-key storage file.')

if not os.path.exists('.gnupg/'):
    home_fs.makedir(u'.gnupg/')
    gpg = gnupg.GPG(gnupghome='.gnupg/')
    logger.info('Created gnupg home directory.')
    
    try:
        input_data = gpg.gen_key_input(key_type="RSA", key_length=4096, passphrase=input('Enter passphrase for your new key: '))
        key = gpg.gen_key(input_data)
        with open('userfp', 'w') as f:
            f.write(key.fingerprint)
        logger.info('Generated a new user key.')
        logger.info('Wrote user key fingerprint into file. Ready for the first run.')
    except Exception as e:
        logger.error(f'{e} -- unable to generate new keypair.')
else:
    logger.info('gnupg directory already exists, skipping...')
