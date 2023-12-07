from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError

class StudentRegistration(models.Model):
    _name= 'student.registration'
    _description='Student registration'
    _rec_name="name"


# personal information 
    name=fields.Char(string='Name', required=True)
    student_id=fields.Char(string='Student ID', compute="_generate_id")
    birth_date=fields.Date(string='Birth Date', default=fields.Date.today)
    gender = fields.Selection([('male','Male'),('female', 'Female'), ('other', 'Other')], string='Gender')
    image=fields.Binary(string='Image')
    age = fields.Integer(string="age", compute="_calculate_age", store=True)
    email=fields.Char(string='Email')
    contact_number=fields.Char(string='Contact Number')
    english_proficiency=fields.Selection([('basic','Basic'),('intermediate', 'Intermediate'), ('advanced', 'Advanced')], string='English Proficiency')

#address information 
    address=fields.Text(string='Address')
    emergency_contact = fields.Char(string='Emergency Contact')
    nid=fields.Char(string="National ID")
    home_city=fields.Char(string="Home City")
    religion=fields.Char(string="Religion")
    nationality=fields.Char(string="Nationality")
    
# family information 
    father_name=fields.Char(string='Father Name')
    mother_name=fields.Char(string='Mother Name')
    father_occupation=fields.Char(string='Father Occupation')
    mother_occupation=fields.Char(string='Mother Occupation')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    father_salary = fields.Monetary(string='Father Income', currency_field='currency_id', default=0)
    mother_salary = fields.Monetary(string='Mother Income', currency_field='currency_id', default=0)
    total_salary = fields.Integer(string='Family Income', compute="_calculate_family_salary", store=True)
    f_email=fields.Char(string="Family Email")
    guardian_name=fields.Char(string='Guardian Name')
    guardian_relation = fields.Selection([('father','Father'),('mother', 'Mother'), ('brother', 'Brother'), ('sister', 'Sister')], string='Guardian Relation')
    guardian_contact=fields.Char(string='Guardian Contact')
    home_contact=fields.Char(string="Home Phone")

# academic information 
    school_name = fields.Char(string='School Name')
    collage_name = fields.Char(string='Collage Name')
    hsc_result=fields.Float(string="HSC Grade", default="2.00")
    ssc_result=fields.Float(string="SSC Grade", default="2.00")
    ssc_group=fields.Selection([('science','Science'),('commerce', 'Commerce'), ('arts', 'Arts')], string='SSC Group', default='arts')
    hsc_group=fields.Selection([('science','Science'),('commerce', 'Commerce'), ('arts', 'Arts')], string='HSC Group', default='arts')
    # subject wise inforamtion for department selection
    # grade_domain=[('a+','A+'),('a','A'),('a-','A-'),('b','B'),('c','C'),('d','D')]
    grade_domain=[('5.0','A+'),('4.5','A'),('4.0','A-'),('3.5','B'),('3.0','C'),('2.0','D')]
    hsc_math_grade=fields.Selection(grade_domain,string="HSC Math Grade", default="2.0")
    hsc_physics_grade=fields.Selection(grade_domain,string="HSC Physics Grade", default="2.0")
    hsc_chemisty_grade=fields.Selection(grade_domain,string="HSC Chemisty Grade", default="2.0")
    hsc_english_grade=fields.Selection(grade_domain,string="HSC English Grade", default="2.0")
    hsc_biology_grade=fields.Selection(grade_domain,string="HSC Biology Grade", default="2.0")
    hsc_finance_grade=fields.Selection(grade_domain,string="HSC finance Grade", default="2.0")
    hsc_accounting_grade=fields.Selection(grade_domain,string="HSC accounting Grade", default="2.0")
    
    ssc_math_grade=fields.Selection(grade_domain,string="SSC Math Grade", default="2.0")
    ssc_physics_grade=fields.Selection(grade_domain,string="SSC Physics Grade", default="2.0")
    ssc_chemisty_grade=fields.Selection(grade_domain,string="SSC Chemisty Grade", default="2.0")
    ssc_biology_grade=fields.Selection(grade_domain,string="SSC Biology Grade", default="2.0")
    ssc_finance_grade=fields.Selection(grade_domain,string="SSC finance Grade", default="2.0")
    ssc_accounting_grade=fields.Selection(grade_domain,string="SSC accounting Grade", default="2.0")
    ssc_english_grade=fields.Selection(grade_domain,string="SSC English Grade", default="2.0")
    

