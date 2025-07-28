from odoo import api, models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    modular_type_id = fields.Many2one(
        'modular.type.config',
        string="Module Type",
        readonly=True
    )


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model_create_multi
    def create(self, vals_list):
        custom_values_map = {}
        for i, vals in enumerate(vals_list):
            if 'custom_modular_values' in vals:
                custom_values_map[i] = vals.pop('custom_modular_values')

        mos = super().create(vals_list)

        for i, mo in enumerate(mos):
            custom_values = custom_values_map.get(i)
            if custom_values and mo.move_raw_ids:
                for custom_val in custom_values:
                    move_to_update = mo.move_raw_ids.filtered(
                        lambda m: m.product_id.id == custom_val['component_product_id']
                    )
                    if move_to_update:
                        move_to_update.write({
                            'product_uom_qty': custom_val['quantity'],
                            'modular_type_id': custom_val['modular_type_id'],
                        })
        return mos
