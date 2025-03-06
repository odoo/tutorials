from odoo.http import Controller, request, route
from odoo.addons.estate.controller.controller_estate_property import EstateWebsite

class EstateWebsiteInherit(EstateWebsite):

    @route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):

        selling_type = kwargs.get('selling_type')
        domain = []

        if selling_type:
            domain.append(('selling_type', '=', selling_type))

        kwargs['domain'] = domain

        return super().list_properties(**kwargs)

    @route("/createoffer/<model('estate.property'):property>", type='http', auth='public', website=True)
    def create_offer(self, property, **kwargs):
        return request.render('estate_auction.add_offer_page', {'property': property})


    @route("/addoffer/<model('estate.property'):property>", type='http', auth='public', website=True)
    def add_offer(self, property, **kwargs):

        if kwargs.get('amount'):
            amount = kwargs.get('amount')
            record = request.env['estate.property.offer'].sudo().create({
                'price' : amount,
                'partner_id' : request.env.user.partner_id.id,
                'property_id' : property.id
            })

        return request.render('estate_auction.congratulation_page')
