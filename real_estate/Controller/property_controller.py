from odoo import http
from odoo.http import request

class PropertyController(http.Controller):

    @http.route('/properties', auth='public', website=True)
    def property_page(self, page=1):
        page = int(page)
        per_page = 3  
        total_properties = request.env['estate.property'].sudo().search_count([])
        properties = request.env['estate.property'].sudo().search([], offset=(page-1)*per_page, limit=per_page)

        return request.render('real_estate.property_template', {
            'properties': properties,
            'page': page,
            'total_pages': (total_properties // per_page) + (1 if total_properties % per_page else 0)
        })

    @http.route('/property/<int:property_id>', auth='public', website=True)
    def property_detail(self, property_id):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        
        if not property_obj.exists():
            return request.render("website.404") 

        return request.render("real_estate.estate_property_detailed", {
            'property': property_obj
        })
    
    @http.route('/make-offer', type='http', auth="public", website=True)
    def make_offer_form(self, property_id=None, **kwargs):
        property = request.env['estate.property'].sudo().browse(int(property_id))
        return request.render('real_estate.estate_property_offer_template', {'property': property})

    @http.route('/submit-offer', type='http', auth="public", methods=['POST'], website=True)
    def submit_offer(self, **post):
      if post.get('price'):
        price = float(post.get('price'))
        property_id = int(post.get('property_id'))
        
        existing_offer = request.env['estate.property.offer'].sudo().search([
            ('property_id', '=', property_id)
        ], order='price desc', limit=1)

        if existing_offer and price < existing_offer.price:
            return request.redirect('/property/%s' % property_id)

        request.env['estate.property.offer'].sudo().create({
            'price': price,
            'validity': post.get('validity'),
            'property_id': property_id,
            'partner_id': request.env.user.partner_id.id,
        })

        return request.redirect('/property/%s' % post.get('property_id'))
