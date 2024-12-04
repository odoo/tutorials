from odoo import http
from odoo.http import request, route
import json


class WebsiteContactForm(http.Controller):

    @http.route("/website/contact_form", auth="public", website=True)
    def contact_form(self):
        # Render the contact form template
        return request.render("estate.contact_form_template")

    @route(
        "/website/contact_form_submit",
        auth="user",
        methods=["POST"],
        type="http",
        website=True,
    )
    def submit_contact_form(self, **post):
        name = post.get("name")
        email = post.get("email")

        request.env["res.partner"].sudo().create({"name": name, "email": email})

        return request.render("estate.thank_you")

    @http.route(
        "/ext_website/contact_form/submit",
        auth="public",
        methods=["POST"],
        type="json",
        website=True,
        csrf=False,
        cors="*",
    )
    def submit_contact_form_ext(self, **post):
        # print("post:", post)
        if not post:
            try:
                ## request.httprequest.data is raw data format (binary data)
                post = json.loads(request.httprequest.data.decode("utf-8"))
            except Exception as e:
                _logger.error(f"Fallback JSON Parsing Error: {e}")
                return {"error": "Invalid request format"}

        name = post.get("name")
        email = post.get("email")

        # Debugging - check the received data
        print(f"Received data: {name}, {email}")

        if name and email:
            # Create a new partner record with the provided data
            partner = (
                request.env["res.partner"].sudo().create({"name": name, "email": email})
            )
            return "Partner created successfully!"
        else:
            return "Error: Please provide both name and email."
