from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property's type"
    
    # Order attributes
    _order = "sequence, name"

    name = fields.Char(required=True,)

    sequence = fields.Integer(string="Sequence", default=1, help="Used to order stages. Lower is better.",)

    # Relations
    property_ids = fields.One2many(
        "estate.property", 
        "property_type_id", 
        string="Properties",
    )

    offer_ids = fields.One2many(
        "estate.property.offer", 
        "property_type_id", 
        string="Offers",
    )

    # -------------------------------------------------------------------------
    # COMPUTED FIELDS
    # -------------------------------------------------------------------------
    offer_count = fields.Integer(
        string="Offers Count", 
        compute="_compute_offer_count",
    )


    # -------------------------------------------------------------------------
    # CONSTRAINTS
    # -------------------------------------------------------------------------
    _unique_type_name = models.Constraint(
        'UNIQUE(name)', 
        'A property type name must be unique.',
    )


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
