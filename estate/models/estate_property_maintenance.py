from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyMaintenance(models.Model):
    _name = 'estate.property.maintenance'
    _description = "EstatePropertyMaintenance"

    name = fields.Char("Title")
    cost = fields.Integer()
    property_id = fields.Many2one(
        'estate.property', 'maintenance_id', required=True
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
        for record in self:
            if record.status == 'approved' and record.cost <= 0:
                raise UserError(
                    'Approved cost must be greater then 0'
                )