#social platform 
    linkedin_id=fields.Char(string="Linkedin Profile")
    meta_id=fields.Char(string="Meta Profile")
    instagram_id=fields.Char(string="Instagram Profile")
    codeforce_id=fields.Char(string="Codeforces Profile")
    leetcode_id=fields.Char(string="LeetCode Profile")
    github_id=fields.Char(string="Github Profile")

    
#department selection 

    faculty_name=fields.Selection([('engineering','Engineering'),('business', 'business'), ('arts', 'Arts')], string='Select Faculty')

    engineering_departments=fields.Many2one(
        comodel_name='engineering.faculty',
        # inverse_name='eng_student_id',
        string='Engineering Department'
    )
    business_departments=fields.Many2one(
        comodel_name='business.faculty',
        # inverse_name='business_student_id',
        string="Business Department"
    )
    arts_departments=fields.Many2one(
        comodel_name='arts.faculty',
        # inverse_name='arts_student_id',
        string="Arts Department"
    )
    
    accepted_faculty=fields.Char(string="Faculty", readonly=True)
    accepted_department=fields.Char(string="Department",readonly=True)
    congres_group=fields.Char(default="not_confirm")
    is_admitted=fields.Boolean(default=False)
    department_obj =fields.Char(string="Object")


    # next step : there will three one2many field 
    # for three faculty class, according to selection 
    # faculty , res two field will be readonly(not accessable vai xml attrs)
    # and  accroding to student result i will check all department and
    # collect all department which are possible for her,, this
    # list will show in text field for her view,, if he select
    # any field in selection which is not possible for her, then 
    # it will create a error message 
    #next confirm button for generating course list for this department





  











#calculate age and show in age field and check min age requirement
    @api.onchange('birth_date')
    def _calculate_and_show_age(self):
        self.age=False
        for record in self:
            record.age=relativedelta(date.today(),record.birth_date).years

    @api.constrains('birth_date')
    def _check_student_minimum_age_requirement(self):
        for record in self:
            calculated_age=relativedelta(date.today(),record.birth_date).years
            if calculated_age > 25:
                raise models.ValidationError('Students over 34 years old cannot be admitted.')  
            else:
                record.age=calculated_age

    @api.depends('birth_date')
    def _calculate_age(self):
        self.age=False
        for record in self:
            record.age=relativedelta(date.today(),record.birth_date).years


