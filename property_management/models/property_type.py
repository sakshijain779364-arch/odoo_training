from odoo import api,fields,models,tools


class PropertyType(models.Model):
    _name = "property.type"
    _description = "Property Type"

    _sql_constraints = [
        (
            'unique_name', 'UNIQUE(name)',
            'The property type name must be unique.'
        ),
    ]

    name = fields.Char(string="Name")
    property_type = fields.Char(string="Property Type")
    postcode = fields.Integer(string="Postcode")
    expected_price = fields.Integer(string="Expected Price")
    selling_price = fields.Integer(string="Selling Price")
    available_from = fields.Date(string="Available From")
    property_type_id = fields.Many2one('property.type',string="Property Type")
    property_ids = fields.One2many('estate.property','property_type_id',string='Properties')
