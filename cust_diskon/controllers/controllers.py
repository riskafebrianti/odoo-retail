# -*- coding: utf-8 -*-
# from odoo import http


# class CustDiskon(http.Controller):
#     @http.route('/cust_diskon/cust_diskon', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cust_diskon/cust_diskon/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cust_diskon.listing', {
#             'root': '/cust_diskon/cust_diskon',
#             'objects': http.request.env['cust_diskon.cust_diskon'].search([]),
#         })

#     @http.route('/cust_diskon/cust_diskon/objects/<model("cust_diskon.cust_diskon"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cust_diskon.object', {
#             'object': obj
#         })
