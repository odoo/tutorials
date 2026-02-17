from odoo import api, fields, models


class InheritedProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_second_uom_id = fields.Many2one(
        'uom.uom',
        string="POS Second UoM",
        help="Secondary unit of measure for quick quantity conversion in the POS popup.",
    )
    uom_root_id = fields.Many2one(
        'uom.uom', string="UoM Root", compute='_compute_uom_root_id'
    )

    @api.depends('uom_id')
    def _compute_uom_root_id(self):
        for record in self:
            if record.uom_id and record.uom_id.parent_path:
                root_id = int(record.uom_id.parent_path.split('/')[0])
                record.uom_root_id = root_id
            else:
                record.uom_root_id = False

    @api.onchange('uom_id')
    def _onchange_uom_id_clear_second(self):
        if self.pos_second_uom_id and not self.uom_id._has_common_reference(
            self.pos_second_uom_id
        ):
            self.pos_second_uom_id = False
