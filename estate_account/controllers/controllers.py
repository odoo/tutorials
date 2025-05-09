# -*- coding: utf-8 -*-
# from odoo import http


# class EstateAccount(http.Controller):
#     @http.route('/estate_account/estate_account', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estate_account/estate_account/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('estate_account.listing', {
#             'root': '/estate_account/estate_account',
#             'objects': http.request.env['estate_account.estate_account'].search([]),
#         })

#     @http.route('/estate_account/estate_account/objects/<model("estate_account.estate_account"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estate_account.object', {
#             'object': obj
#         })

