from odoo import http
from odoo.http import request

class EstateWebsite(http.Controller):

    # route for propwerty list with pagination and property details
    @http.route(['/properties', '/properties/<int:property_id>','/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, property_id=None, page=1, **kargs):
        # if property_id found then render property details 
        if property_id:
            property = request.env['estate.property'].sudo().browse(property_id)
            return request.render('estate.property_detail_template' , {'property': property})
        
        # if property_id not found then render all property list
        page_size = 4
        offset = (int(page) - 1 )*page_size  # offset == index of properties array to start fatching
        properties = request.env['estate.property'].search([('state', 'in', ('new', 'offer_received'))], limit=page_size, offset=offset)
        total_properties = request.env['estate.property'].search_count([('state', 'in', ('new', 'offer_received'))])

        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=page_size
        )
        return request.render('estate.property_list_template' , {'properties': properties, 'pager': pager,})
    
    # if route type get then render from and if post then crete offer and store in database (database interection)
    @http.route('/properties/<int:property_id>/make-offer', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def make_offer(self, property_id, **body):
        property = request.env['estate.property'].sudo().browse(property_id)
        
        if not property.exists():
            return request.redirect('/properties')
        
        offer_price = body.get('offer_price')
        date_validity = body.get('date_validity')
        # Get logged-in user's partner
        partner = request.env.user.partner_id

        request.env['estate.property.offer'].sudo().create({
            'property_id': property_id,
            'partner_id': partner.id,
            'price': float(offer_price),
            'date_deadline': date_validity,
        })
        return request.redirect('/properties/%d' % property_id)
    