from odoo import http
from odoo.http import request

class RealEstateController(http.Controller):

    @http.route(
        ["/properties","/properties/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def list_properties(self, **kwargs):
        per_page = 6  # Number of properties per page
        
        # Get the page number from the request URL (default is 1)
        page = int(kwargs.get('page', 1))

        # Get the selected date from the request URL
        listed_after = kwargs.get('listed_after')

        search_query = kwargs.get('search')

        # Define the domain for filtering properties
        domain = [
            ('state', 'in', ['new', 'offer_received']),
            ('active', '=', True)
        ]

        # Apply date filter if a date is selected
        if listed_after:
            domain.append(('create_date', '>=', listed_after))

        if search_query:
            domain.append(('name', 'ilike', search_query))

        # Fetch total count of filtered properties
        total_properties = request.env['estate.property'].search_count(domain)

        # Fetch paginated properties with applied filters
        properties = request.env['estate.property'].search(
            domain, limit=per_page, offset=(page - 1) * per_page, order="create_date desc"
        )

        # Generate pagination URLs with filters
        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=per_page,
            url_args={"listed_after": listed_after,"search": search_query},
        )

        return request.render(
            "estate.property_list_template",
            {
                "properties": properties,
                "pager": pager,  # ✅ Pass pager to template
                'listed_after': listed_after or '',
            },
        )
