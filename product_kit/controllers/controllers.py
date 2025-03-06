# -*- coding: utf-8 -*-
# from odoo import http


# class ProductKit(http.Controller):
#     @http.route('/product_kit/product_kit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_kit/product_kit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_kit.listing', {
#             'root': '/product_kit/product_kit',
#             'objects': http.request.env['product_kit.product_kit'].search([]),
#         })

#     @http.route('/product_kit/product_kit/objects/<model("product_kit.product_kit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_kit.object', {
#             'object': obj
#         })

