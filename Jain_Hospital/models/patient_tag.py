from typing import Self

from odoo import fields, models, api
from odoo.api import ValuesType


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name, active)', """Name must be unique"""),
    ]
    
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")

    @api.returns('self')
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + "(copy)"
            return super(PatientTag, self).copy(default=default)

