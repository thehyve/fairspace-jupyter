# A Docker image for Jupyter Hub. Includes OpenID Connect authenticator.

This image enables authentication using OpenID Connect API. Optionally, it allows to store JWT access and refresh tokens in Pluto, retrieve a JSESSIONID cookie and pass it to the single user server as an environment variable. 
Implementation of OpenIDConnectOAuthenticator is similar to GenericOAuthenticator from oauthenticator package.
