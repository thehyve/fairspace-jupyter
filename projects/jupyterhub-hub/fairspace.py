"""
Fairspace Authenticator
"""

from oauthenticator.generic import GenericOAuthenticator


class FairspaceOAuthenticator(GenericOAuthenticator):
    async def pre_spawn_start(self, user, spawner):
        auth_state = await user.get_auth_state()
        spawner.environment['REFRESH_TOKEN'] = auth_state['refresh_token']
        spawner.environment['REALM_URL'] = self.token_url[0:-len('/protocol/openid-connect/token')]
        spawner.environment['CLIENT_ID'] = self.client_id
        spawner.environment['CLIENT_SECRET'] = self.client_secret
