from odoo import api, fields, models, _
from pprint import pprint
from odoo.exceptions import ValidationError

class Voiture(models.Model):
    _name = 'location_cars.vehicule'
    _description = 'Vehicle'


    name = fields.Char(string="Name",compute="_compute_vehicle_name", store=True)
    description = fields.Text("Vehicule Description", required=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', required=True)
    Date_immatriculation = fields.Date("Date d'immatriculation", required=True,
                                   default=fields.Date.today, help='Date when the vehicle has been immatriculated')
    plaque_immatriculation = fields.Char("Plaque d'immatriculation",tracking=True,
                                help='License plate number of the vehicule (i = plate number for a car)', required=True)
    chass_num = fields.Char('Numéro de châssis', help='Unique number written on the vehicule motor (VIN/SN number)',
                         copy=False, required=True)
    model_id = fields.Many2one('location_cars.model', 'Model',
                               tracking=True, required=True, help='Model of the vehicule')
    chaise = fields.Integer('Nombre du chaise', help='Number of seats of the vehicle', required=True)
    anne_model = fields.Char('Année du modèle', help='Year of the model', required=True)
    portes = fields.Integer('Nombre de portes', help='Number of doors of the vehicle', default=4, required=True)
    etiquette = fields.Many2many('location_cars.etiquette', required=True)
    test = fields.Char('test',required=True)
    image_128 = fields.Binary(related='model_id.image_128', readonly=True)
    net_car_valeur = fields.Monetary(string="Valeur d'achat", help="Purchase value of the vehicle", required=True)
    residual_valeur = fields.Monetary(string="Valeur résiduelle", required=True)
    car_valeur = fields.Monetary(string="Valeur catalogue", help='Value of the bought vehicle', required=True)
    coleur = fields.Char(string="coleur", required=True)
    anne_model = fields.Date("année du modél", required=True)
    contract_ids = fields.One2many('location_cars.contract', 'vehicle_id', string='Contrats', copy=True, ondelete='cascade')
    odometer = fields.Float( string='Dernier Odometer',help='Odometer measure of the vehicle at the moment of this log', required=True)
    odometer_unit = fields.Selection([
        ('kilometers', 'km'),
        ('miles', 'mi')
    ], 'Odometer Unit', default='kilometers', help='Unit of the odometer ', required=True)
    transmission = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission',
                                    help='Transmission Used by the vehicle', required=True)
    Type_carburant = fields.Selection([
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('lpg', 'LPG'),
        ('electrique', 'Electrique'),
        ('hybride', 'Hybride')
    ], 'Type de carburant', help='Fuel Used by the vehicle', required=True)
    Nombre_chevaux = fields.Integer("Nombre de chevaux", required=True)
    puissance_tax = fields.Monetary('impôt du puissance', required=True)
    puissance = fields.Integer('puissance', help='Power in kW of the vehicle', required=True)
    co2 = fields.Float('CO2 Emissions', help='CO2 emissions of the vehicle', required=True)
    _sql_constraints = [
        ('unique_chass_num', 'unique(chass_num)', 'nombre chassis must be unique!'),
        ('unique_plaque_immatriculation', 'unique(plaque_immatriculation)', 'Plaque immatriculation must be unique!'),
    ]

    @api.depends('model_id.brand_id.name', 'model_id.name', 'plaque_immatriculation')
    def _compute_vehicle_name(self):
        for record in self:
            record.name = (record.model_id.brand_id.name or '') + '/' + (record.model_id.name or '') + '/' + (
                        record.plaque_immatriculation or _('No Plate'))

    @api.onchange('model_id.id')
    def changing_logo(self):
        print("dsqdsq")
        for line in self:
            line.image_128 = line.model_id.image_128
        return True

    @api.constrains('chass_num')
    def _check_your_field(self):
        for record in self:
            if record.chass_num and (not record.chass_num.isalnum() or len(record.chass_num) != 17):
                raise ValidationError("Your Field must be alphanumeric and have a length of 17.")