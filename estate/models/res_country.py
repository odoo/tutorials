from odoo import fields, models

class CountryState(models.Model):
    _name = 'res.country.state'
    _description = 'Country State'
    _order = 'code'

    country_id = fields.many2one ('res.country', string='Country', required=True)
    name = fields.Char(string='State Name', required=True,
               help='Administrative divisions of a country. E.g. Fed. State, Departement, Canton')
    code = fields.Char(string='State Code', help='The state code.', required=True)

