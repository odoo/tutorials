from odoo import http
from odoo.http import request


class EstatePropertyController(http.Controller):

    @http.route('/property/<model("estate.property"):estate_property>', type='http', auth='public', website=True)
    def property_detail(self, estate_property, **kwargs):
        return request.render('estate.property_detail', {
            'property': estate_property,
        })