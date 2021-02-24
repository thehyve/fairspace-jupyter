const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const GrantManager = require('keycloak-connect/middleware/auth-utils/grant-manager');
const Grant = require('keycloak-connect/middleware/auth-utils/grant');
const Token = require('keycloak-connect/middleware/auth-utils/token');

const externalTargets = require('./targets.json')

const port = process.env.PORT || 3000;
const realmUrl = process.env.REALM_URL;
const target = process.env.TARGET_URL;
const clientId = process.env.CLIENT_ID;
const secret = process.env.CLIENT_SECRET;
const refresh_token = new Token(process.env.REFRESH_TOKEN, clientId);

refresh_token.isExpired = () => false;

const grantManager = new GrantManager({realmUrl, clientId, secret});

grantManager.validateGrant = (grant) => Promise.resolve(grant);

const grant = new Grant({refresh_token});

const app = express();

app.use((req, res, next) =>
    grantManager.ensureFreshness(grant)
        .then(grant => {
            req.headers['Authorization'] = `Bearer ${grant.access_token.token}`;
            next();
        })
        .catch((err) => {
            console.error(err);
            res.sendStatus(500);
        }));

app.use('/fairspace', createProxyMiddleware({
    target,
    changeOrigin: true,
    pathRewrite: {
        "^/fairspace": "/",
    }
}));

if (externalTargets && Array.isArray(externalTargets) && externalTargets.length > 0) {
    externalTargets.forEach(exTarget => {
        app.use(`/${exTarget.name}`, createProxyMiddleware({
            target: exTarget.url,
            changeOrigin: true,
            pathRewrite: {
                [`^/${exTarget.name}`]: '/'
            },
        }));
    })
}

app.listen(port);
