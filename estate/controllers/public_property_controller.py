from odoo import http


class PublicPropertyWeb(http.Controller):

    @http.route("/properties", auth="public", website=True)
    def index(self, page=1, **kw):
        properties = http.request.env["public.property"].search(
            ["|", ("state", "!=", "sold"), ("state", "!=", "cancelled")]
        )

        return http.request.render(
            "estate.public_property_web_render",
            {"properties": properties, "total_properties": len(properties)},
        )

    @http.route("/properties/<id>/", auth="public", website=True)
    def detailsOfProperty(self, id):
        details = http.request.env["public.property"].search([("id", "=", id)])
        print(details)
        return http.request.render(
            "estate.public_property_single_web_render", {"properties": details}
        )
