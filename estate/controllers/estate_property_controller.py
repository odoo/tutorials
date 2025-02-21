from odoo import http
from odoo.http import request

class RealEstateController(http.Controller):

    @http.route(
        ["/properties","/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def list_properties(self, **kwargs):
        per_page = 6 
        
        page = int(kwargs.get('page', 1))

        listed_after = kwargs.get('listed_after')

        search_query = kwargs.get('search')

        domain = [
            ('state', 'in', ['new', 'offer_received']),
            ('active', '=', True)
        ]

        if listed_after:
            domain.append(('create_date', '>=', listed_after))

        if search_query:
            domain.append(('name', 'ilike', search_query))

        total_properties = request.env['estate.property'].search_count(domain)

        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=per_page,
            url_args={"listed_after": listed_after,"search": search_query},
        )

        properties = request.env['estate.property'].search(
            domain, limit=per_page, offset=pager["offset"]
        )

        return request.render(
            "estate.property_list_template",
            {
                "properties": properties,
                "pager": pager,  
                'listed_after': listed_after or '',
            },
        )

    @http.route('/property/<int:property_id>', type='http', auth='public', website=True)
    def property_details(self, property_id, **kwargs):
        property_obj = request.env['estate.property'].browse(property_id)

        if not property_obj.exists():
            return request.render('website.404') 

        return request.render('estate.property_detail_template', {
            'property': property_obj
        })
