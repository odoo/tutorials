from odoo.http import request, route
from odoo.addons.estate.controllers.property_list import EstatePropertyController


class EstatePropertyOfferController(EstatePropertyController):
    @route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def list_properties(self, page=1, domain=None, **kwargs):
        domain = domain or []

        selected_auction_type = kwargs.get('selected_property_auction_type', 'all')
        if selected_auction_type != 'all':
            domain.append(('property_auction_type', '=', selected_auction_type))

        selected_is_rent_or_not = kwargs.get('selected_is_rent_or_not', 'all')
        if selected_is_rent_or_not == 'sale':
            domain.append(('is_rent_property', '=', False))
        elif selected_is_rent_or_not == 'rent':
            domain.append(('is_rent_property', '=', True))

        return super().list_properties(page=page, domain=domain, selected_auction_type=selected_auction_type, **kwargs)

    @route(['/terms-and-conditions'], type='http', auth="public", website=True)
    def terms_and_conditions(self):
        return request.render('automated_auction.terms_conditions_page')
