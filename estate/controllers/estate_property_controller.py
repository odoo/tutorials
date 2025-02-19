from odoo import http, fields
from odoo.http import request



class EstatePropertyController(http.Controller):

    @http.route(['/properties','/properties/page/<int:page_no>'], type='http', auth='public', website = True)
    def list_properties(self,page_no = 1 , **kwargs):
        domain = [('state','in',["new","offer_accepted","offer_received"])]

        date_listed = kwargs.get('date_listed')
        if date_listed:
            filter_date = fields.Datetime.to_datetime(date_listed + " 00:00:00")
            domain.append(('create_date','>=', filter_date))

        total_count = request.env['estate.property'].sudo().search_count(domain)
        per_page = 6
        offset = (page_no - 1) * per_page
        properties = request.env['estate.property'].sudo().search(domain, limit = per_page, offset= offset)
        pager = request.website.pager(
            url = "/properties",
            total = total_count,
            page = page_no,
            step = per_page,
            scope = 3,
            url_args= {'date_listed':date_listed } if date_listed else {}
        )
        return request.render('estate.list_properties_template',{ 'properties': properties, 'pager':pager})

    @http.route('/properties/<int:property_id>', type='http', auth='public', website = True)
    def show_property_details(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse((property_id,))
        return request.render('estate.property_detail_template',{'property':property})
