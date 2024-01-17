from odoo import api, fields, models, _

class TypeService(models.Model):
    _name = 'location_cars.type'
    _description = 'Voiture Type Service'

    name = fields.Char(required=True, translate=True)

    category = fields.Selection([
        ('contract', 'Contract'),
        ('service', 'Service')
        ], 'Category', required=True, help='Choose whether the service refer to contracts, vehicle services or both')
