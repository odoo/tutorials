from datetime import datetime
from odoo import http
from odoo.http import request


class EstateController(http.Controller):

    @http.route(["/properties","/properties/page/<int:page>"], type="http", auth="user", website=True)
    def estate_list_controller(self, page=1, **kwargs):
        search_query = kwargs.get('search', '') 
        listed_after = kwargs.get('listed_after')
        step=6 
        offset = (page - 1) * step
        domain = [
            '|', ('state', '=', 'new'),
            ('state', '=', 'offer_received')
        ]
        if listed_after:
            listed_after_date = datetime.strptime(listed_after, "%Y-%m-%d")
            domain.append(('create_date', '>', listed_after_date))
        
        if search_query:
            domain.append(('name', 'ilike', search_query))

        total_properties = request.env["estate.property"].search_count(domain)
        properties = request.env["estate.property"].search(domain=domain, limit=step, offset=offset, order="create_date desc")
        pager = request.website.pager(
            url="/properties", 
            total=total_properties, 
            step=step, 
            page=page,
            url_args={'search': search_query}
        )
        return request.render("estate.estate_property_list_template", {
            'properties': properties,
            'pager': pager,
            'search_query': search_query,
            'listed_after': listed_after
        })

    @http.route("/property/<int:property_id>", type="http", auth="user", website=True)
    def estate_form_controller(self, property_id):
        single_property = request.env['estate.property'].browse(property_id)
        if not single_property.exists():
            return request.redirect('/properties')

        return request.render('estate.estate_property_detail_template', {'property': single_property})
