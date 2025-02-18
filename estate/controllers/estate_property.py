from datetime import datetime

from odoo import http
from odoo.http import request


class EstateProperty(http.Controller):
    @http.route(["/properties","/properties/page/<int:page>"], type="http", auth="user", website=True)
    def properties_list_controller(self, page=1, **kwargs):
        listed_after = kwargs.get('listed_after')
        search_query = kwargs.get('search', '')
        step=6 
        offset = (page - 1) * step
        domain = [('state', 'in', ['new', 'offer received'])]
        if listed_after:
            listed_after_date = datetime.strptime(listed_after, "%Y-%m-%d")
            domain.append(('create_date', '>', listed_after_date))
        if search_query:
            domain.append(('name', 'ilike', search_query))
        total_properties = request.env["estate.property"].search_count(domain)
        properties = request.env["estate.property"].search(
            domain=domain, limit=step, offset=offset, order="create_date desc"
        )
        pager = request.website.pager(
            url="/properties", 
            total=total_properties, 
            step=step, 
            page=page
        )
        return request.render("estate.property_list_template", {
            'properties': properties,
            'pager': pager,
            'search_query': search_query
        })

    @http.route("/property/<int:property_id>", type="http", auth="user", website=True)
    def property_form_controller(self, property_id):
        property_details = request.env['estate.property'].browse(property_id)
        if not property_details.exists():
            return request.redirect('/properties')
        return request.render('estate.property_detail_template', {'property': property_details})
