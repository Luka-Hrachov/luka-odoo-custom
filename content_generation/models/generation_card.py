from odoo import fields, models


class GenerationCard(models.Model):
    _name = 'generation.card'
    _description = 'Generation Card'

    name = fields.Char(string='Name', required=True)
    base_language_id = fields.Many2one('res.lang', string='Base Language', required=True)
    content_type = fields.Selection([
        ('product', 'Product'),
        ('set',  'Set'),
        ('category', 'Category'),
        ('blog', 'Blog')
    ])
    notes = fields.Text(string='Notes')
