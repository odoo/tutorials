import json
from odoo import http
from odoo.addons.auth_oauth.controllers.main import OAuthLogin
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
from odoo.http import request


class CustomAuthSignup(AuthSignupHome):
    """
    Custom authentication and signup controller for handling user registration,
    including OAuth provider integration and automatic login upon signup.
    """

    @http.route("/", type="http", auth="public", website=True)
    def home_page(self):
        """
        Renders the home page with a list of available OAuth providers.
        """
        oauth = OAuthLogin()
        providers = oauth.list_providers()
        return request.render(
            "form_signup.home_page_template", {"providers": providers}
        )

    def _prepare_signup_values(self, qcontext):
        """
        Prepares user signup values by validating input fields and ensuring password confirmation.
        """
        values = super()._prepare_signup_values(qcontext)
        valid_user_fields = request.env["res.users"]._fields.keys()
        # Extract only valid user fields that are in qcontext
        new_values = {
            key: value for key, value in qcontext.items() if key in valid_user_fields
        }
        # Add only missing keys from new_values to values
        for key, value in new_values.items():
            if key not in values:
                values[key] = value
        return values

    @http.route(
        "/web/signup/<string:model_name>",
        type="http",
        auth="public",
        website=True,
        csrf=False,
    )
    def website_form(self, **kw):
        """
        Handles user signup via a website form.
        - Collects user input
        - Validates form data
        - Creates a new user account
        - Automatically logs in the user upon successful registration
        """
        qcontext = kw
        error_message = None
        user_id = None

        if "error" not in qcontext and request.httprequest.method == "POST":
            try:
                self.do_signup(qcontext)
                user = (
                    request.env["res.users"]
                    .sudo()
                    .search([("login", "=", qcontext.get("login"))], limit=1)
                )
                # Assign user session if signup is successful
                if user:
                    user_id = user.id
                    request.session.uid = user_id
                else:
                    error_message = "User signup was successful, but automatic login failed."
                # Return JSON response
                if not error_message:
                    return http.Response(
                        json.dumps({"success": True, "id": user_id}),
                        content_type="application/json",
                    )
            except UserError as e:
                error_message = e.args[0]
            except (SignupError, AssertionError) as e:
                # Check if the email is already registered
                if (
                    request.env["res.users"]
                    .sudo()
                    .search_count([("login", "=", qcontext.get("login"))], limit=1)
                ):
                    error_message = "Another user is already registered using this email address."
                else:
                    error_message = "Could not create a new account." + str(e)
        return http.Response(
            json.dumps({"error": error_message}), content_type="application/json"
        )
