from odoo import api,fields,models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    never_drop_ship = fields.Boolean(string="Never Drop Ship")

