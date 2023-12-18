from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError
import re

class StudentRegistration(models.Model):
    _name= 'student.registration'
    _description='Student registration'
    _rec_name="registration_id"


# personal information 
    name=fields.Char(string='Name', required=True)
    student_id=fields.Char(string='Student ID', readonly=True)
    birth_date=fields.Date(string='Birth Date', default=fields.Date.today)
    gender = fields.Selection([('male','Male'),('female', 'Female'), ('other', 'Other')], string='Gender', default='male')
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
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    # currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]))

    father_salary = fields.Monetary(string='Father Income', currency_field='currency_id', default=0)
    mother_salary = fields.Monetary(string='Mother Income', currency_field='currency_id', default=0)
    total_salary = fields.Monetary(string='Family Income', compute="_calculate_family_salary", currency_field='currency_id', store=True)
    f_email=fields.Char(string="Family Email")
    guardian_name=fields.Char(string='Guardian Name')
    guardian_relation = fields.Selection([('father','Father'),('mother', 'Mother'), ('brother', 'Brother'), ('sister', 'Sister')], string='Guardian Relation')
    guardian_contact=fields.Char(string='Guardian Contact')
    home_contact=fields.Char(string="Home Phone")


# academic information 
    school_name = fields.Char(string='School Name')
    collage_name = fields.Char(string='Collage Name')
    hsc_result=fields.Float(string="HSC Grade", default="3.50")
    ssc_result=fields.Float(string="SSC Grade", default="3.00")
    ssc_group=fields.Selection([('science','Science'),('commerce', 'Commerce'), ('arts', 'Arts')], string='SSC Group', default='arts')
    hsc_group=fields.Selection([('science','Science'),('commerce', 'Commerce'), ('arts', 'Arts')], string='HSC Group', default='arts')
    # subject wise inforamtion for department selection
    # grade_domain=[('a+','A+'),('a','A'),('a-','A-'),('b','B'),('c','C'),('d','D')]
    grade_domain=[('5.0','A+'),('4.5','A'),('4.0','A-'),('3.5','B'),('3.0','C'),('2.0','D')]
    hsc_math_grade=fields.Selection(grade_domain,string="HSC Math Grade", default="3.0")
    hsc_physics_grade=fields.Selection(grade_domain,string="HSC Physics Grade", default="3.0")
    hsc_chemisty_grade=fields.Selection(grade_domain,string="HSC Chemisty Grade", default="3.0")
    hsc_english_grade=fields.Selection(grade_domain,string="HSC English Grade", default="3.0")
    hsc_biology_grade=fields.Selection(grade_domain,string="HSC Biology Grade", default="3.0")
    hsc_finance_grade=fields.Selection(grade_domain,string="HSC finance Grade", default="3.0")
    hsc_accounting_grade=fields.Selection(grade_domain,string="HSC accounting Grade", default="3.0")
    
    ssc_math_grade=fields.Selection(grade_domain,string="SSC Math Grade", default="3.0")
    ssc_physics_grade=fields.Selection(grade_domain,string="SSC Physics Grade", default="3.0")
    ssc_chemisty_grade=fields.Selection(grade_domain,string="SSC Chemisty Grade", default="3.0")
    ssc_biology_grade=fields.Selection(grade_domain,string="SSC Biology Grade", default="3.0")
    ssc_finance_grade=fields.Selection(grade_domain,string="SSC finance Grade", default="3.0")
    ssc_accounting_grade=fields.Selection(grade_domain,string="SSC accounting Grade", default="3.0")
    ssc_english_grade=fields.Selection(grade_domain,string="SSC English Grade", default="3.0")
    

#social platform 
    linkedin_id=fields.Char(string="Linkedin Profile")
    meta_id=fields.Char(string="Meta Profile")
    instagram_id=fields.Char(string="Instagram Profile")
    codeforce_id=fields.Char(string="Codeforces Profile")
    leetcode_id=fields.Char(string="LeetCode Profile")
    github_id=fields.Char(string="Github Profile")

