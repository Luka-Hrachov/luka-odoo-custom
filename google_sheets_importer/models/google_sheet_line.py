from odoo import fields, models


class GoogleSheetLine(models.Model):
    _name = 'google.sheet.line'
    _description = 'Google Sheet Field Mapping'

    sheet_id = fields.Many2one(
        comodel_name='google.sheet',
        string='Sheet',
        required=True,
        ondelete='cascade',
    )
    sheet_column_name = fields.Char(
        string='Sheet Column',
        required=True,
    )
    odoo_field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Odoo Field',
    )
    sequence = fields.Integer(default=10)

    def action_test_line(self):
        for record in self:
            print(f"Тестуємо колонку: {record.sheet_column_name}")
        return True