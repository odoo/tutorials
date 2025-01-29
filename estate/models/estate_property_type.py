from odoo import models, fields,api


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char('Property Type', required=True, translate=True)
    property_ids = fields.One2many(
        comodel_name="estate_property", 
        inverse_name="property_type_id", 
        string="Properties"
    )


      # One2many field linking to the estate_property_offer model
    offer_ids = fields.One2many(
        comodel_name='estate_property_offer',  # Target model
        inverse_name='property_type_id',       # Field in estate_property_offer that links back
        string='Offers'
    )

    sequence = fields.Integer(string='Sequence', default=10)  # Add the sequence field

    offer_count = fields.Integer('Offer Count', compute='_compute_offer_count')



    @api.depends('offer_ids')

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)








# Exercise

# Add a stat button to property type.

# Add the field property_type_id to estate_property_offer. We can define it as a related field on property_id.property_type_id and set it as stored.

# Thanks to this field, an offer will be linked to a property type when it’s created. You can add the field to the list view of offers to make sure it works.

# Add the field offer_ids to estate.property.type which is the One2many inverse of the field defined in the previous step.

# Add the field offer_count to estate.property.type. It is a computed field that counts the number of offers for a given property type (use offer_ids to do so).

# At this point, you have all the information necessary to know how many offers are linked to a property type. When in doubt, add offer_ids and offer_count directly to the view. The next step is to display the list when clicking on the stat button.

# Create a stat button on estate.property.type pointing to the estate_property_offer action. This means you should use the type="action" attribute (go back to the end of Chapter 9: Ready For Some Action? if you need a refresher).

# At this point, clicking on the stat button should display all offers. We still need to filter out the offers.

# On the estate_property_offer action, add a domain that defines property_type_id as equal to the active_id (= the current record, here is an example)