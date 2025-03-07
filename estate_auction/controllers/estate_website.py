from odoo import http
from odoo.http import request
from odoo.addons.estate.controllers.estate_website import EstateWebsite


class EstateAuctionWebsite(EstateWebsite):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def list_properties(self, page=1, **kwargs):
        domain = []

        # Filter by selling mode
        selling_mode = kwargs.get('selling_mode')
        if selling_mode in ['regular', 'auction']:
            domain.append(('selling_mode', '=', selling_mode))

        kwargs['domain'] = domain
        return super().list_properties(**kwargs)
