from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.tools import add, float_compare, frozendict, split_every, format_date
from num2words import num2words



# ini buat di res_partner
class cust_diskon2(models.Model):
    _inherit = 'res.partner'
    diskon = fields.Integer('Diskon')
    kodevend = fields.Char(string='Kode Vendor')

    def number_to_words(self, amount, currency):

        if currency.name == 'IDR':
            number2words = num2words(amount, lang='id')
            check_number2words = number2words.replace(' koma nol', '')
            amount_to_words = check_number2words.title()+' Rupiah'
        else:
            amount_decimal_check = amount - int(amount)

            if amount_decimal_check == 0.00:
                number2words = num2words(amount, lang='en').title()
            else:
                amount_decimal = '%.2f' % amount
                
                x = amount_decimal.rfind('.')
                amount_before_comma = amount_decimal[:x]
                amount_after_comma = amount_decimal[x+1:]

                number2words1 = num2words(int(amount_before_comma), lang='en').title()
                number2words2 = num2words(int(amount_after_comma), lang='en').title()

                number2words = number2words1+' Point '+number2words2

            if currency.name == 'USD':
                amount_to_words = 'United State Dollar '+number2words
            else:
                amount_to_words = currency.name+' '+number2words

        return amount_to_words


# class barcode(models.Model):
#     _inherit = 'res.partner'
#     # _description = 'cust_diskon.cust_diskon'
#     diskon = fields.Integer('Diskon')

#--ini buat di order line nambahin dsc


class report(models.Model):
    _inherit = 'account.move'

    # hide_post_button = fields.Boolean(compute='_compute_hide_post_button', readonly=True)
    to_check = fields.Boolean(
    string='To Check',
    default=True,
    tracking=True,
    help="testitng",
)
    
    tess = fields.Char('tess')
    


    def number_to_words(self, amount, currency):

        if currency.name == 'IDR':
            number2words = num2words(amount, lang='id')
            check_number2words = number2words.replace(' koma nol', '')
            amount_to_words = check_number2words.title()+' Rupiah'
        else:
            amount_decimal_check = amount - int(amount)

            if amount_decimal_check == 0.00:
                number2words = num2words(amount, lang='en').title()
            else:
                amount_decimal = '%.2f' % amount
                
                x = amount_decimal.rfind('.')
                amount_before_comma = amount_decimal[:x]
                amount_after_comma = amount_decimal[x+1:]

                number2words1 = num2words(int(amount_before_comma), lang='en').title()
                number2words2 = num2words(int(amount_after_comma), lang='en').title()

                number2words = number2words1+' Point '+number2words2

            if currency.name == 'USD':
                amount_to_words = 'United State Dollar '+number2words
            else:
                amount_to_words = currency.name+' '+number2words

        return amount_to_words
    

    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    # _description = 'cust_diskon.cust_diskon'
    # barcode = fields.Char('barcode',related='product_template_id.barcode')
    barcode = fields.Char('barcode', related='product_template_id.barcode')
    kode_hrg = fields.Char('Kode Harga', related='product_template_id.kode_hrg')
    add_diskon = fields.Monetary(string='Additional Discount', store=True)
    # add_diskon = fields.Monetary(string='Additional Discount', store=True)


    @api.onchange ("product_template_id")
    def _onchange_product_template_id(self):
        if self.product_template_id:
        #  self.barcode  = self.product_template_id.barcode
            self.discount = self.order_id.partner_id.diskon
    
    @api.onchange('add_diskon')
    def _onchange_add_diskon(self):
        if self.add_diskon:
            self.discount = (self.add_diskon / self.price_unit) * 100
            print()
    

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
    add_diskon_total = fields.Monetary(string='Additional Discount', store=True)
    


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

    # @api.depends('order_line.price_subtotal', 'order_line.price_tax', 'order_line.price_total')
    # def _compute_amounts(self):
    #     """Compute the total amounts of the SO."""
    #     for order in self:
    #         order_lines = order.order_line.filtered(lambda x: not x.display_type)

    #         if order.company_id.tax_calculation_rounding_method == 'round_globally':
    #             tax_results = self.env['account.tax']._compute_taxes([
    #                 line._convert_to_tax_base_line_dict()
    #                 for line in order_lines
    #             ])
    #             totals = tax_results['totals']
    #             amount_untaxed = totals.get(order.currency_id, {}).get('amount_untaxed', 0.0)
    #             amount_tax = totals.get(order.currency_id, {}).get('amount_tax', 0.0)
    #         else:
    #             amount_untaxed = sum(order_lines.mapped('price_subtotal'))
    #             amount_tax = sum(order_lines.mapped('price_tax'))

    #         order.amount_untaxed = amount_untaxed
    #         order.amount_tax = amount_tax
    #         order.amount_total = order.amount_untaxed + order.amount_tax
    
    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id:
            self.diskon  = self.partner_id.diskon
            if self.order_line:
                for line in self.order_line:
                    line.discount = self.diskon

