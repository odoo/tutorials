from odoo import fields, models, api
from odoo.exceptions import UserError


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
            if maintenance.cost <= 0.00:
                raise UserError("Maintenance cost must be greater than zero")

            maintenance.status = "approved"
        return True

    def maintenance_refuse(self):
        for maintenance in self:
            maintenance.status = "cancle"
        return True
