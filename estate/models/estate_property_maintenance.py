from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero

class EstatePropertyMaintenance(models.Model):
    _name = 'estate.property.maintenance'
    _description = 'Estate Property maintenance'

    title = fields.Char(required=True)
    cost = fields.Float(string="Cost")
    status = fields.Selection(
        [
            ('new', "New"),
            ('approved', "Approved"),
            ('done', "Done"),
            ('cancle', "Cancle")
        ],
        required=True,
        default="new",
    )

    property_id = fields.Many2one('estate.property', required=True)

    def maintenance_accept(self):
        for maintenance in self:
            if float_is_zero(maintenance.cost, precision_digits=2):
                raise UserError("Maintenance cost must be greater than zero")

            maintenance.status = "approved"
        return True

    def maintenance_refuse(self):
        for maintenance in self:
            maintenance.status = "cancle"
        return True
