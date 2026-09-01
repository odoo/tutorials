from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EstateVisit(models.Model):
    _name = "estate.visit"
    _description = "Property Visit"
    _order = "date_time desc"

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    customer_id = fields.Many2one("res.partner", string="Customer", required=True)
    agent_id = fields.Many2one(
        "res.users",
        string="Agent",
        required=True,
        default=lambda self: self.env.user,
    )
    date_time = fields.Datetime(string="Time Slot", required=True)

    @api.onchange("property_id")
    def _onchange_property_id(self):
        if self.property_id and self.property_id.salesperson_id:
            self.agent_id = self.property_id.salesperson_id

    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('scheduled', "Scheduled"),
            ('completed', "Completed"),
            ('cancelled', "Cancelled"),
        ],
        string="Status",
        default="scheduled",
        required=True,
    )
    rating = fields.Selection(
        selection=[
            ("1", "Poor"),
            ("2", "Fair"),
            ("3", "Good"),
            ("4", "Very Good"),
            ("5", "Excellent"),
        ],
        string="Rating",
    )
    feedback = fields.Text(string="Feedback")

    _check_unique_property_slot = models.Constraint(
        "UNIQUE(property_id, date_time)",
        "A time slot is already booked for this property for the same time.",
    )

    @api.constrains("property_id", "customer_id", "date_time")
    def _check_duplicate_customer_visit(self):
        for record in self:
            domain = [
                ("id", "!=", record.id),
                ("property_id", "=", record.property_id.id),
                ("customer_id", "=", record.customer_id.id),
                ("date_time", "=", record.date_time),
            ]
            if record.search_count(domain) > 0:
                raise ValidationError(
                    _("This customer already has a visit scheduled for this property at this time."),
                )
