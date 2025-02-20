from odoo import http
from odoo.http import request

class MyController(http.Controller):
    @http.route(['/properties', '/properties/page/<int:page>'], type='http', auth='public', website=True)
    def raj(self, page=1,*kwargs):
        all_properties = request.env["estate.property"]
        total = all_properties.search_count([])
        pager = request.website.pager(
            url='/properties',
            total=total,
            page=page,
            step=4
            )
        return request.render("estate.template_properties_webview",qcontext={'properties': all_properties.search([],offset=(page-1)* 4, limit=4),'pager': pager})
