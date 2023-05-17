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
        ## TODO Apply changes below, when a new version (>15.1.0) of https://github.com/jupyterhub/oauthenticator is released
        ## (exposing auth_state['id_token']
        ## in order to fix logout issue (https://www.keycloak.org/docs/21.0.1/upgrading/index.html#openid-connect-logout)
        #
        # logout_redirect_url = os.getenv('LOGOUT_REDIRECT_URL', '')
        # id_token = os.getenv('ID_TOKEN', '')
        # if logout_redirect_url:
        #     if id_token:
        #         return logout_redirect_url + "&id_token_hint=" + id_token
        #     return logout_redirect_url
        # return ''
        return os.getenv('LOGOUT_REDIRECT_URL', '')

    async def pre_spawn_start(self, user, spawner):
        auth_state = await user.get_auth_state()
        spawner.environment['REFRESH_TOKEN'] = auth_state['refresh_token']
        # spawner.environment['ID_TOKEN'] = auth_state['id_token'] # TODO
        spawner.environment['REALM_URL'] = self.token_url[0:-len('/protocol/openid-connect/token')]
        spawner.environment['CLIENT_ID'] = self.client_id
        spawner.environment['CLIENT_SECRET'] = self.client_secret