#others
    admission_date=fields.Date(string='Admission Date', default=fields.Date.today)
    registration_id=fields.Char(string='Registration Id', compute='generate_registration_id', store=True)
    REG_STATUS_SELECTION = [
        ('Draft', 'Draft'),
        ('Reviewing', 'Reviewing'),
        ('Enrolled', 'Enrolled'),
    ]

    registration_status = fields.Selection(
        selection=REG_STATUS_SELECTION,
        string='Admission Status',
        default='Draft',  
    )
    students_profile_relation = fields.Many2one(
        comodel_name='student.profile',
    )

    web_ribbon=fields.Char(string='ADMITTED')






    
#department selection 

    faculty_name=fields.Selection([('engineering','Engineering'),('business', 'Business'), ('arts', 'Arts')], default='arts', string='Select Faculty' )

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


# select department with one field from department model using domain 
    select_department = fields.Many2one(
        comodel_name='department.information',
        domain="[('faculty', '=', faculty_name)]",
        string="department select"  
    )

    
    accepted_faculty=fields.Char(string="Faculty", readonly=True)
    accepted_department=fields.Char(string="Department",readonly=True)
    congres_group=fields.Char(default="not_confirm")
    is_admitted=fields.Boolean(default=False)
    department_obj =fields.Char(string="Object")





    # course selection after confirm 

    course_ids=fields.One2many(
        comodel_name='course.list',
        inverse_name='students_id',
        domain="['|',('course_faculty', '=', 'all'),('course_faculty', '=', accepted_faculty)]",
        # string="select course"  
    )

    course_cost=fields.Monetary(string='Course Cost', default=0, readonly='1')
    credit_hour=fields.Float(string='Credit Hour')
    
    max_credit_hour=fields.Float(string='Max Credit', compute="_set_max_credit_limit", store=True)
    total_cost = fields.Monetary(string='Fee', readonly='1', default=0)
    invoice_status=fields.Char(string="Invoice Status", default='not created')
    due_date=fields.Date(string='Due Date')

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


            

    @api.depends('name')
    def generate_registration_id(self):
        for rec in self:
            rec.registration_id="S_"+str(rec.id)
            

    @api.onchange('name')
    def check_registration_id(self):
        if self.registration_id!=False:
            self.registration_id=False
       














    def calculate_credit(self,hsc_r,hsc_g):
        credit = 15
        max_cr = 26
        if hsc_g=='commerce':
            credit=credit+3
        if hsc_g=='scienc':
            credit=credit+6
        if hsc_r == 5.00:
            credit=credit+5
        elif hsc_r>= 4.5:
            credit=credit+3
        elif hsc_r>= 4:
            credit=credit+2
        else:
            credit=credit+1
        return credit
    


