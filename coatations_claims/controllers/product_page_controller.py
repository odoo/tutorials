from odoo import http
from odoo.http import request

class WebsiteSaleCoatation(http.Controller):
    @http.route('/coatations_claims/get_product_options', type='json', auth='user', csrf=False)
    def get_product_options(self, product_id=None):
        if not product_id:
            return {'error': 'Product ID is required'}

        # Fetch the relevant coatation lines for the product_id
        print(product_id)
        coatation_lines = request.env['coatations.lines'].search([('product_id.id', '=', product_id),('status','=','active')])
        print(coatation_lines)

        # If no matching coatation lines are found
        if not coatation_lines:
            return {'error': 'No coatations found for the product'}

        # Prepare the list of coatation options with Coatation_ID, client_name, and price
        options = []
        for line in coatation_lines:
            options.append({
                'coatation_id': line.coation_id.name,
                'client_name': line.coation_id.client_id.name,
                'price': line.coatation_unit_price if line.coatation_unit_price > 0 else line.recommended_sp
            })

        return {'options': options}
