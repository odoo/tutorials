from odoo import api, fields, models


class PharmacyInteraction(models.Model):
    _name = "pharmacy.interaction"
    _description = "Drug Interaction"
    _rec_name = "display_name"

    medicine1_id = fields.Many2one('pharmacy.medicine', string="Medicine A", required=True)
    medicine2_id = fields.Many2one('pharmacy.medicine', string="Medicine B", required=True)
    severity = fields.Selection([
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ], string="Severity", required=True, default='moderate')
    warning_text = fields.Text(string="Warning Message", required=True)
    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('medicine1_id.name', 'medicine2_id.name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.medicine1_id.name} + {rec.medicine2_id.name}"
