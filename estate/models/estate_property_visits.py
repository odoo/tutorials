from odoo import _, fields, models, api
from odoo.exceptions import ValidationError


class EstatePropertyVisits(models.Model):
    _name = "estate.property.visits"
    _description = "Real Estate Visits"
    _order = "create_date desc"

    property_id = fields.Many2one("estate.property", string="Property", required=True, copy=True)
    agent = fields.Many2one("res.users", string="agents", related="property_id.salesperson_id", store=True, readonly=True)
    customer = fields.Many2one("res.partner", string="Customer", copy=True, required=True)
    visit_date = fields.Date(string="Date of visit", required=True)
    status_of_visit = fields.Selection(
        selection=[
            ('scheduled', "Scheduled"),
            ('done', "Done"),
            ('cancelled', "Cancelled"),
        ],
        string="Status Of the Visit",
        default='scheduled',
    )
    rating = fields.Selection(
        selection=[
            ('0', "_"),
            ('1', "*"),
            ('2', "**"),
            ('3', "***"),
            ('4', "****"),
            ('5', "*****"),
        ], string="Rating", index=True)
    time_slot = fields.Selection(
        selection=[
            ('9-10', "9 am - 10 am"),
            ('10-11', "10 am - 11 am"),
            ('11-12', "11 am - 12 am"),
            ('12-1', "12 noon - 1 pm"),
            ('1-2', "1 pm - 2 pm"),
            ('2-3', "2 pm - 3 pm"),
            ('3-4', "3 pm - 4 pm"),
            ('4-5', "4 pm - 5 pm"),
            ('5-6', "5 pm - 6 pm"),
        ], string="Time Of Visit",
        required=True,
    )

    @api.constrains("visit_date", "property_id")
    def _check_no_overlap(self):
        for visit in self:
            overlapping = self.search([
                ('property_id', '=', visit.property_id.id),
                ('visit_date', '=', visit.visit_date),
                ('time_slot', '=', visit.time_slot),
                ("id", '!=', visit.id),
            ])
            if overlapping:
                raise ValidationError(_("more than 1 visit cannot happen at the same time"))

    @api.constrains("customer_id", "property_id")
    def _check_unique_visit(self):
        for visit in self:
            existing = self.search([
                ('customer', '=', visit.customer.id),
                ('property_id', '=', visit.property_id.id),
                ("id", '!=', visit.id),
            ])
            if existing:
                raise ValidationError(_("the customer has already visited the property"))

    @api.onchange("propert_id")
    def _onchange_property_id(self):
        if self.property_id:
            self.agent == self.property_id.user_id

    def _compute_display_name(self):
        for record in self:
            record.display_name = "new"

    # def action_send_reminder(self):
    #     for record in self:
    #         if record.status_of_visit == 'scheduled':
    #             if record.visit_date >= fields.Datetime.now() and record.visit_date <= fields.Datetime.now() + timedelta(hours=24):