# salary calculation for family
    @api.onchange('father_salary','mother_salary')
    def _calculate_family_salary_and_show(self):
        for record in self:
            record.total_salary=record.father_salary+record.mother_salary


    @api.depends('father_salary','mother_salary')
    def _calculate_family_salary(self):
        for record in self:
            record.total_salary=record.father_salary+record.mother_salary

   
   
   
    #id generate
    # student id will be generated via department selection 
    def _generate_id(self):
        for record in self:
            record.student_id=record.ids








    # generate department list comparing with academic result and department requirements
    #convert subject grade to to lower case and then in flot value
    #after button click new student will be registraed,, so i need to 
    #override unlink method for delete this record if he/she not admitted

    possible_engineering_departments=[]
    possible_business_departments=[]
    possible_arts_departments=[]

    def check_arts_department(self,choosed_department):

        if float(choosed_department.hsc_english_min_grade) > float(self.hsc_english_grade) or float(choosed_department.ssc_english_min_grade) > float(self.ssc_english_grade):
            return False
        return True


    def check_business_department(self,choosed_department):    
        if self.check_arts_department(choosed_department)==False:        
            return False
        if float(choosed_department.hsc_finance_min_grade) > float(self.hsc_finance_grade) or float(choosed_department.ssc_finance_min_grade) > float(self.ssc_finance_grade):
            return False
        if float(choosed_department.hsc_accounting_min_grade) > float(self.hsc_accounting_grade) or float(choosed_department.ssc_accounting_min_grade) > float(self.ssc_accounting_grade):
            return False
        return True
    
    def check_engineering_department(self,choosed_department):
        if self.check_arts_department(choosed_department)==False:        
            return False
        if float(choosed_department.hsc_math_min_grade) > float(self.hsc_math_grade) or float(choosed_department.ssc_math_min_grade) > float(self.ssc_math_grade):
            return False
        if float(choosed_department.hsc_physics_min_grade) > float(self.hsc_physics_grade) or float(choosed_department.ssc_physics_min_grade) > float(self.ssc_physics_grade):
            return False
        if float(choosed_department.hsc_chemisty_min_grade) > float(self.hsc_chemisty_grade) or float(choosed_department.ssc_chemisty_min_grade) > float(self.ssc_chemisty_grade):
            return False
        if float(choosed_department.hsc_biology_min_grade) > float(self.hsc_biology_grade) or float(choosed_department.ssc_biology_min_grade) > float(self.ssc_biology_grade):
            return False
        return True




    

    def check_department_validity(self,choosed_department,choosed_faculty):
        if choosed_department=="" or choosed_faculty=="":
            return False
        if choosed_department.available_seats==0:
            return False
        if choosed_department.hsc_min_grade>self.hsc_result or choosed_department.ssc_min_grade>self.ssc_result:
            return False
        isPossible=False
        if choosed_faculty=="engineering":
            isPossible= self.check_engineering_department(choosed_department)
        elif choosed_faculty=="business":
            isPossible=self.check_business_department(choosed_department)
        else: 
            isPossible=self.check_arts_department(choosed_department)
        return isPossible


    # @api.model
    def department_check_according_to_grade(self):
        if self.is_admitted==True:
            raise ValidationError("You have alreadey admitted in a department!!!")
        choosed_department=""
        choosed_faculty=""
        if self.faculty_name=='engineering':
            choosed_department = self.engineering_departments
            choosed_faculty="engineering"
        elif self.faculty_name=='business':
            choosed_department = self.business_departments
            choosed_faculty="business"
        else:
            choosed_department = self.arts_departments
            choosed_faculty="arts"
        
        # print(choosed_department.department_name)

        if self.check_department_validity(choosed_department,choosed_faculty)==False:
            raise UserError("Choose another department!!!")
        else:
            self.accepted_faculty=self.faculty_name
            self.accepted_department=choosed_department.department_name
            self.congres_group="congress"
            self.department_obj=choosed_department.id
            



    # decrease seat for selecting department 
    def decrease_department_seat(self):
        if self.accepted_faculty=='engineering':
            rec = self.env['engineering.faculty'].browse(int(self.department_obj))
            new_seats = rec.available_seats-1
            rec.write({'available_seats':new_seats})
        if self.accepted_faculty=='business':
            rec = self.env['business.faculty'].browse(int(self.department_obj))
            new_seats = rec.available_seats-1
            rec.write({'available_seats':new_seats})
        if self.accepted_faculty=='arts':
            rec = self.env['arts.faculty'].browse(int(self.department_obj))
            new_seats = rec.available_seats-1
            rec.write({'available_seats':new_seats})
            


    # after confirm seat will be decrease 
    def confirm_department_registration(self):
        if self.is_admitted==True:
            raise ValidationError("You have alreadey admitted in a department!!!")
        self.is_admitted=True
        self.decrease_department_seat()
        
        #add student in profile
        self.env['student.profile'].create({
            'name':self.name,
            'student_id':self.student_id,
            'accepted_faculty':self.accepted_faculty,
            'accepted_department':self.accepted_department,
        })
       
