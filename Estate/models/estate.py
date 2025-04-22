
from odoo import fields, models
class Estate(models.Model):
    _name="estate"
    _description="Estate"
    name=fields.Char()
    description=fields.Text()
    postcode=fields.Char()
    date_availability=fields.Date()
    expected_price=fields.Float()
    selling_price=fields.Float()
    bedrooms=fields.Integer()
