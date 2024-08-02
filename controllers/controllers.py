# -*- coding: utf-8 -*-
# from odoo import http


# class Knance(http.Controller):
#     @http.route('/knance/knance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/knance/knance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('knance.listing', {
#             'root': '/knance/knance',
#             'objects': http.request.env['knance.knance'].search([]),
#         })

#     @http.route('/knance/knance/objects/<model("knance.knance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('knance.object', {
#             'object': obj
#         })

