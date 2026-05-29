from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError


class MarketPlaceSignup(AuthSignupHome):
    @http.route()
    def web_auth_signup(self, *args, **kw):
        is_marketplace_enabled = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("website_sale.is_marketplace_enabled")
        )

        user_role = kw.get("user_role")

        if request.httprequest.method == "POST":
            if not is_marketplace_enabled:
                kw["error"] = (
                    "The marketplace feature is currently disabled. Please contact the administrator."
                )
                return request.render("auth_signup.signup", kw)

        response = super(MarketPlaceSignup, self).web_auth_signup(*args, **kw)
        return response

    def do_signup(self, qcontext):
        super(MarketPlaceSignup, self).do_signup(qcontext)

        user_role = qcontext.get("user_role")

        if user_role == "vendor":
            current_user = request.env.user
            if current_user and current_user.partner_id:
                current_user.partner_id.sudo().write({"is_seller": True})
