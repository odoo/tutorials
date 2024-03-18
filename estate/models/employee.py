from odoo import fields, models


class EmployeeModel(models.Model):
    _inherit = "hr.employee"

    property_ids = fields.One2many(
        "estate.property", "salesperson_id",
        string="Assigned Properties",
        domain=[("state", "in", ("new", "offer_received"))],
    )
