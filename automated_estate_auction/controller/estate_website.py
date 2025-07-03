from odoo import http
from odoo.addons.estate.controllers.estate_website import EstatePropertyWebsite


class EstatePropertyWebsiteAddon(EstatePropertyWebsite):
    @http.route(
        ["/estate-properties", "/estate-properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def estate_properties_list(self, page=1, property_sell_type="all", **kwargs):
        response = super().estate_properties_list(page, **kwargs)
        properties = response.qcontext.get("properties")

        if property_sell_type and property_sell_type != "all":
            properties = properties.filtered(
                lambda p: p.property_sell_type == property_sell_type
            )

        total_pages = len(properties)
        pager = http.request.website.pager(
            url="/estate-properties",
            total=total_pages,
            page=page,
            step=1,
            scope=5,
            url_args={
                **kwargs,
                "property_sell_type": property_sell_type,
            },
        )
        response.qcontext.update(
            {
                "properties": properties,
                "pager": pager,
                "property_sell_type": property_sell_type,
            }
        )
        return response

    @http.route(
        "/estate-properties/<int:property_id>", type="http", auth="public", website=True
    )
    def estate_property_detail(self, property_id, **kwargs):
        super().estate_property_detail(property_id, **kwargs)
        property_model = http.request.env["estate.property"]
        property_obj = property_model.browse(property_id)
        return http.request.render(
            "automated_estate_auction.estate_property_detail_template_addon",
            {
                "property": property_obj,
            },
        )

    @http.route(
        "/estate-properties/<int:property_id>/create_offer",
        type="http",
        auth="public",
        website=True,
    )
    def estate_property_create_offer(self, property_id, **kwargs):
        property_model = http.request.env["estate.property"]
        property_obj = property_model.browse(property_id)
        return http.request.render(
            "automated_estate_auction.estate_property_offer_page_view",
            {
                "property_name": property_obj.name,
                "property_id": property_id,
            },
        )

    @http.route(
        "/estate-properties/thank-you",
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
    )
    def estate_property_offer_placed(self, **kwargs):
        offer_model = http.request.env["estate.property.offer"]
        property_id = int(kwargs["property_id"])

        response = offer_model.create(
            {
                "property_id": property_id,
                "price": float(kwargs["offer_price"]),
                "partner_id": http.request.env.user.partner_id.id,
            }
        )
        if response:
            return http.request.render(
                "automated_estate_auction.estate_property_offer_placed_view",
            )
