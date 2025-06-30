from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name asc"

    name = fields.Char("Name", required=True)
    property_ids = fields.Many2one(
        comodel_name="estate.property",
        string="Properties",
        help="Properties of this type"
        )

    sequence = fields.Integer(
        string="Sequence",      
        default=10,
        help="Used to order the property types in the user interface",  
    )

    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",   
        inverse_name="property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(
        string="Offer Count",       
        compute="_compute_offer_count",
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)

    def action_view_offers(self):
        res = self.env.ref("estate.estate_property_offer_action").read()[0]
        res["domain"] = [("id", "in", self.offer_ids.ids)]
        return res