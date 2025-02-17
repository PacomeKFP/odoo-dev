from odoo import fields, models, api


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("estate.property", "salesperson_id", string="Owned Properties",
                                   domain=lambda self: "[('salesperson_id', '=', self.env.user)]")
