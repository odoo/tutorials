from odoo import http
from odoo.http import Controller, request

class EstatePropertyController(Controller):
    
    # @http.route(["/properties", "/properties/page/<int:page>"], type="http", auth="public", website=True)
    @http.route(["/properties", "/properties/page/<int:page>"], type="http", auth="public", website=True)
    def show_property_list(self, filter_domain ="all", page=1, **kwargs):

        '''
        Tasks : (do when free)
        :add default page - /properties/page/1
                            update it in template - form > actions such that it remains in all pages   
        add search functionality 
            - done via appending conditions in domain
            - create a search bar in template list
            - configure in inside a form with submit button trigger post method
        add ranger filters for price
        add a option to upload images for property
            - allow only .png or .jpeg files
            - resize it to default dimensions 
        '''

        filter_key = filter_domain.lower()

        def get_filter(domain_filter):
            if domain_filter == "available":
                return [("state", "in", ["new", "offer_received"])]
            elif domain_filter == "sold":
                return [("state", "=", "sold")]
            else:
                return []

        domain = get_filter(filter_key)

        properties_count = request.env["estate.property"].sudo().search_count(domain)

        page_size = 9
        pager = request.website.pager(
            url='/properties',
            total=properties_count,
            page=page,
            step=page_size
        )

        property_list = request.env["estate.property"].sudo().search(domain, limit=page_size, offset=pager["offset"])
        return request.render("estate.property_list_website_template", {"property_list": property_list, "filter_domain": filter_domain, "pager": pager})
    
    @http.route("/properties/<int:property_id>", type="http", auth="public", website=True)
    def show_property_details(self, property_id):
        property = request.env["estate.property"].sudo().browse(property_id)
        return request.render("estate.property_details_website_template", {"property":property})
