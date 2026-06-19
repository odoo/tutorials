from odoo import api, fields, models


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Members'

    name = fields.Char(required=True)
    email = fields.Char()
    borrow_ids = fields.One2many('library.borrow', 'member_id')
    active_borrow_count = fields.Integer(compute='_compute_borrow_count')
    is_eligible = fields.Boolean(compute='_compute_is_eligible')
    total_fine_amount = fields.Integer(compute='_compute_total_fine', store=True)

    @api.depends('borrow_ids')
    def _compute_borrow_count(self):
        for rec in self:
            rec.active_borrow_count = len(rec.borrow_ids.filtered(lambda r: r.state != 'returned'))

    @api.depends('active_borrow_count')
    def _compute_is_eligible(self):
        for rec in self:
            rec.is_eligible = True if rec.active_borrow_count <= 3 else False

    @api.depends('borrow_ids.fine_amount')
    def _compute_total_fine(self):
        for rec in self:
            rec.total_fine_amount = sum(rec.borrow_ids.mapped('fine_amount'))
