"""
Fairspace Authenticator
"""

import os

from oauthenticator.generic import GenericOAuthenticator
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from traitlets import Unicode


class FairspaceOAuthenticator(GenericOAuthenticator):
    session_url = Unicode(
        os.environ.get('SESSION_URL', ''),
        help="URL for obtaining JSESSIONID"
    ).tag(config=True)

    async def pre_spawn_start(self, user, spawner):
        if self.session_url:
            session_id = ''
            http_client = AsyncHTTPClient()
            req = HTTPRequest(self.session_url,
                              method='GET',
                              headers={'Authorization': 'Bearer ' + user['access_token']},
                              validate_cert=self.tls_verify,
                              )
            resp = await http_client.fetch(req)

            for cookie in resp.headers.get_list('Set-Cookie'):
                if cookie.startswith('JSESSIONID='):
                    session_id = cookie[len('JSESSIONID='):]
                    sep = session_id.find(';')
                    if sep > 0:
                        session_id = session_id[:sep]
                    break
            auth_state = await user.get_auth_state()
            if auth_state:
                spawner.environment['SESSION_ID'] = session_id


