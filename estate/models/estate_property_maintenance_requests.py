from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyMaintenanceRequests(models.Model):
    _name = 'estate.property.maintenance.requests'
    _description = 'Estate Property Maintenance Requests'

    title = fields.Char()
    cost = fields.Float()
    status = fields.Selection(
        default='new',
        copy=False,
        selection=[('new', "New"), ('approved', "Approved"), ('done', "Done")],
    )
    property_id = fields.Many2one('estate.property', required=True)

    @api.constrains('status', 'cost')
    def _check_cost(self):
        if self.status == 'approved' and self.cost <= 0:
            raise ValidationError(
                "The cost must be greater than zero.")
