from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string="Name", required=True)
    color = fields.Char(string="Color", default="#03FF02")