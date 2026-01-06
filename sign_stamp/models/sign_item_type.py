from odoo import api, fields, models


class SignItemType(models.Model):
    _inherit = "sign.item.type"
    _order = "sequence"

    sequence = fields.Integer(string="Sequence", default=1)
    display_name = fields.Char(compute="_compute_display_name")

    @api.depends_context('company')
    def _compute_display_name(self):
        self.display_name = self.env.company.name
        for record in self:
            if record.item_type == "stamp" and record.sequence == 0:
                record.name = record.display_name
                break
