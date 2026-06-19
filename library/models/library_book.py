from odoo import api, fields, models


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = "Library Management"

    name = fields.Char(required=True)
    author = fields.Many2one('res.partner')
    total_copies = fields.Integer()
    available_copies = fields.Integer(compute='_compute_available_copies')
    state = fields.Selection(
        selection=[
            ('available', "Available"),
            ('out_of_stock', "Out of Stock")
        ],
        default='available'
    )
    active_borrow_count = fields.Integer(compute='_compute_borrow_count')
    borrow_ids = fields.One2many('library.borrow', 'book_id')
    popularity = fields.Selection(
        selection=[
            ('low', "Low"),
            ('medium', "Medium"),
            ('high', "High"),
        ],
        compute="_compute_popularity",
        store=True
    )

    @api.depends('borrow_ids')
    def _compute_borrow_count(self):
        for rec in self:
            rec.active_borrow_count = len(rec.borrow_ids.filtered(lambda r: r.state != 'returned'))

    @api.depends('total_copies', 'active_borrow_count')
    def _compute_available_copies(self):
        for rec in self:
            if rec.total_copies > 0:
                rec.available_copies = rec.total_copies - rec.active_borrow_count
            else:
                rec.available_copies = 0

    @api.depends('active_borrow_count')
    def _compute_popularity(self):
        for rec in self:
            if rec.active_borrow_count < 5:
                rec.popularity = 'low'
            elif rec.active_borrow_count < 20:
                rec.popularity = 'medium'
            elif rec.active_borrow_count >= 20:
                rec.popularity = 'high'

    @api.onchange('available_copies')
    def _onchange_available_copies(self):
        if self.available_copies == 0:
            self.state = 'out_of_stock'
