import functools
import getpass
import botocore.credentials


old_create_credential_resolver = botocore.credentials.create_credential_resolver

class PromptProvider(botocore.credentials.CredentialProvider):
  METHOD = 'custom-prompt'
  def load(self):
    print('Please authenticate with your aws_access_key_id and aws_secret_access_key')
    return botocore.credentials.Credentials(
        access_key=getpass.getpass('aws_access_key_id: '),
        secret_key=getpass.getpass('aws_secret_access_key: '),
        method=self.METHOD,
    )

@functools.wraps(old_create_credential_resolver)
def new_create_credential_resolver(*args, **kwargs):
  cr = old_create_credential_resolver(*args, **kwargs)
  cr.insert_after('iam-role', PromptProvider())
  return cr

botocore.credentials.create_credential_resolver = new_create_credential_resolver
