from odoo import api, fields, models, _

class EtiquetteVoiture(models.Model):
    _name = 'location_cars.etiquette'
    _description = 'Vehicule etiquette'

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color Index')

    _sql_constraints = [('name_uniq', 'unique (name)', "Tag name already exists !")]