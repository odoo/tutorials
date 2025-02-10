from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property, such as home, apartment, row house"
    _order = "name asc"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many('estate.property','property_type_id',string="Properties")
    offer_ids = fields.One2many("estate.property.offer","property_type_id",string="Offers")
    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count"
    )

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'Property type names must be unique.')
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        self.offer_count = len(self.offer_ids)

