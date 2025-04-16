from odoo import http
from odoo.http import request
from odoo.addons.estate.controllers.estate_property_controller import EstatePropertyController
from odoo.tools import float_utils


class EstateWebsiteExtended(EstatePropertyController):

    @http.route(['/estate', '/estate/page/<int:page>'], auth='public', type='http', website=True)
    def estate_property_list(self, page=1, **kwargs):
        per_page = 6
        domain = [('status', 'in', ['new', 'offer_received', 'offer_accepted'])]

        selling_type = kwargs.get('selling_type')
        if selling_type:
            domain.append(('selling_type', '=', selling_type))

        total_properties = request.env['estate.property'].search_count(domain)

        properties = request.env['estate.property'].search(domain, offset=(page - 1) * per_page, limit=per_page)

        pager = request.website.pager(
            url="/estate",
            total=total_properties,
            page=page,
            step=per_page,
            url_args={'selling_type': selling_type} if selling_type else {},
        )

        return request.render('estate.property_list_template', {
            'properties': properties,
            'pager': pager,
            'selling_type': selling_type,
        })

    @http.route(['/estate/submit', "/estate/page/property/<int:property_id>/submit", "/property/<int:property_id>/submit"], auth='public', type='http', website=True, csrf=False, methods=['POST'])
    def submit_offer(self, **post):

        property_id = int(post.get('property_id'))
        offer_price = float(post.get('offer_price'))

        property = request.env['estate.property'].browse(property_id)

        if float_utils.float_compare(float(property.best_offer), float(offer_price), 2) == 1 and property.selling_type == 'regular':
            return request.redirect('/property/' + str(property_id) + '/offer/' + "?error=Offer must be higher than " + str(property.best_offer))

        property = request.env['estate.property'].browse(property_id)

        if property.exists() and post.get('validity'):
            request.env['estate.property.offer'].create({
                'property_id': property_id,
                'partner_id': request.env.user.partner_id.id,
                'price': offer_price,
                'validity': int(post.get('validity'))
            })
        else:
            request.env['estate.property.offer'].create({
                'property_id': property_id,
                'partner_id': request.env.user.partner_id.id,
                'price': offer_price,
                'validity': 7
            })

        return request.redirect('/property/%s' % property_id)
