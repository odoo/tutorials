from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo import http
from odoo.http import request


class MarketPlaceSignup(AuthSignupHome):
    @http.route()
    def web_auth_signup(self, *args, **kw):
        is_marketplace_enabled = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("website_sale.is_marketplace_enabled")
        )

        if request.httprequest.method == "POST":
            if not is_marketplace_enabled:
                kw["error"] = (
                    "The marketplace feature is currently disabled. Please contact the administrator."
                )
                return request.render("auth_signup.signup", kw)

        response = super().web_auth_signup(*args, **kw)

        if request.httprequest.method == "POST" and "user_type" in request.params:
            if hasattr(response, "qcontext"):
                response.qcontext["user_type"] = request.params.get("user_type")

        return response

    def do_signup(self, qcontext):
        super().do_signup(qcontext)

        user_role = request.params.get("user_type")
        if user_role == "seller":
            login = qcontext.get("login")
            if login:
                new_user = (
                    request.env["res.users"]
                    .sudo()
                    .search([("login", "=", login)], limit=1)
                )

                if new_user and new_user.partner_id:
                    new_user.partner_id.sudo().write({"is_seller": True})
