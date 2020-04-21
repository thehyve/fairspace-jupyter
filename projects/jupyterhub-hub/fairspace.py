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
            auth_state = await user.get_auth_state()
            if auth_state:
                req = HTTPRequest(self.session_url,
                                  method='GET',
                                  headers={'Authorization': 'Bearer ' + auth_state['access_token']},
                                  validate_cert=self.tls_verify
                                  )
                resp = await AsyncHTTPClient().fetch(req)

                for cookie in resp.headers.get_list('Set-Cookie'):
                    if cookie.startswith('JSESSIONID='):
                        session_id = cookie[len('JSESSIONID='):]
                        sep = session_id.find(';')
                        if sep > 0:
                            session_id = session_id[:sep]
                        spawner.environment['SESSION_ID'] = session_id



