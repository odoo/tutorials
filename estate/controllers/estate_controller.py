from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website

class EstatePropertyController(http.Controller):
    @http.route(['/properties','/properties/page/<int:page>'], auth="public", website=True)
    def my_site(self, page=1, **kwargs):
        listed_after = kwargs.get('listed_after')
        searching_name=kwargs.get('property_name')
        page = int(page)
        domain = [('status', 'in', ['new', 'offer_received'])]

        if listed_after:
            try:
                listed_after_date = datetime.strptime(listed_after, '%Y-%m-%d').date()
                domain.append(('date_availability', '>', listed_after_date))
            except ValueError:
                listed_after_date = None
        
        if searching_name:
            domain.append('|')
            domain.append(('name','ilike',searching_name))
            domain.append(('description','ilike',searching_name))

        properties = request.env['estate.property'].sudo().search(
            domain, order='date_availability desc', limit=6, offset=(page-1)*6
        )

        total_properties = request.env['estate.property'].sudo().search_count(domain)
        #total_pages = (total_properties // 6) + (1 if total_properties % 6 != 0 else 0)
        
        pager = request.website.pager(
            url="/properties",
            total=total_properties, 
            page=page,        # the page arg.
            step=6,   # 6 in our case
            url_args=kwargs  # Preserve filters like 'listed_after'
        )

        return request.render("estate.property_page", {
            'properties': properties,
            'pager': pager,  # Pass the pager to the template , here no need to explicitly add total_pages and page. 
        })
    
    @http.route('/properties/<int:property_id>', auth='public', website=True)
    def property_detail(self, property_id, **kwargs):
        property = request.env['estate.property'].sudo().browse(property_id)
        
        if not property.exists():
            return request.not_found()

        return request.render('estate.property_detail_page', {
            'property': property
        })



"""
Pagination by website.pager (built in):

    pager = request.website.pager(
            url="/properties",
            total=total_properties, 
            page=page,        # the page arg.
            step=per_page,   # 6 in our case
            url_args=kwargs  # Preserve filters like 'listed_after'
        )

    Then render and in 
        return request.render("estate.property_page", {
            'properties': properties,
            'pager': pager,  # Pass the pager to the template , here no need to explicitly add total_pages and page. 
        })

        in xml:
            <t t-if="pager">
                <t t-call="website.pager">
                    <t t-set="pager" t-value="pager"/>
                </t>
            </t> 
            and done.
"""