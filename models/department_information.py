from odoo import fields,models,api
from odoo.exceptions import AccessError, UserError, ValidationError
import re
class DepartmentInformation(models.Model):
    _name="department.information"
    _description="University Department information and minimum requirements"
    _rec_name="department_name"

    department_name=fields.Char(string="Departmnet Name", required=True)
    department_code=fields.Char(string="Code", compute='generate_department_code')
    available_seats=fields.Integer(string="Available Seat", default=20)
    logo=fields.Image(string="Logo")
    phone=fields.Char(string="Phone")
    email=fields.Char(string="Email")
    department_description=fields.Text(string="Department Description")
    #minimum result required
    hsc_min_grade=fields.Float(string="HSC Grade Required", default="3.50")
    ssc_min_grade=fields.Float(string="SSC Grade Required", default="3.00")
    faculty=fields.Selection([('engineering','Engineering'),('business', 'Business'), ('arts', 'Arts')], string='Faculty Type', default='arts')
    total_students=fields.Integer(string="Department Students", default=0)

    # minimum grade requirements
    # grade_domain=[('a+','A+'),('a','A'),('a-','A-'),('b','B'),('c','C'),('d','D')]
    grade_domain=[('5.0','A+'),('4.5','A'),('4.0','A-'),('3.5','B'),('3.0','C'),('2.0','D')]
    hsc_math_min_grade=fields.Selection(grade_domain,string='HSC Math Grade Required',default='3.0')
    hsc_physics_min_grade=fields.Selection(grade_domain,string='HSC Physics Grade Required',default='3.0')
    hsc_chemisty_min_grade=fields.Selection(grade_domain,string='HSC Chemisty Grade Required',default='2.0')
    hsc_english_min_grade=fields.Selection(grade_domain,string='HSC English Grade Required',default='2.0')
    hsc_biology_min_grade=fields.Selection(grade_domain,string='HSC Biology Grade Required',default='2.0')
    hsc_finance_min_grade=fields.Selection(grade_domain,string='HSC Finance Grade Required',default='2.0')
    hsc_accounting_min_grade=fields.Selection(grade_domain,string='HSC Accounting Grade Required',default='2.0')
    ssc_math_min_grade=fields.Selection(grade_domain,string='SSC Math Grade Required',default='3.0')
    ssc_physics_min_grade=fields.Selection(grade_domain,string='SSC Physics Grade Required',default='2.0')
    ssc_chemisty_min_grade=fields.Selection(grade_domain,string='SSC Chemisty Grade Required',default='2.0')
    ssc_english_min_grade=fields.Selection(grade_domain,string='SSC English Grade Required',default='2.0')
    ssc_biology_min_grade=fields.Selection(grade_domain,string='SSC Biology Grade Required',default='2.0')
    ssc_finance_min_grade=fields.Selection(grade_domain,string='SSC Finance Grade Required',default='2.0')
    ssc_accounting_min_grade=fields.Selection(grade_domain,string='SSC Accounting Grade Required',default='2.0')


    # student_list=fields.Many2one()



    ##add department according to faculty type


    @api.depends('department_name')
    def generate_department_code(self):
        for rec in self:
            name = rec.department_name.lower()
            rec.department_code=name+"_"+str(rec.id)
            rec.department_name=name.upper()









    @api.model
    def department_add_in_faculty(self,faculty,department_name,department_code, available_seats,total_students,hsc_min_grade,ssc_min_grade,hsc_math_min_grade,hsc_physics_min_grade,hsc_chemisty_min_grade,hsc_english_min_grade,hsc_finance_min_grade,hsc_accounting_min_grade,hsc_biology_min_grade,ssc_math_min_grade,ssc_physics_min_grade,ssc_chemisty_min_grade,ssc_english_min_grade,ssc_finance_min_grade,ssc_accounting_min_grade,ssc_biology_min_grade):
        
        if faculty=='engineering':
            self.env['engineering.faculty'].create({
                'department_name':department_name,
                'department_code':department_code,
                'available_seats':available_seats,
                'total_students':total_students,
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
                'department_code':department_code,
                'available_seats':available_seats,
                'total_students':total_students,
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
                'department_code':department_code,
                'available_seats':available_seats,
                'total_students':total_students,
                'hsc_min_grade':hsc_min_grade,
                'ssc_min_grade':ssc_min_grade,
                'hsc_english_min_grade':hsc_english_min_grade,
                'ssc_english_min_grade':ssc_english_min_grade,
            })
        

    ##while creating department it will store in faculty wise

    @api.model
    def create(self,val):
        if ('department_name' in val.keys() and 'email' not in val.keys()) or ('department_name' in val.keys() and 'email' in val.keys() and val['email']==False):
            dname=val['department_name']
            val['email']=dname.lower()+"@gmail.com"
            print('---------------------------ai')   

        ctx = self.env.context.copy()
        rec=super(DepartmentInformation,self.with_context(ctx)).create(val)

        #after create a record it will department_add_in_faculty
        self.department_add_in_faculty(rec.faculty,rec.department_name, rec.department_code, rec.available_seats,rec.total_students,rec.hsc_min_grade,rec.ssc_min_grade,rec.hsc_math_min_grade,rec.hsc_physics_min_grade,rec.hsc_chemisty_min_grade,rec.hsc_english_min_grade,rec.hsc_finance_min_grade,rec.hsc_accounting_min_grade,rec.hsc_biology_min_grade,rec.ssc_math_min_grade,rec.ssc_physics_min_grade,rec.ssc_chemisty_min_grade,rec.ssc_english_min_grade,rec.ssc_finance_min_grade,rec.ssc_accounting_min_grade,rec.ssc_biology_min_grade)
        return rec   
    
    



    # duplicate record check 
    @api.constrains('department_name')
    def _check_duplicate_name(self):
        for record in self:
            if record.search_count([('department_name', 'ilike', record.department_name)]) > 1:
                raise ValidationError("Duplicate record with the same name found!")

    


    def check_11_digit(self,pno):
        if pno[0]!='0' or pno[1]!='1' or pno[2]=='2':
            return False
        pattern = re.compile(r".*[a-zA-Z].*")
        is_char=pattern.match(pno)
        return not is_char

    def check_14_digit(self,pno):
        if pno[0]=='+' and pno[1]=='8' and pno[2]=='8' and (self.check_11_digit(pno[3:])==True):
            return True
        else:
            return False
        

    @api.onchange('phone')
    def check_phone_number(self):
        if self.phone==False:
            return
        if len(self.phone)==14 and self.check_14_digit(self.phone):
            return
        elif len(self.phone)==11 and self.check_11_digit(self.phone):
            phone_no="+880"+self.phone
            self.phone=phone_no
        else:
            raise ValidationError("Enter valid phone number")


    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(pattern, email)
        return bool(match)

    # @api.onchange('email')
    # def check_email(self):
    #     if not self.is_valid_email(self.email):
    #         raise ValidationError('Email format is not correct')