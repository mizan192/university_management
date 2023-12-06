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


    # student_list=fields.Many2one()



    ##add department according to faculty type

    @api.model
    def department_add_in_faculty(self,faculty,department_name, available_seats,hsc_min_grade,ssc_min_grade,hsc_math_min_grade,hsc_physics_min_grade,hsc_chemisty_min_grade,hsc_english_min_grade,hsc_finance_min_grade,hsc_accounting_min_grade,hsc_biology_min_grade,ssc_math_min_grade,ssc_physics_min_grade,ssc_chemisty_min_grade,ssc_english_min_grade,ssc_finance_min_grade,ssc_accounting_min_grade,ssc_biology_min_grade):
        
        if faculty=='engineering':
            self.env['engineering.faculty'].create({
                'department_name':department_name,
                'available_seats':available_seats,
                'hsc_min_grade':hsc_min_grade,
                'ssc_min_grade':ssc_min_grade,
                'hsc_math_min_grade':hsc_math_min_grade,
                'hsc_physics_min_grade':hsc_physics_min_grade,
                'hsc_chemisty_min_grade':hsc_chemisty_min_grade,
                'hsc_biology_min_grade':hsc_biology_min_grade,
                'hsc_english_min_grade':hsc_english_min_grade,
                'ssc_math_min_grade':ssc_math_min_grade,
                'ssc_physics_min_grade':ssc_physics_min_grade,
                'ssc_chemisty_min_grade':ssc_chemisty_min_grade,
                'ssc_biology_min_grade':ssc_biology_min_grade,
                'ssc_english_min_grade':ssc_english_min_grade,
            })
        if faculty=='business':
            self.env['business.faculty'].create({
                'department_name':department_name,
                'available_seats':available_seats,
                'hsc_min_grade':hsc_min_grade,
                'ssc_min_grade':ssc_min_grade,
                'hsc_english_min_grade':hsc_english_min_grade,
                'hsc_finance_min_grade':hsc_finance_min_grade,
                'hsc_accounting_min_grade':hsc_accounting_min_grade,
                'ssc_english_min_grade':ssc_english_min_grade,
                'ssc_finance_min_grade':ssc_finance_min_grade,
                'ssc_accounting_min_grade':ssc_accounting_min_grade,
            })
        if faculty=='arts':
            self.env['arts.faculty'].create({
                'department_name':department_name,
                'available_seats':available_seats,
                'hsc_min_grade':hsc_min_grade,
                'ssc_min_grade':ssc_min_grade,
                'hsc_english_min_grade':hsc_english_min_grade,
                'ssc_english_min_grade':ssc_english_min_grade,
            })
        

    ##while creating department it will store in faculty wise

    @api.model
    def create(self,val):
        ctx = self.env.context.copy()

        rec=super(DepartmentInformation,self.with_context(ctx)).create(val)

        #after create a record it will department_add_in_faculty
        self.department_add_in_faculty(rec.faculty,rec.department_name, rec.available_seats,rec.hsc_min_grade,rec.ssc_min_grade,rec.hsc_math_min_grade,rec.hsc_physics_min_grade,rec.hsc_chemisty_min_grade,rec.hsc_english_min_grade,rec.hsc_finance_min_grade,rec.hsc_accounting_min_grade,rec.hsc_biology_min_grade,rec.ssc_math_min_grade,rec.ssc_physics_min_grade,rec.ssc_chemisty_min_grade,rec.ssc_english_min_grade,rec.ssc_finance_min_grade,rec.ssc_accounting_min_grade,rec.ssc_biology_min_grade)
        return rec   