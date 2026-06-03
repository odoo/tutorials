from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_second_uom_id = fields.Many2one(
        'uom.uom',
        string="POS Second Unit of Measure"
    )
    pos_second_uom_domain_ids = fields.Many2many('uom.uom', compute="_compute_pos_second_uom_domain_ids", string="All Pos Second Uom")

    @api.depends("uom_id")
    def _compute_pos_second_uom_domain_ids(self):
        for rec in self:
            if not rec.uom_id:
                rec.pos_second_uom_domain_ids = self.env['uom.uom'].search([])
                continue

            root_uom = rec.uom_id
            while root_uom.relative_uom_id:
                root_uom = root_uom.relative_uom_id

            compatible_uoms = self.env['uom.uom'].search([
                '|', ('id', '=', root_uom.id), ('parent_path', 'like', f'%{root_uom.id}%')
            ])

            rec.pos_second_uom_domain_ids = compatible_uoms

    @api.constrains('pos_second_uom_id', 'uom_id')
    def _check_uom_compatibility(self):
        for record in self:
            if record.pos_second_uom_id and record.uom_id:
                root_main = record.uom_id
                while root_main.relative_uom_id:
                    root_main = root_main.relative_uom_id

                root_second = record.pos_second_uom_id
                while root_second.relative_uom_id:
                    root_second = root_second.relative_uom_id

                if root_main.id != root_second.id:
                    raise ValidationError(_("Selected Second UoM must be from the same unit hierarchy family!"))
