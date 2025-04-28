from odoo import api, fields, models


class EstatePropertyType(models.Model):
    # ------------------
    # Private attributes
    # ------------------

    _name = "estate.property.type"
    _description = "This class allows to choose what kind of property is."
    _order = "sequence, name"

    # ------------------
    # Field declarations
    # ------------------

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)
    offer_count = fields.Integer(compute="_compute_offer_count")

    # One2Many relationships
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')

    # ---------------
    # Compute methods
    # ---------------

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
