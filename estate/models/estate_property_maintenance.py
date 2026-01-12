from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class EstatePropertyMaintenanceRequest(models.Model):
    _name = 'estate.property.maintenance'
    _description = "this is property maintenance model"

    title = fields.Char("Title", required=True, default="Unknown")
    cost = fields.Float('Price')
    status = fields.Selection(
        [
            ('new', "New"),
            ('approved', "Approved"),
            ('Done', "Done"),
        ],
        default='new',
    )

    property_id = fields.Many2one('estate.property', required=True)

    # _check_cost = models.Constraint(
    #    'CHECK(cost > 0)', "The expected cost must be Strictly positive"
    # )

    @api.constrains('status')
    def _check_cost(self):
        for record in self:
            if record.status == 'approved' and record.cost <= 0:
                raise ValidationError(
                    "The Cost must be Positive"
                )

    def action_approved(self):
        self.status = 'Done'
    