#    set maximum credit limit for student 
    @api.depends('hsc_result','hsc_group')
    def _set_max_credit_limit(self):
        for rec in self:
            count=self.calculate_credit(self.hsc_result,self.hsc_group)
            rec.max_credit_hour=count

   


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
        if choosed_department.available_seats<=0:
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
        self.registration_status='Reviewing'
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
    # def decrease_seat_and_increase_student_count_in_department(self):
    #     if self.accepted_faculty=='engineering':
    #         rec = self.env['engineering.faculty'].browse(int(self.department_obj))
    #         new_seats = rec.available_seats-1
    #         rec.write({'available_seats':new_seats})
    #     if self.accepted_faculty=='business':
    #         rec = self.env['business.faculty'].browse(int(self.department_obj))
    #         new_seats = rec.available_seats-1
    #         rec.write({'available_seats':new_seats})
    #     if self.accepted_faculty=='arts':
    #         rec = self.env['arts.faculty'].browse(int(self.department_obj))
    #         new_seats = rec.available_seats-1
    #         rec.write({'available_seats':new_seats})



    def decrease_seat_and_increase_student_count_in_department(self):
        # update in department table 
        d_name = self.accepted_department
        domain = [("department_name", "=", d_name)]
        record = self.env["department.information"].search(domain)
        new_seats=record.available_seats-1
        student_count=record.total_students+1
        s_count = str(student_count)
        # print("-------------student count ------------", record.total_students)

        record.write({'available_seats':new_seats,'total_students':student_count})
        # update in faculty based table 
        f_name = self.accepted_faculty+".faculty"
        
        domain = [("department_name", "=", d_name)]
        rec= self.env[f_name].search(domain)
        rec.write({'available_seats':new_seats,'total_students':student_count})

        #set student id while confirm : department_name_student_count
        s_id=self.accepted_department+"_"+s_count
        self.student_id=str(s_id)




    # after confirm seat will be decrease 
    def confirm_department_registration(self):
        self.registration_status='Enrolled'
        if self.is_admitted==True:
            raise ValidationError("You have alreadey admitted in a department!!!")
        self.is_admitted=True
        self.decrease_seat_and_increase_student_count_in_department()
        
        #add student in profile
        self.env['student.profile'].create({
            'name':self.name,
            'student_id':self.student_id,
            'registration_id':self.registration_id,
            'accepted_faculty':self.accepted_faculty,
            'accepted_department':self.accepted_department,
            'course_cost':0,
            'hsc_result':self.hsc_result,
            'ssc_result':self.ssc_result,
            'image':self.image,
            # 'course_list':self.course_ids
        })
    


    # select course 
    def open_course_selection_wizard_form(self):
        self.invoice_status='to invoice'

        # passing One2many filed ids
        course_id_list = self.course_ids.ids

        context = {
        'default_main_model_id': self.id,
        'default_name': self.name,
        'default_student_id': self.student_id,
        'default_accepted_faculty': self.accepted_faculty,
        'default_accepted_department': self.accepted_department,
        'default_course_ids': course_id_list,
        }
        new_context = self._context.copy()

        return {
            'name': "Course Selection Panel",
            'type': 'ir.actions.act_window',
            'res_model': 'student.registration',
            'res_id':self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('university_management.course_selection_wizard_view').id,
            'target': 'new',
            # 'target': 'current',
            'context': context,
        }
    

    # custom save button for course select popup window
    def custom_save_method(self):
        main_model = self.env['student.registration']
        c_ids = self.course_ids.ids
        values_to_save = {
            'course_ids': c_ids,
        }

        print(c_ids)

        if self._context.get('active_id'):
            main_model.browse(self._context['active_id']).write(values_to_save)
        else:
            new_record = main_model.create(values_to_save)

        return{'type': 'ir.actions.act_window_close',}
    

        # course_id_list = self.course_ids.ids

        # context = {
        # 'default_main_model_id': self.id,
        # 'default_name': self.name,
        # 'default_student_id': self.student_id,
        # 'default_accepted_faculty': self.accepted_faculty,
        # 'default_accepted_department': self.accepted_department,
        # 'default_course_ids': course_id_list,
        # }

        # return {
        #     'name': "Student Registration View",
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'student.registration',
        #     'view_mode': 'form',
        #     'view_id': self.env.ref('university_management.student_profile_after_course_selection').id,
        #     'target': 'current',
        #     'context': self._context
        # }

        





    #course fee calcualtion     

    @api.onchange('course_ids')
    def calculate_course_cost_and_credit_hour(self):
        cost=0
        total_credit_hour=0
        for rec in self.course_ids:
            cost=cost+rec.lab_fee+(rec.credit_hour*rec.credit_hour_fee)
            total_credit_hour=total_credit_hour+rec.credit_hour
        # if self.credit_hour>self.max_credit_hour:
        #     ValidationError("You Cannot ")
        self.course_cost=cost
        self.credit_hour=total_credit_hour

        #update course cost in profile
        s_id=self.student_id
        domain = [('student_id','=',s_id)]
        rec = self.env['student.profile'].search(domain)
        rec.write({
            'course_cost': self.course_cost,
        })
        rec = self.env['student.registration'].search(domain)
        rec.write({
            'course_cost': self.course_cost,
        })






    # create invoice for students 
    # @api.model 
    def create_invoice(self):
        s_id=self.student_id
        domain = [('student_id','=',s_id)]
        rec = self.env['student.registration'].search(domain)



        # course_id_list = self.course_ids.ids
        context = {
        # 'default_main_model_id': self.id,
        'default_name': self.name,
        'default_student_id': s_id,
        'default_registration_id': self.registration_id,
        'default_faculty': self.accepted_faculty,
        'default_department': self.accepted_department,
        'default_course_fee': self.course_cost,
        'default_from_registration':True,
        # 'default_course_ids': course_id_list,
        }

        
        return {
            'name': "Student Account View",
            'type': 'ir.actions.act_window',
            # 'res_id':self.id,
            'res_model': 'student.account',
            'view_mode': 'form',
            'view_id': self.env.ref('university_management.students_accounts_fees_calculation_views').id,
            'target': 'current',
            'context': context,
        }
    


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
        

    @api.onchange('contact_number')
    def check_phone_number(self):
        if self.contact_number==False:
            return
        if len(self.contact_number)==14 and self.check_14_digit(self.contact_number):
            return
        elif len(self.contact_number)==11 and self.check_11_digit(self.contact_number):
            phone_no="+880"+self.contact_number
            self.contact_number=phone_no
        else:
            # print(self.check_11_digit(self.contact_number[3:]))
            raise ValidationError("Enter valid phone number")




    # def is_valid_email(email):
    #     pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    #     return bool(pattern.match(email))


    @api.onchange('email')
    def check_email(self):
        if self.email==False:
            return
        if len(self.email)<10:
            mail=self.email+"@gmail.com"
            self.email=mail
        else:
            last_part =self.email[10]
            print(last_part)
            if last_part!="@gmail.com":
                mail=self.email+"@gmail.com"
                self.email=mail




    # show report 
    # def confirm_report(self):
    #     return {
    #         'name': "Report View",
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'student.report',
    #         'view_mode': 'form',
    #         'view_id': self.env.ref('university_management.student_reports_wizard_view').id,
    #         'target': 'new',
    #     }





    @api.model
    def create(self,vals):
        if 'name' in vals.keys() and vals['name']:
            name=vals['name']
            prefix=name[4:]
            full_name=name
            if vals['gender']=='female':
                if prefix!='Mrs.' and prefix!='mrs.' and prefix!='MRS.':
                    vals['name']="Mrs."+full_name
            else:
                prefix=name[3:]
                if prefix!='Mr.' and prefix!='mr.' and prefix!='MR.':
                    vals['name']="Mr."+full_name

        if 'registration_id' not in vals.keys():
            return super(StudentRegistration,self).create(vals)
        reg_id = vals['registration_id']
        record_exist = self.env['student.registration'].search(['registration_id','=',reg_id])

        if record_exist:
            rec = self.write(vals)
        else:
            return super(StudentRegistration,self).create(vals)















    #check existing record
    # @api.model
    # def check_existing_record(self,student_id):
    #     rec = self.env['student.registration'].search([('student_id','=',student_id)])
    #     return True if rec else False

    # @api.model
    # def create(self,vals):
    #     if not self.student_id:
    #         return super(StudentRegistration,self).create(vals)
    #     record_exist=self.check_existing_record(vals['student_id'])
        
    #     if record_exist:
    #         record = self.browse(record_exist.id).write(vals)
    #     else:
    #         record=super(StudentRegistration,self).create(vals)
    #     return record


    # @api.model
    # def write(self,vals):
    #     if not self.student_id:
    #         return super(StudentRegistration,self).write(vals)
    #     existing_record = self.check_existing_record(vals['student_id'])
    #     if existing_record:
    #         record = self.browse(existing_record.id).write(vals)
    #     else:
    #         record = super(StudentRegistration, self).write(vals)

    #     return record

    