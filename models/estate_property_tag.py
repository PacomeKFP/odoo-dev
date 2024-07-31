from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string="Name", required=True)

    # --------- Constraints ---------#
    _sql_constraints = [
        ("name", "unique(name)", "Property name must be unique")
    ]
