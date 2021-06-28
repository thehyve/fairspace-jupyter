"""
Fairspace Authenticator
"""
import os

from oauthenticator.generic import GenericOAuthenticator
from oauthenticator.oauth2 import OAuthLogoutHandler
from traitlets import default, Unicode


class FairspaceLogoutHandler(OAuthLogoutHandler):
    async def render_logout_page(self):
        if self.authenticator.logout_redirect_url:
            self.redirect(self.authenticator.logout_redirect_url)
            return

        super().render_logout_page()


class FairspaceOAuthenticator(GenericOAuthenticator):
    logout_handler = FairspaceLogoutHandler
    logout_redirect_url = Unicode(help="""URL for logging out of Fairspace""", config=True)

    @default("logout_redirect_url")
    def _logout_redirect_url_default(self):
        return os.getenv('LOGOUT_REDIRECT_URL', '')

    async def pre_spawn_start(self, user, spawner):
        auth_state = await user.get_auth_state()
        spawner.environment['REFRESH_TOKEN'] = auth_state['refresh_token']
        spawner.environment['REALM_URL'] = self.token_url[0:-len('/protocol/openid-connect/token')]
        spawner.environment['CLIENT_ID'] = self.client_id
        spawner.environment['CLIENT_SECRET'] = self.client_secret
