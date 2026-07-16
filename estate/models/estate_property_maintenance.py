from odoo import fields, models
from odoo.exceptions import UserError


class EstatePropertyMaintenance(models.Model):
    _name = "estate.property.maintenance"
    _description = "Property Maintenance"

    name = fields.Char(required=True, string="Title", translate=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    maintenance_type = fields.Selection(
        selection=[
            ('plumbing', "Plumbing"),
            ('electrical', "Electrical"),
            ('painting', "Painting"),
            ('other', "Other"),
        ],
        string="Type",
    )
    description = fields.Text(string="Description", translate=True)
    other_type = fields.Char(string="Other Details", translate=True)

    requester_id = fields.Many2one(
        "res.users",
        string="Requester",
        default=lambda self: self.env.user,
        required=True,
    )
    request_date = fields.Date(
        string="Request Date",
        default=fields.Date.today,
        required=True,
    )
    estimated_cost = fields.Float(string="Estimated Cost")
    technician_id = fields.Many2one("res.users", string="Technician")
    tentative_cost = fields.Float(string="Tentative Cost")
    final_cost = fields.Float(string="Final Cost")
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('assigned', "Assigned"),
            ('started', "Started"),
            ('done', "Done"),
        ],
        string="State",
        default="new",
        copy=False,
        required=True,
    )

    def action_assign(self):
        for record in self:
            if not record.technician_id:
                raise UserError("Please select a technician first.")
            record.state = "assigned"
        return True

    def action_start(self):
        for record in self:
            record.state = "started"
        return True

    def action_stop(self):
        for record in self:
            if record.final_cost <= 0:
                raise UserError("Please enter a valid final cost before completing the work.")
            record.state = "done"
        return True
