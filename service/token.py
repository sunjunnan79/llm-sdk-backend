from api import request, response, error
from pkg.jwt import getJWT


class TokenService:
    def __init__(self):
        self.jwt = getJWT()

    def Register(self, req: request.RegisterReq) -> response.RegisterResp:
        if self.jwt.check_create_token(req.token):
            token = self.jwt.issue_license(owner=req.owner)

            return response.RegisterResp(token=token)
        else:
            raise error.TOKEN_BAD_CREATE_TOKEN
