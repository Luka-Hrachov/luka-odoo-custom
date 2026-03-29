from odoo import fields, models, api


class GoogleSheet(models.Model):
    _name = 'google.sheet'
    _description = 'Google Sheet Import'

    name = fields.Char(required=True)
    user_id = fields.Many2one(
        'res.users',
        string='Responsible',
        default=lambda self: self.env.user,
        copy=False
    )
    external_sheet_id = fields.Char(required=True, copy=False)
    line_ids = fields.One2many(
        comodel_name='google.sheet.line',
        inverse_name='sheet_id',
        string='Fields',
        copy=True,
    )
    ignore_empty_columns = fields.Boolean(default=False)
    report_email = fields.Char(string='Report Email')
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('importing', 'Importing'),
        ('done', 'Done')
    ], default='new', required=True, copy=False, string='Status')
    tag_ids = fields.Many2many('google.sheet.tag', string='Tags')
    line_count = fields.Integer(compute='_compute_line_count')

    @api.depends('line_ids')
    def _compute_line_count(self):
        for record in self:
            record.line_count = len(record.line_ids)


class Google(models.Model):
    _name = 'google.sheet.tag'
    _description = 'Google Sheet Tag'

    name = fields.Char(required=True)
    color = fields.Integer(string='Color')