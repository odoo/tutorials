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
    priority = fields.Selection(
        selection=[
            ('0', "test"),
            ('1', 'Low'),
            ('2', "Medium"),
            ('3', "High"),
        ],
        default="1",
        string="Priority",
    )
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
        self.ensure_one()
        if not self.technician_id:
            msg = "Please select a technician first."
            raise UserError(msg)
        self.state = "assigned"
        return True

    def action_start(self):
        self.ensure_one()
        self.state = "started"
        return True

    def action_stop(self):
        self.ensure_one()
        if self.final_cost <= 0:
            msg = "Please enter a valid final cost before completing the work."
            raise UserError(msg)
        self.state = "done"
        return True
