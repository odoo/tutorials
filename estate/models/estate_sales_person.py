from odoo import fields, models
from odoo.tools.float_utils import float_compare

class EstateSalesPerson(models.Model):
    _inherit= "res.users"
    property_ids = fields.One2many(comodel_name= "estate.property", inverse_name= "sales_person_id")