from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate App"
    name = fields.Char()
    description

postcode

date_availability

expected_price

selling_price

bedrooms

living_area

facades

garage

garden

garden_area

garden_orientation
    # _order = "sequence"

    # name = fields.Char('Plan Name', required=True, translate=True)
    # number_of_months = fields.Integer('# Months', required=True)
    # active = fields.Boolean('Active', default=True)
    # sequence = fields.Integer('Sequence', default=10)

    # _sql_constraints = [
    #     ('check_number_of_months', 'CHECK(number_of_months >= 0)', 'The number of month can\'t be negative.'),
    # ]