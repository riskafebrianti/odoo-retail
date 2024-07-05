

    # @api.depends('order_line.price_total')
    # def _compute_total_amount(self):
    #     for order in self:
    #         order.total_amount = sum(order.order_line.mapped('price_total'))