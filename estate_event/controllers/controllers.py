# -*- coding: utf-8 -*-
# from odoo import http


# class EstateEvent(http.Controller):
#     @http.route('/estate_event/estate_event', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estate_event/estate_event/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('estate_event.listing', {
#             'root': '/estate_event/estate_event',
#             'objects': http.request.env['estate_event.estate_event'].search([]),
#         })

#     @http.route('/estate_event/estate_event/objects/<model("estate_event.estate_event"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estate_event.object', {
#             'object': obj
#         })

