from odoo import fields,models,api

class DepartmentInformation(models.Model):
    _name="department.information"
    _description="University Department information and minimum requirements"
    _rec_name="department_name"

    department_name=fields.Char(string="Departmnet Name", required=True)
    department_code=fields.Char(string="Code")
    available_seats=fields.Integer(string="Available Seat", default=20)
    logo=fields.Image(string="Logo")
    phone=fields.Char(string="Phone")
    email=fields.Char(string="Email")
    department_description=fields.Text(string="Department Description")
    #minimum result required
    hsc_min_grade=fields.Char(string="HSC Grade Required", default="3.50")
    ssc_min_grade=fields.Char(string="SSC Grade Required", default="3.00")
    faculty=fields.Selection([('engineering','Engineering'),('business', 'business'), ('arts', 'Arts')], string='Faculty Type', default='arts')

    # minimum grade requirements
    grade_domain=[('a+','A+'),('a','A'),('a-','A-'),('b','B'),('c','C'),('d','D')]
    hsc_math_min_grade=fields.Selection(grade_domain,string='HSC Math Grade Required',default='a')
    hsc_physics_min_grade=fields.Selection(grade_domain,string='HSC Physics Grade Required',default='a-')
    hsc_chemisty_min_grade=fields.Selection(grade_domain,string='HSC Chemisty Grade Required',default='a-')
    hsc_english_min_grade=fields.Selection(grade_domain,string='HSC English Grade Required',default='b')
    hsc_biology_min_grade=fields.Selection(grade_domain,string='HSC Biology Grade Required',default='b')
    hsc_finance_min_grade=fields.Selection(grade_domain,string='HSC Finance Grade Required',default='a-')
    hsc_accounting_min_grade=fields.Selection(grade_domain,string='HSC Accounting Grade Required',default='b')
    ssc_math_min_grade=fields.Selection(grade_domain,string='SSC Math Grade Required',default='a')
    ssc_physics_min_grade=fields.Selection(grade_domain,string='SSC Physics Grade Required',default='a-')
    ssc_chemisty_min_grade=fields.Selection(grade_domain,string='SSC Chemisty Grade Required',default='a-')
    ssc_english_min_grade=fields.Selection(grade_domain,string='SSC English Grade Required',default='b')
    ssc_biology_min_grade=fields.Selection(grade_domain,string='SSC Biology Grade Required',default='b')
    ssc_finance_min_grade=fields.Selection(grade_domain,string='SSC Finance Grade Required',default='a-')
    ssc_accounting_min_grade=fields.Selection(grade_domain,string='SSC Accounting Grade Required',default='b')


