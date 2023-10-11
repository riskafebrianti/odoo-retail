from odoo import models, fields, api


class cust_diskon(models.Model):
    _inherit = 'res.partner'
    # _description = 'cust_diskon.cust_diskon'
    diskon = fields.Integer('Diskon')

#--

class cust_diskon(models.Model):
    _inherit = 'sale.order.line'
    # _description = 'cust_diskon.cust_diskon'
    # barcode = fields.Char('barcode',related='product_template_id.barcode')
    barcode = fields.Char('barcode')

    @api.onchange("product_template_id")
    def _onchange_product_template_id(self):
        if self.product_template_id:
         self.barcode  = self.product_template_id.barcode

    @api.model_create_multi
    def create(self, vals_list):
            res = super().create(vals_list)
            if res.order_id.partner_id.diskon != 0:
                res.discount = res.order_id.partner_id.diskon
            return res
    
class cust_diskonn(models.Model):
    _inherit = 'sale.order'
    # _description = 'cust_diskon.cust_diskon'
    diskonn = fields.Float('Diskon customer') 


# class cust_diskonsale(models.Model):
#     _inherit = 'pos.order'
#      _description = 'cust_diskon.cust_diskon'
#     diskon = fields.Float('Diskon Custsomer')
    # partner_id = fields.Many2one("res.partner", string="Partner")

# class cust_diskonPOS(models.Model):
#     _inherit = 'loyalty.program'
#     # _description = 'cust_diskon.cust_diskon'
#     diskon = fields.Float('Diskon Customer')
#     # partner_id = fields.Many2one("res.partner", string="Partner")

# buatautocomplite
    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id:
         self.diskonn  = self.partner_id.diskon
        # self.discount  = self.partner_id.discount
        # self.description = "Default description for %s" % (self.partner_id.diskon)
        
  
   
    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100

    # @api.onchange('diskon')
    # def _onchange_vehicle(self):
    #     sale.order = "Rental Order for %s" % self.vehicle_id.name