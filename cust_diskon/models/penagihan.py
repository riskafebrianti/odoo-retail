from odoo import models, fields, api


class Custdiskon(models.Model):
    _inherit = 'res.partner'
    # _description = 'cust_diskon.cust_diskon'
    # barcode = fields.Char('barcode',related='product_template_id.barcode')
    kode_hrg = fields.Char(string='Kode Harga', required=True)
  
    invoice_list = fields.One2many('account.move', 'partner_id',
                                    string="Invoice Details",
                                    readonly=True,
                                    domain=(
                                    [('payment_state', '=', 'not_paid'),
                                        ('move_type', '=', 'out_invoice'),
                                        ('move_type', '=', 'out_invoice'),
                                        ('state','=','posted')]))
    
    periode = fields.Char(string='Periode')
    

