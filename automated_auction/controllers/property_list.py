from odoo.http import request, route
from odoo.addons.estate.controllers.property_list import EstatePropertyController


class EstatePropertyOfferController(EstatePropertyController):
    @route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def list_properties(self, page=1, domain=None, **kwargs):
        domain = domain or []

        selected_auction_type = kwargs.get('selected_property_auction_type', 'all')
        if selected_auction_type != 'all':
            domain.append(('property_auction_type', '=', selected_auction_type))

        return super().list_properties(page=page, domain=domain, selected_auction_type=selected_auction_type, **kwargs)
