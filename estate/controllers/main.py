# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import Controller
from odoo.http import request 
from odoo.http import route 

class Visitor(Controller):
    @route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def property_display(self, page=1):
        Property = request.env['estate.property']
        total_count = Property.search_count([])
        items_per_page = 6
        pager = request.website.pager(
            url='/properties',
            total=total_count,
            page=page,
            step=items_per_page,
        )
        properties = Property.search([], limit=items_per_page, offset=(page - 1) * items_per_page)
        return request.render('estate.property_template', {'properties':
    properties, 'pager':pager})

    @route('/property/<model("estate.property"):property>', type='http', auth='public', website=True)
    def property_details(self, property):
        return request.render('estate.property_details_template', {'property':
    property})
