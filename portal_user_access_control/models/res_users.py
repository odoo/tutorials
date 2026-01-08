from odoo import api, fields, models, SUPERUSER_ID


class ResUsers(models.Model):
    _inherit = 'res.users'

    portal_access_so = fields.Boolean(default=True, store=True)
    portal_access_quotes = fields.Boolean(default=True, store=True)
    portal_access_rfq = fields.Boolean(default=True, store=True)
    portal_access_po = fields.Boolean(default=True, store=True)
    portal_access_invoices = fields.Boolean(default=True, store=True)
    portal_access_projects = fields.Boolean(default=True, store=True)
    portal_access_tasks = fields.Boolean(default=True, store=True)
    is_portal_user = fields.Boolean(string="Is Portal User", compute="_compute_is_portal_user")

    @api.depends("groups_id")
    def _compute_is_portal_user(self):
        portal_group = self.env.ref("base.group_portal")
        for user in self:
            user.is_portal_user = portal_group in user.groups_id

    def update_portal_access_groups(self):
        portal_group = self.env.ref("base.group_portal")
        if not portal_group:
            return

        groups_map = {
            'portal_access_so': 'portal_user_access_control.sales_order_group',
            'portal_access_quotes': 'portal_user_access_control.quotetion',
            'portal_access_rfq': 'portal_user_access_control.rfq',
            'portal_access_po': 'portal_user_access_control.purchase_order',
            'portal_access_invoices': 'portal_user_access_control.invoices',
            'portal_access_projects': 'portal_user_access_control.projects',
            'portal_access_tasks': 'portal_user_access_control.tasks',
        }

        for user in self:
            if portal_group not in user.groups_id:
                continue

            for field, group_xml in groups_map.items():
                group = self.env.ref(group_xml)
                if group:
                    if getattr(user, field):
                        group.write({'users': [(4, user.id)]})
                    else:
                        group.write({'users': [(3, user.id)]})

    def write(self, vals):
        res = super().write(vals)
        if any(field in vals for field in [
            'portal_access_so', 'portal_access_quotes', 'portal_access_rfq', 'portal_access_po', 'portal_access_invoices', 'portal_access_projects', 'portal_access_tasks'
        ]):
            self.update_portal_access_groups()
        return res

    def _register_hook(self):
        res = super()._register_hook()
        env = api.Environment(self._cr, SUPERUSER_ID, {})
        default_user = env['res.users'].search([('login', '=', 'portal')], limit=1)
        if default_user:
            default_user.update_portal_access_groups()
        return res
