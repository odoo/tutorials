from odoo import http
from odoo.http import request
from datetime import datetime


class EstatePropertyController(http.Controller):
    @http.route(['/estate', '/estate/page/<int:page>'], auth='public', type='http', website=True)
    def estate_property_list(self, page = 1):

        per_page = 6
        domain = [('status', 'in', ['new', 'offer_received', 'offer_accepted'])]
        total_properties = request.env['estate.property'].search_count(domain)

        properties = request.env['estate.property'].search(domain, offset=(page - 1) * per_page, limit=per_page)

        pager = request.website.pager(
            url="/estate",
            total=total_properties,
            page=page,
            step=per_page
        )
        return request.render('estate.property_list_template', {
                'properties': properties,
                'pager': pager
            })
    
    @http.route(['/property/<int:property_id>',"/estate/page/property/<int:property_id>"], auth='public', type='http', website=True)
    def estate_property_details(self, property_id):
        property = request.env['estate.property'].browse(property_id)

        return request.render('estate.website_property_details', {
            'property': property,
            'offers': property.offer_ids
        })
    
    @http.route(['/offer',"/estate/page/property/<int:property_id>/offer","/property/<int:property_id>/offer"], auth='public', type='http', website=True)
    def estate_property_offer(self, property_id):
        property = request.env['estate.property'].browse(property_id)
        return request.render('estate.make_offer_template', {'property': property})

    @http.route(['/estate/submit',"/estate/page/property/<int:property_id>/submit","/property/<int:property_id>/submit"], auth='public', type='http', website=True, csrf=False, methods=['POST'])
    def submit_offer(self, **post):
        property_id = int(post.get('property_id'))
        offer_price = float(post.get('offer_price'))

        property = request.env['estate.property'].browse(property_id)

        if property.exists():
            request.env['estate.property.offer'].create({
                'property_id': property_id,
                'partner_id': request.env.user.partner_id.id,
                'price': offer_price,
                'validity': int(post.get('validity'))
            })

        return request.redirect('/property/%s' %property_id)
