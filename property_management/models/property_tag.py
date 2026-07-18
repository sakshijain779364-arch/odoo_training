from odoo import api, fields, models, tools


class PropertyTag(models.Model):
    _name = 'property.tag'
    _description = 'Property Tag'

    name = fields.Char(string="Name" , required=True)
    property_id = fields.Many2one('property.property', required=True)
