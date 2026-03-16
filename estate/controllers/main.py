from odoo import http
from odoo.http import request

class PropertyController(http.Controller):
    @http.route(['/properties'], type='http', auth="public", website=True)
    def property_list(self, **post):
        properties = request.env['estate.property'].sudo().search([])
        # breakpoint()
        return request.render('estate.property_list_template', {
            'properties': properties,
        })

    @http.route(['/properties/<model("estate.property"):prop>'], type='http', auth="public", website=True)
    def property_detail(self, prop, **post):
        return request.render('estate.property_detail_template', {
            'property': prop,
        })

class EstateController(http.Controller):
    @http.route('/estate/get_property_data', type='json2', auth='public', website=True)
    def get_property_data(self, **kwargs):
        limit = int(kwargs.get('limit') or 3)
        properties = request.env['estate.property'].sudo().search(
            [('state', '=', 'new')],
            limit=limit
        )
        return request.env['ir.ui.view']._render_template("estate.dynamic_filter_template_property_cards_estate", {
            'records': [{'_record': p} for p in properties],
        })

# class EstateController(http.Controller):
#     @http.route('/estate/get_property_data', type='json2', auth='public', website=True)
#     def get_property_data(self, **kwargs):
#         # Standard Odoo dynamic snippets expect results formatted for the template
#         limit = int(kwargs.get('limit', 3))
#         properties = request.env['estate.property'].sudo().search([('state', '=', 'new')], limit=limit)
#         # breakpoint()
#         # We render the fragment here, just like Odoo's _render() method does
#         return request.env['ir.ui.view']._render_template("estate.dynamic_filter_template_property_cards_estate", {
#             'records': [{'_record': p} for p in properties],
#         })

# class EstateController(http.Controller):
#     @http.route('/estate/get_property_data', type='json2', auth='public', website=True)
#     def get_property_data(self, **kwargs):
#         # Fetch records
#         properties = request.env['estate.property'].sudo().search([('state', '=', 'new')], limit=3)
#         # breakpoint()
#         # Odoo Dynamic Snippets expect a list of dictionaries with '_record' key
#         records = [{'_record': prop} for prop in properties]
#         # breakpoint()
#         return request.env['ir.ui.view']._render_template("estate.dynamic_filter_template_property_cards_estate", {
#             'records': records
#         })

    # @http.route('/estate/get_property_data', type='json2', auth='public', website=True)
    # def get_property_data(self, limit=3, sort='name', category='all'):
    #     # 1. Map UI sort values to database fields
    #     order_map = {'price': 'expected_price', 'name': 'name'}
    #     order_field = order_map.get(sort, 'name')

    #     # 2. Build domain filter
    #     domain = [('state', '=', 'new')]
    #     if category and category != 'all':
    #         domain.append(('property_type_id.name', '=', category))

    #     # 3. Perform search
    #     properties = request.env['estate.property'].sudo().search(
    #         domain, 
    #         limit=int(limit), 
    #         order=order_field
    #     )
    
    #     # 4. Render the fragment
    #     # This returns the HTML string to the frontend JS
    #     return request.env['ir.ui.view']._render_template("estate.property_cards_content", {
    #         'properties': properties
    #     })

    # @http.route('/estate/get_property_data', type='jsonrpc', auth='public')
    # def get_property_data(self, limit=3, sort='name', category='all'):
    #     # Map UI sort values to database fields
    #     order_map = {'price': 'expected_price', 'name': 'name'}
    #     order_field = order_map.get(sort, 'name')

    #     # Build domain filter
    #     domain = [('state', '=', 'new')]
    #     if category != 'all':
    #         domain.append(('property_type_id.name', '=', category))

    #     properties = request.env['estate.property'].search(domain, limit=int(limit), order=order_field)

    #     if not properties:
    #         return ""
   
    #     return request.env['ir.ui.view']._render_template("estate.property_cards_content", {
    #         'properties': properties
    #     })

# class EstateController(http.Controller):
#     @http.route('/estate/get_property_data', type='jsonrpc', auth='public')
#     def get_property_data(self, limit, sort, category):
#         # 1. Fetch data based on params
#         properties = request.env['estate.property'].search([], limit=int(limit), order=sort)
        
#         # 2. Render a template with the results
#         if not properties:
#             return "" # The JS will handle the fallback
            
#         return request.env['ir.ui.view']._render_template("estate.property_cards_content", {
#             'properties': properties
#         })