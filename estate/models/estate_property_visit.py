from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyVisit(models.Model):
    _name = 'estate.property.visit'
    _description = "Real Estate Property Visit"

    customer_id = fields.Many2one(
        'res.partner',
        string="Customer",
        copy=False,
    )
    date_visit = fields.Datetime(
        string="Visit Date",
        required=True,
    )
    property_id = fields.Many2one(
        'estate.property',
        required=True,
    )
    status = fields.Selection(
        [
            ('new', "New"),
            ('visiting', "Visiting"),
            ('visit_completed', "Visit Completed"),
        ],
        required=True,
        copy=False,
        default='new',
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string="Salesperson",
    )

    @api.constrains('property_id', 'date_visit')
    def _check_duplicate_visit(self):
        for record in self:
            duplicate = self.search([
                ('id', '!=', record.id),
                ('property_id', '=', record.property_id.id),
                ('date_visit', '=', record.date_visit),
            ], limit=1)

            if duplicate:
                raise ValidationError(
                    "This property is already booked for the selected date and time."
                )

    @api.onchange('property_id')
    def _onchange_salesp(self):
        if self.property_id:
            self.salesperson_id = self.property_id.salesperson_id

    def action_start_visit(self):
        self.ensure_one()
        if self.status != 'new':
            raise UserError("Visit can only be started from New status.")

        self.status = 'visiting'
        self.date_visit = fields.Datetime.now()

    def action_complete_visit(self):
        self.ensure_one()
        if self.status != 'visiting':
            raise UserError("You can only complete a visit that is in progress.")

        self.status = 'visit_completed'
