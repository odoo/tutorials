from odoo import http
from odoo.http import request       # used to the odoo's environment

class estatePropertyController(http.Controller):
    @http.route('/odoo/action-80', typr='http, auth='public', website=True)
    def property_list(self, page=1, **searches):
        property = request.env['estate.property']
        domain = [('state', 'in' , ['new','offer_recevied'])]

        properties_count = property.search_count(domain)
        pager = request.website.pager(
            url="/odoo/action-80",
            total=properties_count,
            page=page,
            step=6
        )

        properties = property.search(domain, limit=6, offset=pager['offset'])
        return request.render('estate.property_list', {
            'properties': properties,
            'pager': pager
        })

    @http.route('/property/<model("estate.property"):estate_property>', type='http', auth='public', website=True)
    def property_details(self, estate_property):
        return request.render('estate.property_details', {
            'property': estate_property
        })

