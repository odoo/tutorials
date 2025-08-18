from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    
    modular_type_id = fields.Many2one(
        comodel_name="modular.types",
        string="Modular Type",
        domain="[('id', 'in', available_modular_type_ids)]"
    )

    available_modular_type_ids = fields.Many2many(
        comodel_name="modular.types",
        compute="_compute_available_modular_types",
        store=False
    )

    @api.depends('bom_id.product_tmpl_id')
    def _compute_available_modular_types(self):
        processed_boms = {}

        for line in self:
            bom = line.bom_id
            if bom in processed_boms:
                line.available_modular_type_ids = processed_boms[bom]
            else:
                modular_types = bom.product_tmpl_id.modular_type_ids.ids if bom.product_tmpl_id else []
                processed_boms[bom] = modular_types
                line.available_modular_type_ids = modular_types
