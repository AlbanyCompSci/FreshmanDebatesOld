# Sproxy

## What does Sproxy Do?
Sproxy is a proxy server (independent of the backend) for authenticating users
using Google OAuth2. It safely authenticates the user and passes requests to
the backend with authentication information (email address, name, origin, etc.).
It also has the ability to implement simple individual and group based
authorization for endpoints, however, I do not intend to use this feature as
authorization for the debates website will be dependent on the database (users
are also members of the database).

## Comparison to Other Solutions
Sproxy is the only solution I have found that authenticates through a proxy
rather than integrating with the app itself. This has the benefits of
simplifying the app, making it language agnostic and allowing one instance to
be used for more than one app.

## Getting Started
- see also the README on [Sproxy's GitHub page](https://github.com/zalora/sproxy)
1. Clone [Sproxy from GitHub](https://github.com/zalora/sproxy)
    - `git clone https://github.com/zalora/sproxy.git`
2. Install external dependencies
    - [PostgreSQL](http://www.postgresql.org/)
    - [GHC](https://www.haskell.org/ghc/)
    - [Cabal](https://www.haskell.org/cabal/)
3. Add `dev.zalora.com` to `/etc/hosts`
    - `sudo echo "127.0.2.1    dev.zalora.com" >> /etc/hosts`
4. Set up a project in the Google Developer Console
    1. APIs & auth
    2. Credentials
    3. Create new Client ID
    4. Use https://dev.zalora.com as Authorized JavaScript origins
    5. Use https://dev.zalora.com/sproxy/oauth2callback as Authorized redirect URI
5. Make and edit a copy of the configuration file
    - `cp config/sproxy.yml.example config/sproxy.yml`
    - Add Client ID to `config/sproxy.yml`
    - Add Client Secret to `config/client_secret`
6. Create the Sproxy database
    - `createdb sproxy && psql sproxy < sproxy.sql && psql sproxy < example/privileges.sql`
7. Install Sproxy
    - `cabal sandbox init`
    - `cabal install`
    - `cabal build`
