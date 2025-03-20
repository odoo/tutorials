from odoo import http
from odoo.http import request

class EstatePropertyController(http.Controller):

    @http.route(["/properties/available","/properties/available/page/<int:page>"] ,website=True,auth='public')
    def available_property(self,page=1,**kw): 
        per_page=6
        page=(int)(page)
        tot_properties=request.env["estate.property"].sudo().search_count([('state','not in',['sold','cancelled']),('active','=',True)])    

        pager=request.website.pager(
            url='/properties/available',
            total=tot_properties,
            page=page,
            step=per_page
        )
        properties=request.env["estate.property"].sudo().search([('state','not in',['sold','cancelled']),('active','=',True)],limit=per_page,offset=pager['offset'])    
        return request.render("real_estate.properties_page",{
            "properties":properties,
            "pager":pager
        })
