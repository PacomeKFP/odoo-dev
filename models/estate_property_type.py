from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = "name asc"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", "Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order properties based on types. Lower is better.")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id", "Offers")
    offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count')

    # --------- Constraints ---------#
    _sql_constraints = [
        ("name", "unique(name)", "Property name must be unique")
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for _type in self:
            _type.offer_count = len(_type.offer_ids)
