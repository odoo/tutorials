from odoo import http
from odoo.http import request

class EstateController(http.Controller):
    @http.route(['/view_property','/view_property/page/<int:page>'],type='http',auth='public',website=True)
    def view_property_web(self,page=1):
        page = int(page)
        total_records = request.env['estate.property'].sudo().search_count([('state','!=','canceled')])
        page_size =4
        offset=(page-1)*page_size
        properties = request.env['estate.property'].sudo().search([('state','!=','canceled')],limit=page_size,offset=offset)
        return http.request.render('estate.view_property_list', {
            'properties': properties,
            'pager': request.website.pager(url="/view_property", total=total_records, page=page, step=page_size),
        })
    
    @http.route('/view_property/search',type='http',auth='public',website='True')
    def estate_property_search(self,search=None,selected_date=None):
        domain=[]
        if search:
            domain += [('name','ilike',search)]
        if selected_date:
            domain += [('create_date','>=',selected_date)]
        property = request.env['estate.property'].sudo().search(domain)
        return request.render('estate.view_property_list',{
            'properties':property
        })
    
    @http.route('/view_property/<int:property_id>', type='http', auth='public', website=True)
    def property_details(self, property_id):
        property_obj = request.env['estate.property'].sudo().browse(property_id)
        return http.request.render('estate.view_property_form', {
            'property': property_obj,
        })