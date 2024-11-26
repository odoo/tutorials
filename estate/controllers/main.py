from odoo.http import Controller, request, route


class EstatePropertyControllers(Controller):
    @route("/active_properties", auth="public", website=True)
    def list_active_properties(self, page=1):
        page = int(page)
        limit = 3
        offset = (page - 1) * limit

        properties = (
            request.env["estate.property"]
            .sudo()
            .search_read(
                [
                    "&",
                    ("active", "=", True),
                    ("state", "in", ["new", "offer_received"]),
                ],
                fields=["name", "expected_price", "description"],
                limit=limit,
                offset=offset,
            )
        )
        total_properties = (
            request.env["estate.property"]
            .sudo()
            .search_count(
                ["&", ("active", "=", True), ("state", "in", ["new", "offer_received"])]
            )
        )
        total_pages = (total_properties + limit - 1) // limit

        return request.render(
            "estate.property_list_template",
            {
                "properties": properties,
                "current_page": page,
                "total_pages": total_pages,
            },
        )

    @route("/property/<int:property_id>", auth="public", website=True)
    def property_detail(self, property_id, **kw):
        property = request.env["estate.property"].sudo().browse(property_id)
        if property.exists():
            # print("*-*-" * 100)
            # print(property.image)
            return request.render(
                "estate.property_detail_template", {"property": property}
            )
        else:
            return request.not_found()

    # Route for logged-in users
    @route("/private_page", auth="user")
    def private_page(self):
        """
        Route accessible only to logged-in users.
        - Authentication is required.
        - Useful for internal interfaces or APIs where user identification is necessary.
        """
        return """
            <h1>Private Page</h1>
            <p>This page is for logged-in users only.</p>
            <p>Authentication is required to access this route.</p>
            <p>It is commonly used for internal user interfaces or secure APIs.</p>
        """

    # Route with no authentication or session required
    @route("/none_type", auth="none", methods=["GET"], csrf=False)
    def api_data(self):
        return """
        Stateless API route with no authentication or session.
        <p><i><b>- Auth type: 'none' (no user/session context).</p></i></b>
        <p><i><b>- CSRF disabled for this route.</p></i></b>
        <p><i><b>- Suitable for integration scenarios requiring lightweight stateless operations.</p></i></b>
        """

    # Route accessible only to administrators
    @route("/admin_page", auth="admin")
    def admin_page(self):
        """
        Route accessible only to administrators.
        - Auth type: 'admin'.
        - Suitable for pages or actions restricted to users with admin rights.
        """
        return """
            <h1>Admin Page</h1>
            <p>This page is restricted to administrators only.</p>
            <p>It is used for critical or sensitive backend operations.</p>
        """

    # Route for portal users with website context
    @route("/portal_users", auth="portal", website=True)
    def my_orders(self):
        """
        Route for portal users with website context.
        - Auth type: 'portal' (only users with portal access can view).
        - Includes website context for frontend integration.
        - Common use case: showing customer-specific data like orders or invoices.
        """
        return """
            <h1>Portal Users Page</h1>
            <p>This page is only accessible to portal users (e.g., customers or suppliers).</p>
            <p>It is integrated with the website module for a frontend display.</p>
        """
