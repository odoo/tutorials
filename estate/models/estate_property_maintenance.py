from odoo import _, fields, models
from odoo.exceptions import UserError


class EstatePropertyMaintenance(models.Model):
    _name = "estate.property.maintenance"
    _description = "Property Maintenance"
    _order = "id desc"

    name = fields.Char(string="Title", required=True, translate=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    maintenance_type = fields.Selection(
        string="Type",
        selection=[
            ('plumbing', "Plumbing"),
            ('electrical', "Electrical"),
            ('painting', "Painting"),
            ('other', "Other"),
        ],
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
        string="Priority",
        selection=[
            ('0', "Low"),
            ('1', "Medium"),
            ('2', "High"),
            ('3', "Very High"),
        ],
        default="0",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('assigned', "Assigned"),
            ('started', "Started"),
            ('done', "Done"),
        ],
        default="new",
        copy=False,
        required=True,
    )

    def action_assign(self):
        self.ensure_one()
        if not self.technician_id:
            raise UserError(_("Please select a technician first."))
        self.state = "assigned"
        return True

    def action_start(self):
        self.ensure_one()
        self.state = "started"
        return True

    def action_stop(self):
        self.ensure_one()
        if self.final_cost <= 0:
            raise UserError(_("Please enter a valid final cost before completing the work."))
        self.state = "done"
        return True
