from odoo import http


class Properties(http.Controller):
    @http.route(['/properties','/properties/page/<int:page>'],auth='public',website=True)
    def list_properties(self, page=1, **kwargs):
        property = http.request.env['estate.property']
        per_page = 6
        domain = [('status','in',['new','offer_received'])]
        total_properties = property.search_count(domain)
        properties = property.search(domain,offset=(page-1)*per_page,limit=per_page)
        pager = http.request.website.pager(
            url='/properties',
            total=total_properties,
            page=page,
            step=per_page
        )
        return http.request.render(
            'estate.property_listing_template',
            {'properties': properties,'pager': pager}
        )

    @http.route(['/property/<model("estate.property"):property>'],type='http',auth="public",website=True)
    def property_details(self,property,**kwargs):
        return http.request.render(
            'estate.property_details_template',
            {'property': property}
        )
