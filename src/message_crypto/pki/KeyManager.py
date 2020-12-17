import gnupg
import logging


class KeyManager:
    '''
    A class for key import/export/deletion, provides access to user's public key.
    '''
    def __init__(self):
        self.gpg = gnupg.GPG(gnupghome='./.gnupg')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
 
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        ch.setFormatter(formatter)

        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()

        self.logger.addHandler(ch)
        try:
            with open('userfp', 'r') as f:
                self.__user_fingerprint = f.read()
        except Exception as e:
            self.logger.warning(f'{e} -- Unable to read user key fingerprint.')
   
    def import_key(self, key_data):
        try:
            self.gpg.import_keys(key_data)
            self.logger.info('Successfully imported public key.')
            return 'ok'
        except Exception as e:
            self.logger.error(f'{e} -- Unable to import public key.')

    def delete_key(self, fingerprint):
        try:
            status = self.gpg.delete_keys(fingerprint)
            self.logger.info(f'Deleted key with fingerprint {fingerprint}')
            return 'ok'
        except Exception as e:
            self.logger.error(f'{e} -- Unable to delete the key.')

    def get_user_key(self):
        key = str(self.gpg.export_keys(self.__user_fingerprint))
        return key

    def get_key_by_id(self, id):
        id = str(id)
        try:
            with open('keys', 'r') as f:
                rec = None
                keys = f.readlines()
                for i in keys:
                    if id in i:
                        rec = i.split('-')[1].strip('\n')
                if (rec):
                    return rec
                else:
                    raise ValueError('User not found')
        except Exception as e:
            self.logger.error(f'{e}')

    def get_user_fingerprint(self):
        return self.__user_fingerprint