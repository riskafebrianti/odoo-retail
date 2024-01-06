from odoo import models, fields, api
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_amount = fields.Monetary(string='Total Amount', compute='_compute_total_amount', store=True)

    @api.depends('order_line.price_total')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(order.order_line.mapped('price_total'))