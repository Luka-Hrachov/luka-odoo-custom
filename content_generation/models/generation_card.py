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
    initial_product_name = fields.Char(string='Initial Product Name')
    initial_category_name = fields.Char(string='Initial Category Name')
    initial_blog_title = fields.Char(string='Initial Blog Title')
    initial_set_name = fields.Char(string='Initial Set Name')
    notes = fields.Text(string='Notes')
    image_1920 = fields.Image(string='Main Image')

    width = fields.Float(string='Width')
    length = fields.Float(string='Length')
    height = fields.Float(string='Height')
    weight = fields.Float(string='Weight')


