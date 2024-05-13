import os
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
#     invoiced = fields.Char(compute='_compute_invoiced', string='invoiced')
    
#     # @api.depends('picking_id')
#     def _compute_invoiced(self):
#         if self.picking_ids:
#             print(self)

        

class StockMove(models.Model):
    _inherit = "stock.move"


    def action_show_details(self):
            """ Returns an action that will open a form view (in a popup) allowing to work on all the
            move lines of a particular move. This form view is used when "show operations" is not
            checked on the picking type.
            """
            self.ensure_one()

            # If "show suggestions" is not checked on the picking type, we have to filter out the
            # reserved move lines. We do this by displaying `move_line_nosuggest_ids`. We use
            # different views to display one field or another so that the webclient doesn't have to
            # fetch both.
            if self.picking_type_id.show_reserved:
                view = self.env.ref('stock.view_stock_move_operations')
            else:
                view = self.env.ref('stock.view_stock_move_nosuggest_operations')

            if self.product_id.tracking == "serial" and self.state == "assigned":
                self.next_serial = self.env['stock.lot']._get_next_serial(self.company_id, self.product_id)
# Lot automated
            # Get the current date
            current_date = datetime.now()

            # Get the year and month components
            year = current_date.year
            month = current_date.month

            # Format the year and month as YYMM
            formatted_date = "{:02d}".format(month) + str(year)[2:5]
            if self.has_tracking == 'lot':
                if self.product_id.default_code:
                    if self.purchase_line_id.order_id.partner_id.kodevend:
                        kode_vend = self.purchase_line_id.order_id.partner_id.kodevend +'-'+ formatted_date +'-'+ self.product_id.default_code
                        having_lot = self.env['stock.lot'].search([
                            ('name','=',kode_vend)
                        ],limit=1)

                        if having_lot.id == False:
                            self.env['stock.lot'].create({
                                'name': kode_vend,
                                'product_id': self.product_id.id,
                                'company_id':self.company_id.id
                            })
                    else:
                        raise UserError('Silahkan Isi Kode Vendor ...')
                else:
                    raise UserError('Silahkan Isi Internal Reference ...')
                for xrec in self.move_line_ids:
                    id_lot = self.env['stock.lot'].search([
                        ('name','=',kode_vend)
                    ],limit=1).id
                    xrec.lot_id = id_lot
                    # for xpo_line in self.picking_id.lite_purchase_order_id.order_line.filtered(lambda x: x.product_id.id == xrec.product_id.id and x.product_id.default_code == xrec.product_id.default_code):
                    # xcount = self.picking_id.lite_purchase_order_id.order_line.filtered(lambda x: x.product_id.id == xrec.product_id.id)
                    # if len(xcount) == 1:
                    #     for xpo_line in self.picking_id.lite_purchase_order_id.order_line.filtered(lambda x: x.product_id.id == xrec.product_id.id):       
                    #         xrec.lot_id = xpo_line.lot_id.id if xpo_line.lot_id.id else False
                        
                        
            return {
                'name': _('Detailed Operations'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'stock.move',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': self.id,
                'context': dict(
                    self.env.context,
                    show_owner=self.picking_type_id.code != 'incoming',
                    show_lots_m2o=self.has_tracking != 'none' and (self.picking_type_id.use_existing_lots or self.state == 'done' or self.origin_returned_move_id.id),  # able to create lots, whatever the value of ` use_create_lots`.
                    show_lots_text=self.has_tracking != 'none' and self.picking_type_id.use_create_lots and not self.picking_type_id.use_existing_lots and self.state != 'done' and not self.origin_returned_move_id.id,
                    show_source_location=self.picking_type_id.code != 'incoming',
                    show_destination_location=self.picking_type_id.code != 'outgoing',
                    show_package=not self.location_id.usage == 'supplier',
                    show_reserved_quantity=self.state != 'done' and not self.picking_id.immediate_transfer and self.picking_type_id.code != 'incoming'
                ),
            }