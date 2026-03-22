from odoo import fields, models


class GoogleSheet(models.Model):
    _name = 'google.sheet'
    _description = 'Google Sheet Import'

    name = fields.Char(required=True)
    external_sheet_id = fields.Char(required=True)
    line_ids = fields.One2many(
        comodel_name='google.sheet.line',
        inverse_name='sheet_id',
        string='Fields',
        copy=True,
    )