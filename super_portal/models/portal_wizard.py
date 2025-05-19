from odoo import api, fields, models


class PortalWizardUser(models.TransientModel):
    _inherit = 'portal.wizard.user'

    can_edit = fields.Boolean(compute='_compute_can_edit', string="Can Edit")

    #-------------------------------------------------------------------------------#
    # Compute [if the user can edit based on access rights]
    #-------------------------------------------------------------------------------#
    @api.depends('user_id', 'user_id.groups_id')
    def _compute_can_edit(self):

        for portal_wizard_user in self:
            user = portal_wizard_user.user_id
            if user.has_group('super_portal.group_edit_portal_access'):
                portal_wizard_user.can_edit = True
            else:
                portal_wizard_user.can_edit = False
