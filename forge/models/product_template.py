from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_ids = fields.Many2many('website')
