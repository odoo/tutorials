from odoo import fields, models
from odoo.exceptions import UserError


class EstatePropertyMaintenance(models.Model):
    _name = "estate.property.maintenance"
    _description = "The Property Maintenance"

    issue = fields.Char(required=True)
    status = fields.Selection(
        selection=[
            ("report", "Report"),
            ("inprogress", "Inprogress"),
            ("done", "Done"),
        ],
        default="report",
        readonly=True,
        copy=False,
    )

    agent_ids = fields.Many2one(
        "res.users", string="Agent", default=lambda self: self.env.user
    )
    price = fields.Float()
    create_date = fields.Date()
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")

    _check_positive_price = models.Constraint(
        "CHECK(price >= 0)",
        "The Price Should be Positive",
    )

    def action_in_progress(self):
        for record in self:
            if record.agent_ids and self.env.user != record.agent_ids:
                raise UserError(
                    self.env._("Only assigned agent can change status to In Progress.")
                )
            record.status = "inprogress"

    def action_done(self):
        for record in self:
            if record.agent_ids and self.env.user != record.agent_ids:
                raise UserError(
                    self.env._("Only assigned agent can change status to Done.")
                )
            if record.price <= 0:
                raise UserError(
                    self.env._("Please enter the price before marking as Done.")
                )
            record.status = "done"
