from odoo import models, fields
from odoo import _


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = _("Real Estate Property")
    _order = "name, id"

    name = fields.Char(required=True, index=True, help=_("Name of the property"))
    expected_price = fields.Float(required=True, help=_("The price you expect the property to be sold for"))

