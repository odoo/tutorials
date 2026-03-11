from odoo import fields, models, api


class EstatePropertyVisit(models.Model):
    _name="estate.property.visit"
    _description="Property Visit"

    name = fields.Char(default="New Event")
    property_id = fields.Many2one(
        "estate.property",
        string="property",
        required=True
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="customer",
        required=True
    )
    visit_date = fields.Date(
        string="visit date",
        required=True
    )
    state = fields.Selection(
        [
            ('schedule', "schedule"),
            ('done', "done"),
            ('cancel', "cancel"),
        ],
    )

    @api.onchange('visit_date')
    def _onchange_visit_date(self):
        if self.visit_date:
            self.state = 'schedule'

    _check_date = models.Constraint(
            'UNIQUE(property_id, visit_date)',
            'another visit is already scheduled on this date',
        )
    