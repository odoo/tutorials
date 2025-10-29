from odoo import models, fields, api


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    module_type_ids = fields.Many2many(
        'module.types',
        string="Available Module Types",
        related='product_tmpl_id.module_types',
        readonly=True
    )

    @api.onchange('product_tmpl_id')
    def _onchange_parent_product(self):
        if self.bom_line_ids:
            for line in self.bom_line_ids:
                line.module_types_id = False


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    module_types_id = fields.Many2one(
        'module.types',
        string="Module Type",
        domain="[('id', 'in', available_module_type_ids)] or []"
    )

    available_module_type_ids = fields.Many2many(
        'module.types',
        compute='_compute_available_module_type_ids',
        store=False
    )

    @api.depends('bom_id.product_tmpl_id')
    def _compute_available_module_type_ids(self):
        for line in self:
            if line.bom_id.product_tmpl_id:
                line.available_module_type_ids = line.bom_id.product_tmpl_id.module_types
            else:
                line.available_module_type_ids = False
