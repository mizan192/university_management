from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError
import re

class DepartmentMigration(models.Model):
    _name="department.migration"
    _description="Department switch process"

    name=fields.Char(string='Name', compute='retrive_student_details', store=True)
    student_id=fields.Char(string='Student ID', compute='retrive_student_details', store=True)
    # registration_id=fields.Char(string='Registration Id')
    birth_date=fields.Date(string='Birth Date', compute='retrive_student_details', store=True)
    image=fields.Binary(string='Image', compute='retrive_student_details', store=True)
    age = fields.Integer(string="age", compute='retrive_student_details', store=True)
    email=fields.Char(string='Email', compute='retrive_student_details', store=True)
    contact_number=fields.Char(string='Contact Number', compute='retrive_student_details', store=True)
    admission_date=fields.Date(string='Admission Date', compute='retrive_student_details', store=True)
    previous_faculty=fields.Char(string='Previous Faculty', compute='retrive_student_details', store=True)
    previous_department=fields.Char(string='Previous Department', compute='retrive_student_details', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    due = fields.Monetary(string='Due Amount', compute='retrive_student_details', store=True)
    invoice_status=fields.Char(string="Invoice Status", default='not created')
    reg_id = fields.Many2one(
        comodel_name='student.registration',
        domain="[('registration_status','=','Enrolled'),('registration_id', '!=', False)]",
        # placeholder="Student Registration no",
    )
    student_new_id=fields.Char(string='New ID')
    course_cost = fields.Monetary()
    invoice_status=fields.Char(string="Invoice Status", default='not created')

    # migration_date = fields.Date(default=fields.date.today)
    
# select switched faculty and department 
 
    faculty_choice=fields.Selection([('engineering','Engineering'),('business', 'Business'), ('arts', 'Arts')], string='Select Faculty', default='arts')

    e_departments_choice=fields.Many2one(
        comodel_name='engineering.faculty',
        # inverse_name='eng_student_id',
        string='Engineering Department'
    )
    b_departments_choice=fields.Many2one(
        comodel_name='business.faculty',
        # inverse_name='business_student_id',
        string="Business Department"
    )
    arts_departments_choice=fields.Many2one(
        comodel_name='arts.faculty',
        # inverse_name='arts_student_id',
        string="Arts Department"
    )

    
    accepted_faculty=fields.Char(string="Faculty", readonly=True)
    accepted_department=fields.Char(string="Department",readonly=True)
    congres_group=fields.Char(default="not_confirm")
    is_admitted=fields.Boolean(default=False)
    department_obj =fields.Char(string="Object")

    web_ribbon=fields.Char(string='MIGRATION CONFIRM')


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

    # record_ids = self.env['course.list'].search([]).ids
    # def get_ids(self):
    #     return self.env['course.list'].search([]).ids
    
    course_ids=fields.One2many(
        comodel_name='course.list',
        inverse_name='migrated_students_id',
        
        domain="['|',('course_faculty', '=', 'all'),('course_faculty', '=', accepted_faculty)]",

    )

    




    @api.onchange('reg_id')
    def show_student_details(self):
        self.name=self.reg_id.name
        self.student_id=self.reg_id.student_id
        self.image=self.reg_id.image
        self.email=self.reg_id.email
        self.admission_date=self.reg_id.admission_date
        self.previous_department=self.reg_id.accepted_department
        self.previous_faculty=self.reg_id.accepted_faculty
        self.due=self.reg_id.total_cost

        # print(self.reg_id.course_ids.course_name)


    @api.depends('reg_id')
    def retrive_student_details(self):
        for rec in self:
            rec.name=rec.reg_id.name
            rec.student_id=rec.reg_id.student_id
            rec.image=rec.reg_id.image
            rec.email=rec.reg_id.email
            rec.admission_date=rec.reg_id.admission_date
            rec.previous_department=rec.reg_id.accepted_department
            rec.previous_faculty=rec.reg_id.accepted_faculty
            rec.due=rec.reg_id.total_cost




    def arts_department_check(self,choosed_department):

        if float(choosed_department.hsc_english_min_grade) > float(self.reg_id.hsc_english_grade) or float(choosed_department.ssc_english_min_grade) > float(self.reg_id.ssc_english_grade):
            return False
        return True


    def business_department_check(self,choosed_department):    
        if self.arts_department_check(choosed_department)==False:        
            return False
        if float(choosed_department.hsc_finance_min_grade) > float(self.reg_id.hsc_finance_grade) or float(choosed_department.ssc_finance_min_grade) > float(self.reg_id.ssc_finance_grade):
            return False
        if float(choosed_department.hsc_accounting_min_grade) > float(self.reg_id.hsc_accounting_grade) or float(choosed_department.ssc_accounting_min_grade) > float(self.reg_id.ssc_accounting_grade):
            return False
        return True
    
    def engineering_department_check(self,choosed_department):
        if self.arts_department_check(choosed_department)==False:        
            return False
        if float(choosed_department.hsc_math_min_grade) > float(self.reg_id.hsc_math_grade) or float(choosed_department.ssc_math_min_grade) > float(self.reg_id.ssc_math_grade):
            return False
        if float(choosed_department.hsc_physics_min_grade) > float(self.reg_id.hsc_physics_grade) or float(choosed_department.ssc_physics_min_grade) > float(self.reg_id.ssc_physics_grade):
            return False
        if float(choosed_department.hsc_chemisty_min_grade) > float(self.reg_id.hsc_chemisty_grade) or float(choosed_department.ssc_chemisty_min_grade) > float(self.reg_id.ssc_chemisty_grade):
            return False
        if float(choosed_department.hsc_biology_min_grade) > float(self.reg_id.hsc_biology_grade) or float(choosed_department.ssc_biology_min_grade) > float(self.reg_id.ssc_biology_grade):
            return False
        return True




    def department_validity_check(self,choosed_department,choosed_faculty):
        if choosed_department=="" or choosed_faculty=="":
            return False
        if choosed_department.available_seats<=0:
            return False
        if choosed_department.hsc_min_grade>self.reg_id.hsc_result or choosed_department.ssc_min_grade>self.reg_id.ssc_result:
            return False
        isPossible=False
        if choosed_faculty=="engineering":
            isPossible= self.engineering_department_check(choosed_department)
        elif choosed_faculty=="business":
            isPossible=self.business_department_check(choosed_department)
        else: 
            isPossible=self.arts_department_check(choosed_department)
        return isPossible

    def check_department(self):
        self.registration_status='Reviewing'
        if self.is_admitted==True:
            raise ValidationError("You have alreadey admitted in a department!!!")
        choosed_department=""
        choosed_faculty=""
        if self.faculty_choice=='engineering':
            choosed_department = self.e_departments_choice
            choosed_faculty="engineering"
            if choosed_department==self.previous_department:
                raise ValidationError("You can't migrate to curent department!! Choose another one")
        elif self.faculty_choice=='business':
            choosed_department = self.b_departments_choice
            choosed_faculty="business"
            if choosed_department==self.previous_department:
                raise ValidationError("You can't migrate to curent department!! Choose another one")
        else:
            choosed_department = self.arts_departments_choice
            choosed_faculty="arts"
            if choosed_department==self.previous_department:
                raise ValidationError("You can't migrate to curent department!! Choose another one")
        if self.department_validity_check(choosed_department,choosed_faculty)==False:
            raise UserError("Choose another department!!!")
        else:
            self.accepted_faculty=self.faculty_choice
            self.accepted_department=choosed_department.department_name
            self.congres_group="congress"
            self.department_obj=choosed_department.id
        



    def update_previous_department_status(self):
        d_name = self.previous_department
        domain = [("department_name", "=", d_name)]
        record = self.env["department.information"].search(domain)
        new_seats=record.available_seats+1
        # student_count=record.total_students-1
        record.write({'available_seats':new_seats})
        # update in faculty based table 
        f_name = self.accepted_faculty+".faculty"
        domain = [("department_name", "=", d_name)]
        rec= self.env[f_name].search(domain)
        rec.write({'available_seats':new_seats})


    def update_department_status(self):
        d_name = self.accepted_department
        domain = [("department_name", "=", d_name)]
        record = self.env["department.information"].search(domain)
        new_seats=record.available_seats-1
        student_count=record.total_students+1
        s_count = str(student_count)
        record.write({'available_seats':new_seats,'total_students':student_count})
        # update in faculty based table 
        f_name = self.accepted_faculty+".faculty"
        domain = [("department_name", "=", d_name)]
        rec= self.env[f_name].search(domain)
        rec.write({'available_seats':new_seats,'total_students':student_count})

        #set student id while confirm : department_name_student_count
        s_id=self.accepted_department+"_"+s_count
        self.student_new_id=str(s_id)

        # seat update from  previous department 
        self.update_previous_department_status()


    def department_confirmation(self):
        self.registration_status='Enrolled'
        if self.is_admitted==True:
            raise ValidationError("You have alreadey migratted to another department!!!")
        self.is_admitted=True

        self.update_department_status()
         
         #update student profile
        domain = [("registration_id", "=", self.reg_id.registration_id)]
        record = self.env['student.profile'].search(domain)
        record.write({
            'accepted_faculty':self.accepted_faculty,
            'accepted_department':self.accepted_department,
            'student_id':self.student_new_id,
        })
        record = self.env['student.registration'].search(domain)
        record.write({
            'accepted_faculty':self.accepted_faculty,
            'accepted_department':self.accepted_department,
            'student_id':self.student_new_id,
        })

    

    def course_selection_method(self):
        self.invoice_status='to invoice'
        context={
            'default_name':self.name,
            'default_accepted_faculty':self.accepted_faculty,
            'default_accepted_department':self.accepted_department,
            'default_student_new_id':self.student_new_id,
            'default_course_cost':self.course_cost,
            'default_course_ids':self.course_ids.ids,
        }
        return {
            'name': "Course Selection",
            'res_model':'department.migration',
            'res_id':self.id,
            'type': 'ir.actions.act_window',
            'view_mode':'form',
            'view_id':self.env.ref('university_management.um_department_migration_course_select').id,
            'target':'new',
            'context':context,
        } 
    
    @api.onchange('course_ids')
    def course_cost_and_credit_hour(self):
        cost=0
        total_credit_hour=0
        for rec in self.course_ids:
            cost=cost+rec.lab_fee+(rec.credit_hour*rec.credit_hour_fee)
            total_credit_hour=total_credit_hour+rec.credit_hour
        # if self.credit_hour>self.max_credit_hour:
        #     ValidationError("You Cannot ")
        self.course_cost=cost
        # self.credit_hour=total_credit_hour

        #update course cost in profile
        s_id=self.reg_id.registration_id
        domain = [('registration_id','=',s_id)]
        rec = self.env['student.profile'].search(domain)
        rec.write({
            'course_cost': self.course_cost,
        })
        rec = self.env['student.registration'].search(domain)
        rec.write({
            'course_cost': self.course_cost,
        })

   
    def confirm_course_selection(self):
        main_model = self.env['department.migration']
        c_ids = self.course_ids.ids
        values_to_save = {
            'course_ids': c_ids,
        }
        if self._context.get('active_id'):
            main_model.browse(self._context['active_id']).write(values_to_save)
        else:
            new_record = main_model.create(values_to_save)

        return{'type': 'ir.actions.act_window_close',}
    

    def create_invoice(self):
        # print('-------from miag----------')
        # print(self.reg_id.registration_id)
        s_id=self.student_new_id

        # domain = [('student_id','=',s_id)]
        # rec = self.env['student.registration'].search(domain)



        # course_id_list = self.course_ids.ids
        context = {
        # 'default_main_model_id': self.id,
        'default_name': self.name,
        'default_student_id': s_id,
        'default_registration_id':self.reg_id.registration_id,
        'default_faculty': self.accepted_faculty,
        'default_department': self.accepted_department,
        'default_course_fee': self.course_cost,
        'default_from_registration':False,
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