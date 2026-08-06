from odoo import fields, models


class TestModel(models.Model):
    _name = "estate.property"
    _description = "This is a dummy table"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
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
    active = fields.Boolean("active", default=True)

    def action_confirm(self):
        print("button is clicked")
        return {
            "type": "ir.actions.act_window",
            "name": "Properties",
            "res_model": "estate.property",
            "view_mode": "form",
            "target": "current",
        }
