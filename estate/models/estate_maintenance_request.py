from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyMaintenanceRequest(models.Model):
    _name = 'estate.property.maintenance.request'
    _description = "estate property maintenance"

    cost = fields.Float()
    tital = fields.Char()
    status = fields.Selection(
        [('new', "New"), ('approved', "Approved"), ('done', "Done")], copy=False
    )
    property_id = fields.Many2one('estate.property', required=True)
    _chek_cost = models.Constraint(
        "CHECK(cost >= 0)", "cost of property should be positive"
    )

    @api.constrains('cost', 'status')
    def _check_cost(self):
        for record in self:
            if record.status == 'approved' and not record.cost > 0:
                raise ValidationError("cost should be grater than 0.")
