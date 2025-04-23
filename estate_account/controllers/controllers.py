# -*- coding: utf-8 -*-
# from odoo import http


# class 18.0-estate-x-invoicing(http.Controller):
#     @http.route('/18.0-estate-x-invoicing/18.0-estate-x-invoicing', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/18.0-estate-x-invoicing/18.0-estate-x-invoicing/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('18.0-estate-x-invoicing.listing', {
#             'root': '/18.0-estate-x-invoicing/18.0-estate-x-invoicing',
#             'objects': http.request.env['18.0-estate-x-invoicing.18.0-estate-x-invoicing'].search([]),
#         })

#     @http.route('/18.0-estate-x-invoicing/18.0-estate-x-invoicing/objects/<model("18.0-estate-x-invoicing.18.0-estate-x-invoicing"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('18.0-estate-x-invoicing.object', {
#             'object': obj
#         })

