# -*- coding: utf-8 -*-
# from odoo import http


# class Estate(http.Controller):
#     @http.route('/estate/estate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estate/estate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('estate.listing', {
#             'root': '/estate/estate',
#             'objects': http.request.env['estate.estate'].search([]),
#         })

#     @http.route('/estate/estate/objects/<model("estate.estate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estate.object', {
#             'object': obj
#         })

