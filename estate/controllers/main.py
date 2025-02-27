from odoo import http
from odoo.http import request

class EstatePropertyController(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='user', website=True)
    def show_property(self, listed_after=None, search_name=None, page=1):
        domain = [('state', 'not in', ['sold', 'cancelled'])]
        if search_name:
            domain.append(('name', '=', search_name))

        if listed_after:
            domain.append(('create_date', '>', listed_after))

        properties_per_page = 6
        total_properties = request.env['estate.property'].search_count(domain)

        if total_properties == 0:
            properties = []
        else:
            properties = request.env['estate.property'].search(
                domain, order='create_date desc', offset=(page - 1) * properties_per_page, limit=properties_per_page
            )

        pager = request.website.pager(
            url='/properties',
            total=total_properties, 
            page=page,
            step=properties_per_page,
            url_args={'listed_after': listed_after} if listed_after else {} 
        )

        return request.render('estate.property_list_template', {
            "properties": properties, 
            "pager": pager,
            "listed_after": listed_after, 
        })

    @http.route('/property/<int:property_id>', type='http', auth="public", website=True)
    def property_info(self, property_id, **kwargs):
        Property = request.env['estate.property'].browse(property_id)
        if not Property.exists():
            return request.not_found()

        return request.render('estate.property_info_template',{
            'property': Property,
        })
