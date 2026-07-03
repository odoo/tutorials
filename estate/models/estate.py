from odoo import models, fields


class Estate(models.Model):
    _name = "estate"
    _description = "Real Estate Module"

    # fields
    name = fields.Char(required=True)
    description = fields.Text()
    date = fields.Datetime(readonly=True)

    garden_area = fields.Selection(string="Type", selection=[("e", "w")])
