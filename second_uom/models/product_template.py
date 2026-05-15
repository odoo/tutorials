from odoo import api, fields, models


class InheritedProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_second_uom_id = fields.Many2one('uom.uom', string="POS Second UoM")
    pos_uom_reference_id = fields.Many2one(
        'uom.uom', string="UoM Root", compute='_compute_pos_uom_reference_id', store=True
    )

    @api.depends('uom_id')
    def _compute_pos_uom_reference_id(self):
        for record in self:
            if record.uom_id:
                record.pos_uom_reference_id = (
                    record.uom_id.relative_uom_id or record.uom_id
                )
            else:
                record.pos_uom_reference_id = False

    @api.onchange('uom_id')
    def _onchange_uom_id_clear_second(self):
        if self.pos_second_uom_id:
            second_ref = self.pos_second_uom_id.relative_uom_id or self.pos_second_uom_id
            main_ref = self.uom_id.relative_uom_id or self.uom_id
            if second_ref != main_ref:
                self.pos_second_uom_id = False
