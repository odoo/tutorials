from odoo import fields, models

class homePlan(models.Model):
    _name = "home.plan"
    _description = "this is home plan"
    
    name = fields.Char('Plan Name', required=True)
    description = fields.Char('Description')
    postcode = fields.Char('Post code', required=True)
    date_availability = fields.Datetime('available till', readonly=True)
    number_of_months = fields.Integer('# Months', required=True)
    expected_price = fields.Float('Price', required=True)
    Garage = fields.Boolean('Active', default=True)

    orientation_direction = fields.Selection(
        [('North','north'),
        ('East','east'),
        ('West','west'),
        ('South','south')
        ]
    )


    # _sql_constraints = [
    #     ('check_number_of_months', 'CHECK(number_of_months >= 0)', 'The number of month can\'t be negative.'),
    # ]
