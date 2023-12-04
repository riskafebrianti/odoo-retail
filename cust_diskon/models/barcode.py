from odoo import models, fields, api

# class cust_js(models.Model):
#     _inherit = 'sale.order'
#     # _description = 'cust_diskon.cust_diskon'
#     # diskon = fields.Float('Diskon customer') 
    
#     name = fields.Char(string='tutorial name', required=True)
#     number_of_videos = fields.Integer(string='number d', required=True)


class cust_diskon(models.Model):
    _inherit = 'product.template'
    # _description = 'cust_diskon.cust_diskon'
    # barcode = fields.Char('barcode',related='product_template_id.barcode')
    kode_hrg = fields.Char('Kode Harga')
    brand = fields.Char('brand')

    # aksi = fields.Char('aksi')

    def set_partner_ref(self):
        return {
        'name': 'My Window',
        'domain': [],
        'res_model': 'sale.order',
        'type': 'ir.actions.act_window',
        'view_mode': 'tree',
        'view_type': 'widget',
        'context': {},
        'target': 'new',
    }