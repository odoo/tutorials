from odoo import http
from odoo.http import request


class EstatePortal(http.Controller):
    @http.route(["/my/properties"], type="http", auth="user", website=True)
    def portal_my_properties(self, **kwargs):

        properties = request.env["estate.property"].search(
            [("buyer_id", "=", request.env.user.partner_id.id)],
        )

        return request.render("estate.portal_my_properties", {"properties": properties})
