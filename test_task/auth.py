from django.conf import settings
from django_auth_ldap.backend import LDAPBackend
import logging
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from django.http import HttpResponseServerError
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

# create logger
logger = logging.getLogger('django')


class LDAPLogin(APIView):
    """
    Class to authenticate a user via LDAP and
    then creating a login session

    ALLOWED METHOD: POST
    AUTHENTICATION: REQUIRED
    USAGE: BASE_URL + "/api/login/"
    """
    authentication_classes = ()
    permission_classes = []


    def post(self, request):

        # TODO : Use Django forms (security requirement)
        username = request.data['username']
        password = request.data['password']

        # defaulting user to None
        user = None

        debug_flag = settings.DEBUG
      
        if not debug_flag:
            # trying first with LDAPBackend
            try:
                auth = LDAPBackend()
                user = auth.authenticate(request=self.request,
                                        username=username,
                                        password=password,
                                        backend='django_auth_ldap.backend.LDAPBackend')

                if user is not None:

                    """
                    Add missing users from LDAP Server..
                    """
                    self.sync_db(self, user)


                    token = Token.objects.get_or_create(user=user)

                    token = token[0].key

                    response = Response({'token': token}, status=200)
                    response['Authorization'] = f"Token {token}"
                    return response

            except AttributeError:
                print('AttributeError api.views.py <l40>')
                pass

        else:
            
            # then trying with modelBackend:
            try:
                user = authenticate(username=username,
                                    password=password)

                if user is None:
                    data = {
                        'error': "L'utilisateur et/ou mot de passe sont incorrects, veuillez réessayer."}
                    return Response(data, status=403)

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                # token = Token.objects.get_or_create(user=user)

                # token = token[0].key

                response = Response(jwt_response_payload_handler(
                    token, user=user, request=request), status=200)
                response['Authorization'] = f"JWT {token}"
                return response

            except AttributeError as e:
                logger.exception('AttributeError api.views.py')
                pass

        return HttpResponseServerError()

    def sync_db(self, user):

        user

        pass
    
 
class LDAPLogout(APIView):
    """
    Class for logging out a user by clearing his/her session
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Api to logout a user
        :param request:
        :return:
        """
        logout(request)
        data = {'detail': 'User logged out successfully'}
        return Response(data, status=200)


