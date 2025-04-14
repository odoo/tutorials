# -*- coding: utf-8 -*-
# from odoo import http


# class OwlTutorials(http.Controller):
#     @http.route('/owl_tutorials/owl_tutorials', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/owl_tutorials/owl_tutorials/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('owl_tutorials.listing', {
#             'root': '/owl_tutorials/owl_tutorials',
#             'objects': http.request.env['owl_tutorials.owl_tutorials'].search([]),
#         })

#     @http.route('/owl_tutorials/owl_tutorials/objects/<model("owl_tutorials.owl_tutorials"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('owl_tutorials.object', {
#             'object': obj
#         })

