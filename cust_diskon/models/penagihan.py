from odoo import models, fields, api


class Custdiskon(models.Model):
    _inherit = 'res.partner'
    # _description = 'cust_diskon.cust_diskon'
    # barcode = fields.Char('barcode',related='product_template_id.barcode')
    kode_hrg = fields.Char('Kode Harga')
  