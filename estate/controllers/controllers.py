from odoo import http
from odoo.http import request
from datetime import datetime

class PropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'],
                auth="public", website=True, csrf=True, methods=['GET', 'POST'])
    def list_properties(self, page=1, **kw):
        
        listed_after = kw.get('listed_after')
        search_property = kw.get('search_property')

        domain = [("state", "in", ["new", "offer_received", "offer_accepted"])]

        if listed_after:
            try:
                date_obj = datetime.strptime(listed_after, "%Y-%m-%d")
                domain.append(('create_date', '>', date_obj))
            except ValueError:
                pass  

        if search_property:
            domain.append(('name', 'ilike', search_property))

        Property = request.env['estate.property']
        total_properties = Property.search_count(domain)
        properties_per_page = 6
        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=properties_per_page,
            url_args={
                'listed_after': listed_after,
                'search_property': search_property
            } if listed_after or search_property else {}
        )

        properties = Property.search(
            domain,
            limit=properties_per_page,
            offset=pager['offset'],
            order="create_date desc"
        )

        return request.render("estate.property_listing", {
            "properties": properties,
            "pager": pager,
            "listed_after": listed_after,
            "search_property": search_property
        })

    @http.route("/properties/<int:property_id>", type="http", auth="public", website=True)
    def property_details(self, property_id):
        property = request.env['estate.property'].browse(property_id)
        if not property.exists():
            return request.not_found()
        return request.render('estate.property_details_template', {
            'property': property
        })
