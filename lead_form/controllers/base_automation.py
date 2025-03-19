import logging

from odoo.http import request, route
from odoo.addons.base_automation.controllers.main import BaseAutomationController
from odoo.addons.base_automation.models.base_automation import get_webhook_request_payload

_logger = logging.getLogger(__name__)


class CustomBaseAutomationController(BaseAutomationController):

    @route(['/web/hook/<string:rule_uuid>'], type='http', auth='public', methods=['GET', 'POST'], csrf=False, save_session=False)
    def call_webhook_http(self, rule_uuid, **kwargs):
        """ Extend the automation webhook to add extra condition """

        response = super().call_webhook_http(rule_uuid, **kwargs)

        data = get_webhook_request_payload()
        hub_challenge = data.get('hub.challenge')

        # If hub.challenge exists, return it. This is required for Facebook webhook verification
        if hub_challenge:
            _logger.info("Facebook webhook verification: %s", hub_challenge)
            return request.make_response(hub_challenge, headers=[('Content-Type', 'text/html')])

        return response
