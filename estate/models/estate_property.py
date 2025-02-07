from odoo import models,fields

class EstateProperty(models.Model):
    _name="estate.property"
    _description="Real Estate Property"

    name=fields.Char(required = True)
    description=fields.Text()
    postcode=fields.Char()
    date_availability=fields.Date(copy=False,
                                    default=fields.Date().add(fields.Date().today(),days = 90))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly = True,
                               copy = False)
    bedrooms=fields.Integer(default = 2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection(
                        selection=[('north','North'),('south','South'),('east','East'),('west','West')])
    active=fields.Boolean("Active",default = True)
    status=fields.Selection(
                        selection=[('new','New'),
                                   ("offer_received","Offer Received"),
                                   ("offer_accepted","Offer Accepted"),
                                   ("sold","Sold"),("canceled","Canceled")],
                        default='new',
                        copy=False)
