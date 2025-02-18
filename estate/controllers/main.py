from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):
    
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def property_list(self, page=1, **kwargs):
        listed_after = kwargs.get("listed_after")
        property_search = kwargs.get("property_search")
        domains = [('state', 'in', ['new', 'offer_received'])]
        total_properties = request.env["estate.property"].search_count([])

        if listed_after:
            domains.append(('create_date', '>=', listed_after))
        if property_search:
            domains.append(('name', 'ilike', property_search))

        pager = request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=6,
        )
        properties = request.env["estate.property"].search(domains, limit=6, offset=pager["offset"])
        return request.render("estate.properties_list_website", {"properties": properties, "pager": pager})

    @http.route('/property/<int:property_id>', type='http', auth='public', website=True)
    def property(self, property_id):
        property = request.env["estate.property"].browse(property_id)
        
        if not property.exists():
            return request.not_found()
        return request.render("estate.property_details_website", {"property": property})
    