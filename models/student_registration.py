from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class StudentRegistration(models.Model):
    _name= 'student.registration'
    _description='Student registration'
    _rec_name="name"

# personal information 
    name=fields.Char(string='Name', required=True)
    student_id=fields.Char(string='Student ID', compute="_generate_id")
    birth_date=fields.Date(string='Birth Date',required=True)
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
    hsc_result=fields.Char(string="HSC Grade", default="2.00")
    ssc_result=fields.Char(string="SSC Grade", default="2.00")
    ssc_group=fields.Selection([('science','Science'),('commerce', 'Commerce'), ('arts', 'Arts')], string='SSC Group', default='arts')
    hsc_group=fields.Selection([('science','Science'),('commerce', 'Commerce'), ('arts', 'Arts')], string='HSC Group', default='arts')
    # subject wise inforamtion for department selection
    grade_domain=[('a+','A+'),('a','A'),('a-','A-'),('b','B'),('c','C'),('d','D')]
    hsc_math_grade=fields.Selection(grade_domain,string="HSC Math Grade", default="d")
    hsc_physics_grade=fields.Selection(grade_domain,string="HSC Physics Grade", default="d")
    hsc_chemisty_grade=fields.Selection(grade_domain,string="HSC Chemisty Grade", default="d")
    hsc_english_grade=fields.Selection(grade_domain,string="HSC English Grade", default="d")
    hsc_biology_grade=fields.Selection(grade_domain,string="HSC Biology Grade", default="d")
    hsc_finance_grade=fields.Selection(grade_domain,string="HSC finance Grade", default="d")
    hsc_accounting_grade=fields.Selection(grade_domain,string="HSC accounting Grade", default="d")
    
    ssc_math_grade=fields.Selection(grade_domain,string="SSC Math Grade", default="d")
    ssc_physics_grade=fields.Selection(grade_domain,string="SSC Physics Grade", default="d")
    ssc_chemisty_grade=fields.Selection(grade_domain,string="SSC Chemisty Grade", default="d")
    ssc_biology_grade=fields.Selection(grade_domain,string="SSC Biology Grade", default="d")
    ssc_finance_grade=fields.Selection(grade_domain,string="SSC finance Grade", default="d")
    ssc_accounting_grade=fields.Selection(grade_domain,string="SSC accounting Grade", default="d")
    ssc_english_grade=fields.Selection(grade_domain,string="SSC English Grade", default="d")
    

#social platform 
    linkedin_id=fields.Char(string="Linkedin Profile")
    meta_id=fields.Char(string="Meta Profile")
    instagram_id=fields.Char(string="Instagram Profile")
    codeforce_id=fields.Char(string="Codeforces Profile")
    leetcode_id=fields.Char(string="LeetCode Profile")
    github_id=fields.Char(string="Github Profile")

    
#department selection 
    faculty_name=fields.Selection([('engineering','Engineering'),('business', 'business'), ('arts', 'Arts')], string='Select Faculty', default='arts')

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




