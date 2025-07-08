

# the tag model will be here



from odoo import fields, models



class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag model for the estate properties"
    name = fields.Char(required=True)
    color = fields.Integer(default=1)
    _sql_constraints = [('check_uniquness', ' UNIQUE(name)', 'Tag name must be unique')]

    # order on which data will be fetched
    _order = "name desc"
