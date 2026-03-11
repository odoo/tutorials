from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyMaintenance(models.Model):
    _name = "estate.property.maintenance"
    _description = "Estate Property Maintenance"
    _rec_name = "title"

    title = fields.Char(required=True)
    created_by = fields.Many2one(
        "res.users",
        string="Created By",
        default=lambda self: self.env.user,
    )

    technision = fields.Many2one(
        "res.partner",
        string="Technision",
    )
    description = fields.Text()
    request_date = fields.Date(copy=False, default=lambda self: fields.Date.today())
    priority = fields.Selection(
        [
            ('low', "Low"),
            ('medium', "Medium"),
            ('high', "High"),
        ],
        copy=False,
        default="low",
    )
    estimate_cost = fields.Float()
    actual_cost = fields.Float()
    state = fields.Selection(
        [
            ('new', "New"),
            ('assign', "Assign"),
            ('progress', "Progress"),
            ('done', "Done"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )

    property_id = fields.Many2one("estate.property", string="Property")

    @api.onchange("technision")
    def _do_assign(self):
        if self.technision:
            self.state = "assign"

    def action_start(self):
        self.write({"state": "progress"})

    def action_stop(self):
        self.write({"state": "done"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    @api.constrains("state")
    def _check_estimated_price(self):
        for record in self:
            if record.state == "progress" and not record.estimate_cost:
                raise ValidationError("Enter Estimate Price !!")
