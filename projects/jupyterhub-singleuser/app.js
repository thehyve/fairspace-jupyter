const express = require('express');
const proxy = require('http-proxy-middleware');

const GrantManager = require('keycloak-connect/middleware/auth-utils/grant-manager');
const Grant = require('keycloak-connect/middleware/auth-utils/grant');
const Token = require('keycloak-connect/middleware/auth-utils/token');

const port = process.env.PORT || 3000;
const realmUrl = process.env.REALM_URL;
const targetUrl = process.env.TARGET_URL;
const clientId = process.env.CLIENT_ID;
const secret = process.env.CLIENT_SECRET;
const refresh_token = new Token(process.env.REFRESH_TOKEN, clientId);

refresh_token.isExpired = () => false;

const grantManager = new GrantManager({realmUrl, clientId, secret});

grantManager.validateToken = (token, expectedType) => Promise.resolve(token);

const grant = new Grant({refresh_token});

const app = express();
app.set('trust proxy', true);

const addToken = (proxyReq, req, res) => {
    proxyReq.socket.pause();
    grantManager.ensureFreshness(grant)
        .then(grant => {
            proxyReq.setHeader('Authorization', `Bearer ${grant.access_token.token}`);
            proxyReq.socket.resume();
        }).catch((err) => {
        console.error(err);
        res.sendStatus(500);
    });
}


app.use(proxy('/**', {
    target: targetUrl,
    onProxyReq: addToken
}));

app.listen(port);
