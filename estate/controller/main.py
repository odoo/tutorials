from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):
    
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def property_list(self, page=1, **kwargs):

        selected_date = kwargs.get("filter_date")
        property_search = kwargs.get("property_search")
        domain = [('state', 'in', ['new', 'offer_received'])]
        total_properties = request.env["estate.property"].search_count([])

        if selected_date:
            domain.append(('create_date', '>=', selected_date))
        if property_search:
            domain.append(('name', 'ilike', property_search))

        per_page = 6
        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=per_page,
            url_args={'filter_date': selected_date} if selected_date else {}
        )

        properties = request.env["estate.property"].search(domain, limit=per_page, offset=(page - 1) * per_page)
        return request.render("estate.properties_list_website", {"properties": properties, "pager": pager})
    
    @http.route('/property/<int:property_id>', type='http', auth='public', website=True)
    def property(self, property_id):
        property = request.env["estate.property"].browse(property_id)
        
        if not property.exists():
            return request.not_found()
        return request.render("estate.property_details_website", {"property": property})
