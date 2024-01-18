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
#    barcode = fields.Char('barcode',compute='_compute_product_id')
    kode_hrg = fields.Char('Kode Harga')
    brand = fields.Char('Brand')

    # @api.depends('product_template_id')
    # def _compute_product_template_id(self):
    #     if self.product_template_id:
    #         self.barcode  = self.product_id.barcode


class Product(models.Model):
    _inherit = 'product.product'
    # barcode = fields.Char('barcode',compute='_compute_product_id',store=True,)

    # @api.depends ("product_product_id")
    # def _compute_product_id(self):
    #     # if self.barcode:
    #     self.barcode  = self.id

    @api.model
    def create(self,vals):
        res = super(Product,self).create(vals)
        res.barcode = res.id
        print(vals)
        return res









    # @api.depends ("product_tmpl_id")
    # def _compute_product_tmpl_id(self):
    #     if self.product_template_id:
    #     #  self.barcode  = self.product_template_id.barcode
    #         self.barcode = self.product_tmpl_id
    # # aksi = fields.Char('aksi')

    # def set_partner_ref(self):
    #     return {
    #     'name': 'My Window',
    #     'domain': [],
    #     'res_model': 'sale.order',
    #     'type': 'ir.actions.act_window',
    #     'view_mode': 'tree',
    #     'view_type': 'widget',
    #     'context': {},
    #     'target': 'new',
    # }