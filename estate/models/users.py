from odoo import api,fields, models,exceptions
from datetime import date, timedelta

class EstateUsers(models.Model):
    _inherit = 'res.users'
    property_ids=fields.One2many("estate.property","salesperson_id")
