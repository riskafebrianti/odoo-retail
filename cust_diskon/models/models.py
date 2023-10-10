# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class cust_diskon(models.Model):
#     _name = 'cust_diskon.cust_diskon'
#     _description = 'cust_diskon.cust_diskon'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
