from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    is_modular_bom = fields.Boolean(
        readonly=True, compute='_compute_is_modular_bom', store=True
    )

    def _compute_is_modular_bom(self):
        for production in self:
            if (
                production.bom_id
                and production.bom_id.product_tmpl_id
                and production.bom_id.product_tmpl_id.modular_type_ids
            ):
                production.is_modular_bom = True
            else:
                production.is_modular_bom = False
        return True
