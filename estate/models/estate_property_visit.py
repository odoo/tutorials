from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyVisit(models.Model):
    _name = "estate.property.visit"
    _description = "Estate Property Visit"

    name = fields.Char(required=True)
    customer_id = fields.Many2one(
        "res.partner", string="Customer", copy=False, required=True
    )
    state = fields.Selection(
        [
            ('schedule', "schedule"),
            ('done', "Done"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default="schedule",
    )
    date_availability = fields.Date(copy=False, required=True, string="Visit Date")
    property_id = fields.Many2one("estate.property", string="Property", readonly=True)

    @api.constrains("date_availability")
    def _check_selling_price(self):
        for record in self:
            all_mettings = record.property_id.visit_req.filtered(
                lambda o: o.id != record.id
            )
            for req in all_mettings:
                if record.date_availability == req.date_availability:
                    raise ValidationError("At this date alraedy visit is schedule !!")

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            date_availability = vals.get("date_availability")

            if date_availability:
                start_date = fields.Date.from_string(date_availability)
                stop_date = start_date

                self.env["calendar.event"].create(
                    {
                        "name": vals.get("name"),
                        "start": start_date,
                        "stop": stop_date,
                    }
                )

        return super().create(vals_list)
