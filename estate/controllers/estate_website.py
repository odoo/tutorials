from odoo import http
from odoo.http import request


class EstateWebsite(http.Controller):
    @http.route(['/property', "/property/page/<int:page>"], type="http", auth="public",website=True)
    def list_properties(self, page=1, status="all", min_price=None, max_price=None, **kwargs):
        step = 6
        offset = (page-1)*step
        domain = [('company_id', '=', request.env.company.id)]  # Filter by company
        if status=="all":
            domain.append(('state', 'in', ["new", "offer_received"]))
        else:
            domain.append(('state', '=', status))
        # Filter by Min Price if provided
        if min_price:
            domain.append(('expected_price', '>=', float(min_price)))
        # Filter by Max Price if provided
        if max_price:
            domain.append(('expected_price', '<=', float(max_price)))
        # Fetch properties based on the dynamic domain
        properties = request.env['estate.property'].sudo().search(domain, limit=step, offset=offset)
        total_properties = request.env["estate.property"].sudo().search_count(domain)
        url_args = {
            'status': status or "",
            'min_price': min_price or "",
            'max_price': max_price or ""
        }
        pager = request.website.pager(
            url="/property", total=total_properties, step=step, page=page, url_args=url_args
        )
        # Pass the selected filter values to the template for form retention
        return request.render("estate.listing_page", {
            'properties': properties,
            "pager": pager
        })

    @http.route("/property/<model('estate.property'):property>", type="http", auth="public",website=True)
    def property_detail(self, property, **kwargs):
        return request.render("estate.property_detail_page", {"property": property})
