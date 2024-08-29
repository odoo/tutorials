from odoo import http


class WebsiteProperty(http.Controller):

    @http.route("/properties", auth="public", website=True)
    def display_properties(self, page=1, **kwargs):
        page = int(page)
        items_per_page = 6
        offset = (page - 1) * items_per_page
        total_properties = http.request.env["estate.property"].search_count([('state', '!=', 'sold'), ('state', '!=', 'canceled')])
        total_page = (total_properties + items_per_page - 1) // items_per_page
        properties = http.request.env["estate.property"].search([('state', '!=', 'sold'), ('state', '!=', 'canceled')], limit=items_per_page, offset=offset)
        return http.request.render(
            "estate.estate_properties_website", {"properties": properties, 'page': page, 'total_page': total_page}
        )

    @http.route('/property/<model("estate.property"):each_property>', type='http', auth='public', website=True)
    def property_details(self, each_property, **kwargs):
        return http.request.render('estate.template_property_details', {
            'property': each_property,
        })
