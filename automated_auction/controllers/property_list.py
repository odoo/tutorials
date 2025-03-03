from odoo.http import request, route
from odoo.addons.estate.controllers.property_list import EstatePropertyController


class EstatePropertyOfferContoller(EstatePropertyController):
    @route(['/properties', '/properties/page/<int:page>'], type='http', auth="public", website=True)
    def list_properties(self, page=1, **kwargs):
        #define
