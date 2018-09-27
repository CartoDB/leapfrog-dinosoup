#class DisableCSRF(object):
#    def process_request(self, request):
#            setattr(request, '_dont_enforce_csrf_checks', True)

from django.utils.deprecation import MiddlewareMixin

class DisableCsrfCheck(MiddlewareMixin):

    def process_request(self, req):
        attr = '_dont_enforce_csrf_checks'
        if not getattr(req, attr, False):
            setattr(req, attr, True)

