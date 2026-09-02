from datetime import datetime

from odoo import fields, models


class TestModel(models.Model):
    today = datetime.now()

    month = today.month + 3
    year = today.year
    day = today.day

    if month > 12:
        year = year + 1
        month = month % 12

    three_month_date = today.replace(year=year, month=month, day=day)

    _name = "estate.property"
    _description = "This is a dummy table"

    name = fields.Char(translate=True, default="Unknown", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=three_month_date.date())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Direction",
        default="north",
    )
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property_type")

    def action_confirm(self):
        return {
            "type": "ir.actions.act_window",  # type and name are very important
            "name": "Properties",
            "res_model": "estate.property",
            "view_mode": "form",
            "target": "current",
        }
