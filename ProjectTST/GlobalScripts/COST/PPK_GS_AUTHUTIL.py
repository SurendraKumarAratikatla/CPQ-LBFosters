def get_cpq_bearer_token(session):
    token, expires_on = session['cpq_bearer_token'], session['cpq_bearer_token_expires_on']
    if token is not None and expires_on is not None and expires_on > DateTime().Now.Ticks:
        return token, "success"

    end_point = '/oauth2/token'
    url = 'https://{}{}'.format(RequestContext.Url.Host, end_point)

    res = AuthorizedRestClient.GetPasswordGrantOAuthToken('CPQ', url)

    if res.access_token is not None:
        session['cpq_bearer_token'] = '{} {}'.format(res.token_type, res.access_token)
        session['cpq_bearer_token_expires_on'] = DateTime().Now.Ticks + (int(res.expires_in) - 30) * 10000000 # 1 Second = 10,000,000 Ticks, 30 Second safety buffer period
        return session['cpq_bearer_token'], "success"

    return res.error, "failure"


def get_cpq_jwt_token(session):
    token, expires_on = session['cpq_jwt_token'], session['cpq_jwt_token_expires_on']
    if token is not None and expires_on is not None and expires_on > DateTime().Now.Ticks:
        return token, "success"
    cpq_bearer_token, status = get_cpq_bearer_token(session)

    end_point = '/api/rd/v1/Core/GenerateJWT'
    url = 'https://{}{}'.format(RequestContext.Url.Host, end_point)

    try:
        res = RestClient.Post(url, {}, {"Authorization": cpq_bearer_token})
        if res.token is not None:
            session['cpq_jwt_token'] = '{} {}'.format('Bearer', res.token)
            session['cpq_jwt_token_expires_on'] = DateTime().Now.Ticks + (82800 * 10000000) # expires in 23 hour 23 * 60 * 60 * 10000000
            return session['cpq_jwt_token'], "success"
    except Exception as ex:
        Log.Error("PPK_GS_AuthUtil", "Error Creating JWT token", ex)
        return "Error occured", "failure"

    return "Error occured", "failure"