from odoo import api, fields, models, _


class InventoryMasterMoves(models.Model):
    _name = 'inv.master.moves'

    prd_name = fields.Char('Product')
    prd_type_id = fields.Char('Product Category')
    internal_ref_num = fields.Char('Internal reference No')
    unit_of_m = fields.Char('UOM')
    store_inv = fields.Char('From Location')
    store_inv_to = fields.Char('To location')
    batch_no = fields.Char('Lot No')
    opening = fields.Char('On Hand')
    inward = fields.Float('Inward Qty')
    outward = fields.Float('Outward Qty')
    balance = fields.Char('Balance Qty')
    price_rate = fields.Float('Rate')
    rate_value = fields.Char('Stock Value')
    create_time = fields.Datetime('Stock Move Time')


class ToInheritStockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.constrains('state')
    def button_validate_create_master_data(self):

        for rec in self:
            if rec.picking_type_code == 'outgoing':
                if rec.state == 'done':

                    for lines in rec.move_ids_without_package:
                        free_avl = self.env['product.product'].search(
                            [('name', '=', lines.product_id.name)])
                        free_quel = free_avl.free_qty

                        s_prd_unit_rate = lines.price_unit
                        s_inv_tot_val = lines.product_id.standard_price * free_quel

                        self.env['inv.master.moves'].create({
                            'create_time': fields.datetime.now(),
                            'prd_name': lines.product_id.name,
                            'prd_type_id': lines.product_id.categ_id.name,
                            'internal_ref_num': lines.product_id.default_code,
                            'unit_of_m': lines.product_id.uom_id,
                            'store_inv': lines.location_id.name,
                            'store_inv_to': rec.partner_id.name,
                            'batch_no': lines.lot_ids.name,
                            'opening': lines.stock_on_hand_indent,
                            'outward': lines.quantity_done,
                            'balance': str(free_quel),
                            'price_rate': s_prd_unit_rate,
                            'rate_value': str(s_inv_tot_val),
                        })

            elif rec.picking_type_code == 'incoming':
                if rec.state == 'done':

                    for lines in rec.move_ids_without_package:
                        free_avl = self.env['product.product'].search(
                            [('name', '=', lines.product_id.name)])
                        free_quel = free_avl.free_qty

                        p_prd_unit_rate = lines.price_unit
                        p_inv_tot_val = lines.product_id.standard_price * free_quel

                        self.env['inv.master.moves'].create({
                            'create_time': fields.datetime.now(),
                            'prd_name': lines.product_id.name,
                            'prd_type_id': lines.product_id.categ_id.name,
                            'internal_ref_num': lines.product_id.default_code,
                            'unit_of_m': lines.product_id.uom_id,
                            'store_inv': lines.partner_id.name,
                            'store_inv_to': lines.location_dest_id.name,
                            'batch_no': lines.lot_ids.name,
                            'opening': lines.stock_on_hand_indent,
                            'inward': lines.quantity_done,
                            'balance': str(free_quel),
                            'price_rate': p_prd_unit_rate,
                            'rate_value': str(p_inv_tot_val),
                        })
