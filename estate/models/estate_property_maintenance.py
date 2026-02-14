from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyMaintenance(models.Model):
    _name = 'estate.property.maintenance'
    _description = "EstatePropertyMaintenance"

    name = fields.Char("Title")
    cost = fields.Integer()
    property_id = fields.Many2one(
        'estate.property', required=True
    )
    status = fields.Selection(
        default='new',
        selection=[
            ('new', "New"),
            ('approved', "Approved"),
            ('done', "Done")
        ]
    )

    @api.constrains('cost', 'status')
    def _check_cost(self):
        invalid_records = self.filtered(
            lambda r: r.status == 'approved' and r.cost <= 0
        )
        if invalid_records:
            raise UserError('Approved cost must be greater than 0')
