from odoo.addons.estate.controllers.estate import EstateController
from odoo.http import request, route


class EstateAuctionFilter(EstateController):
    @route(['/properties', '/properties/page/<int:page>'], auth='public', website=True)
    def fetch_properties(self, page=1, **kwargs):
        response = super().fetch_properties(page, **kwargs)
        properties = response.qcontext.get('properties')
        query_params = response.qcontext.get('pager').get('url_args', {})

        sale_filter = kwargs.get('sale_mode', False)
        if sale_filter:
            if sale_filter in ['auction', 'regular']:
                properties = properties.filtered(lambda p: p.sale_mode == sale_filter)
                query_params.update({'sale_mode': sale_filter})

        items_per_page = 10
        total_items = len(properties)
        start_index = items_per_page * (page - 1)
        page_items = properties[start_index : start_index + items_per_page]

        pager = request.website.pager(
            url='/properties',
            total=total_items,
            page=page,
            step=items_per_page,
            url_args=query_params,
        )

        response.qcontext.update({
            'properties': page_items,
            'pager': pager,
            'sale_mode': sale_filter,
        })

        return response
