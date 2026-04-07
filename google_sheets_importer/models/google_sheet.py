from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.models import Model


class GoogleSheet(models.Model):
    _name = 'google.sheet'
    _description = 'Google Sheet Import'
    _sql_constraints = [
        ('unique_sheet', 'UNIQUE(external_sheet_id, sheet_name)', 'The sheet id and name must be unique')
    ]
    _order = 'id desc'

    name = fields.Char(required=True)
    sheet_name = fields.Char(required=True)
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
    max_sequence = fields.Integer(compute='_compute_max_sequence', inverse='_inverse_max_sequence')

    @api.depends('line_ids')
    def _compute_line_count(self):
        for record in self:
            record.line_count = len(record.line_ids)

    @api.depends('line_ids.sequence')
    def _compute_max_sequence(self):
        for record in self:
            record.max_sequence = max(record.line_ids.mapped('sequence'), default=0)

    def _inverse_max_sequence(self):
        for record in self:
            for line in record.line_ids:
                line.sequence = min(line.sequence, record.max_sequence)

    def action_start_import(self):
        for record in self:
            if not record.line_ids:
                raise UserError('Cannot start import, no lines specified')

            record.state = 'importing'
        return True

    def action_set_done(self):
        for record in self:
            record.state = 'done'
        return True

    def action_set_new(self):
        for record in self:
            record.state = 'new'
        return True

    @api.constrains('external_sheet_id')
    def _check_external_sheet_id(self):
        for record in self:
            if not isinstance(record.external_sheet_id, str) or len(record.external_sheet_id) < 10:
                raise ValidationError('Google sheet id must have at least 10 characters')

        return None

    @api.constrains('ignore_empty_columns', 'report_email')
    def _report_email_check(self):
        for record in self:
            if record.ignore_empty_columns and not record.report_email:
                raise ValidationError('Report email is required')

        return None

    @api.model
    def create(self, vals):
        if isinstance(vals, dict):
            vals = [vals]

        for el in vals:
            if el['name'] == 'amogus':
                raise ValidationError('Name can not be \'amogus\'')

        return super().create(vals)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_name_is_bebra(self):
        if any(record.name == 'bebra' for record in self):
            raise ValidationError('You cannot unlink bebra')

        return None


class GoogleSheetTag(models.Model):
    _name = 'google.sheet.tag'
    _description = 'Google Sheet Tag'
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The tag name must be unique')
    ]

    name = fields.Char(required=True)
    color = fields.Integer(string='Color')
    sheets_count = fields.Integer(compute='_compute_sheets_count')
    sheet_ids = fields.Many2many(comodel_name='google.sheet', string='Sheets')

    @api.depends('sheet_ids')
    def _compute_sheets_count(self):
        for record in self:
            record.sheets_count = len(record.sheet_ids)

        return None
