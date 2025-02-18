from odoo.http import Controller, route, request

class PropertiesController(Controller):
    @route(
        ["/properties", "/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def show_properties(self, page=1):
        """
        Renders the properties page
        """
        properties_list = request.env["estate.property"].search([])

        return request.render(
            "estate.property_listing_template",
            {"properties": properties_list},
        )


class PropertyController(Controller):
    @route(["/properties/<int:property_id>"], type="http", auth="public", website=True)
    def show_property(self, property_id):
        """
        Renders the property page
        """
        property = request.env["estate.property"].browse(property_id)

        return request.render("estate.property_website_view", {"property": property})
