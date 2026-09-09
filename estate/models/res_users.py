from odoo import models, fields


class ResUsers(models.Model):
    # _name = "res.users123"
    _inherit = "res.users"

    # company_ids = fields.Many2many('res.company', 'res_company_users_rel1', 'user_id', 'cid',
    #     string='Companies')
    # group_ids = fields.Many2many('res.groups', 'res_groups_users_rel1', 'uid', 'gid', string='Groups', default=lambda s: s._default_groups(), help="Groups explicitly assigned to the user")

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        string="Real Estate Properties",
        domain=[("state", "in", ("new", "offer_received", "offer_accepted"))],
    )

    test = fields.Char()
