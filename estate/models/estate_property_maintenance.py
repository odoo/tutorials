from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero


class EstatePropertyMaintenance(models.Model):
    _name = 'estate.property.maintenance'
    _description = 'Estate Property maintenance'

    title = fields.Char(required=True)
    cost = fields.Float()
    status = fields.Selection(
        [
            ('new', "New"),
            ('approved', "Approved"),
            ('done', "Done"),
            ('cancel', "Cancel")
        ],
        required=True,
        default="new",
    )

    property_id = fields.Many2one('estate.property', required=True)

    def action_accept_maintenance(self):
        for maintenance in self:
            if float_is_zero(maintenance.cost, precision_digits=2):
                raise UserError("Maintenance cost must be greater than zero")

            maintenance.status = "approved"
        return True

    def action_refuse_maintenance(self):
        for maintenance in self:
            maintenance.status = "cancel"
        return True
