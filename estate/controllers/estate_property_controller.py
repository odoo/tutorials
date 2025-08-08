from datetime import datetime

from odoo import http
from odoo.http import request
from odoo.addons.website.models.website import pager as website_pager


class EstatePropertyController(http.Controller):

    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def list_properties(self, page=1, date_filter=None, **kwargs):
        Properties = request.env['estate.property']

        domain = [('state', 'in', ['new', 'offer_received'])]
        properties_count = Properties.search_count(domain)

        per_page = 6
        offset = (page - 1) * per_page


        if date_filter:
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d").date()
            domain.append(('create_date', '>=', date_obj))

        pager = website_pager(
            url="/properties",
            total=properties_count,
            page=page,
            step=per_page,
            scope=3
        )

        properties = Properties.search(domain, limit=per_page, offset=offset)

        values = {
            'properties': properties,
            'pager': pager,
            'date_filter': date_filter
        }

        return request.render('estate.property_list_template', values)

    
    @http.route('/property/<int:property_id>', type="http", auth="public", website=True)
    def property_details(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        values = {
            "property":property
        }
        return request.render('estate.property_detail_template', values)
