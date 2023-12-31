from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.tools import add, float_compare, frozendict, split_every, format_date
from num2words import num2words



# ini buat di res_partner
class cust_diskon2(models.Model):
    _inherit = 'res.partner'
    diskon = fields.Integer('Diskon')
    kodevend = fields.Char(string='Kode Vendor', required=True)
    

# class barcode(models.Model):
#     _inherit = 'res.partner'
#     # _description = 'cust_diskon.cust_diskon'
#     diskon = fields.Integer('Diskon')

#--ini buat di order line nambahin dsc

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    # _description = 'cust_diskon.cust_diskon'
    # barcode = fields.Char('barcode',related='product_template_id.barcode')
    barcode = fields.Char('barcode', related='product_template_id.barcode')
    kode_hrg = fields.Char('Kode Harga', related='product_template_id.kode_hrg')


    @api.onchange ("product_template_id")
    def _onchange_product_template_id(self):
        if self.product_template_id:
        #  self.barcode  = self.product_template_id.barcode
            self.discount = self.order_id.partner_id.diskon
    
    @api.model
    def create(self, values):
        # Check if the product already exists in the order
        existing_line = self.search([
            ('order_id', '=', values.get('order_id')),
            ('product_id', '=', values.get('product_id')),
        ])

        if existing_line:
            # If the product exists, add a new line with the same product
            values['product_uom_qty'] = 1
            new_line = super(SaleOrderLine, existing_line).create(values)
            return new_line
        else:
            return super(SaleOrderLine, self).create(values)
    
    # @api.onchange('product_id')
    # def product_id_change_custom(self):
    #     if self.product_id:
    #         # If the product is not in the order, add a new line
    #         new_line = self.order_id.order_line.new({
    #             'product_id': self.product_id.id,
    #             'order_id': self.order_id.id,
    #             # Set other default values here
    #         })
    #         self.order_id.order_line += new_line
    #         self.create(new_line)
    
   
    # @api.model_create_multi
    # def create(self, vals_list):
    #         res = super().create(vals_list)
    #         if res.order_id.partner_id.diskon != 0:
    #             res.discount = res.order_id.partner_id.diskon
    #         return res

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    # _description = 'cust_diskon.cust_diskon'
    diskon = fields.Integer('Diskon customer') 
    barcode = fields.Char(string='Barcode')
    kode_hrg = fields.Char('Kode Harga')


    @api.onchange('barcode')
    def add_new_order_line(self):
        print(self)
        if self.barcode != False:
            product = self.env['product.product'].search([('barcode', '=', self.barcode)], limit=1)
            if product:
                order_line_data = {
                    'product_id': product.id,
                    'product_uom_qty': 1,  # Adjust quantity as needed
                    'discount' : self.partner_id.diskon
                    # Add other required fields
                }
                self.order_line = [(0, 0, order_line_data)]
            self.barcode = ''

    
    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id:
            self.diskon  = self.partner_id.diskon
            if self.order_line:
                for line in self.order_line:
                    line.discount = self.diskon

