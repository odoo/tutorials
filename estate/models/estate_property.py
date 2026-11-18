from odoo import fields,models


class EstateProperty(models.Model):
    _name  ="estate_property"
    _description = "ESTATE property"
    #_order  ="sequence"

    currency_id = fields.Many2one(
        'res.currency',
        string = 'Currency',
        default = lambda self:self.env.company.currency_id, required = True)
    name = fields.Char('Name', required=True)
    property_type = fields.Text('Type', required=True)
    postcode = fields.Char()
    date_availability = fields.Datetime(copy=False)
    expected_price =  fields.Monetary(currency_field='currency_id',copy=False, required=True, default=0.0)
    selling_price = fields.Monetary(currency_field='currency_id',readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garden_orientation = fields.Selection([('N','N'),('S','S'),('W','W'),('E','E')])
    active = fields.Boolean(default=True)
    Status = fields.Selection([("0", "New"),("1", "offer received"), ("2", "Sold"), ('3','Sold'), ('4','Cancelled')], default='0', required=True)
