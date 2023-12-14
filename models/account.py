from odoo import fields,models,api
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class StudentAccount(models.Model):
    _name="student.account"
    _description="Students account"


    name=fields.Char(string='Name')
    student_id=fields.Char(string='Id')
    faculty=fields.Char(string='Faculty')
    department=fields.Char(string='Department')
    course_fee=fields.Monetary(string='Course Cost',  readonly='1')

    admission_fee=fields.Monetary(string='Admission Fee', default=20000, readonly='1')  
    registration_fee=fields.Monetary(string='Registration Fee', default=5000, readonly='1')
    department_fee=fields.Monetary(string='Department Fee', compute='_check_department_fee', store = True)
    fine=fields.Monetary(string='Fine', default=0)
    scholarship=fields.Monetary(string='Scholarship', compute='_scholarship_calculation', store=True)
    total_fee=fields.Monetary(string='Total Fee', compute='_calculate_total_Fee', currency_field='currency_id', store=True)

    student_relation = fields.Many2one('student.profile')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    

    invoice_date=fields.Date(string='Invoice Date', default=fields.Date.today, readonly='1')
    due_date=fields.Date(string='Due Date')
    payment_method=fields.Selection([('cash','Cash'),('bank','Bank'),('bkash','Bkash')], string='Payment Method', default='cash')
    ready_to_invoiced=fields.Boolean(default=False)
    
    show_button=fields.Boolean(default=False)
    
    course_list=fields.Many2one(
        comodel_name='student.registration',
        domain="[('student_id','=',student_id)]",
    )








    @api.depends('faculty')
    def _check_department_fee(self):
        fees=12000
        if self.faculty=='engineering':
            fees=fees+5000
        if self.department=='business':
            fees=fees+2500
        self.department_fee=fees

    @api.depends('student_id')
    def _scholarship_calculation(self):
        
        domain = [('student_id','=',self.student_id)]
        rec = self.env['student.profile'].search(domain)
        discount=0
        fees=self.admission_fee+self.registration_fee
        hsc_result = rec.hsc_result
        ssc_result = rec.ssc_result

        if hsc_result>=5.00:
            discount=fees
        elif hsc_result>=4.75 and ssc_result>=5.00:
            discount=fees-(fees*.75)
        elif hsc_result>=4.50:
            discount=fees-(fees*.5)
        elif hsc_result>=4.00 and ssc_result>=4.25:
            discount=fees-(fees*.3)
        else:
            discount=0
        self.scholarship=discount




    @api.depends('student_id')
    def _calculate_total_Fee(self):
        for rec in self:
            rec.total_fee=rec.admission_fee+rec.course_fee+rec.registration_fee+rec.department_fee+rec.fine-rec.scholarship
        # self.total_fee=self.admission_fee+self.course_fee+self.registration_fee+self.department_fee+self.fine-self.scholarship

    

    @api.onchange('due_date')
    def check_due_date(self):
        # self.show_register_button=False
        
        if self.due_date==False:
            self.ready_to_invoiced=False
        
        elif fields.Date.from_string(self.due_date)<fields.Date.from_string(self.invoice_date):
            self.ready_to_invoiced=False
            # raise ValidationError("Due date can't be erailer than invoice-date")
            # ValidationError("Due date can't be erailer than invoice-date")
        else:
            self.ready_to_invoiced=True
        
        print('------------------------')

        for course in self.course_list:
            print('------ course name : ', course.course_name)
            print('------ course cost : ', course.single_course_fee)


    def confirm_fee(self):
        # self.show_button=True
        domain = [('student_id','=',self.student_id)]
        rec = self.env['student.profile'].search(domain)
        rec.write({'total_fee':self.total_fee})
        

    @api.model
    def create(self,vals):
        if 'student_id' not in vals.keys():
            return super(StudentAccount,self).create(vals)
        s_id = vals['student_id']
        record_exist = self.env['student.account'].search(['student_id','=',s_id])

        if record_exist:
            rec = self.write(vals)
        else:
            return super(StudentAccount,self).create(vals)













    def register_payment_method_action(self):
        return 
        context = {
        'default_name': self.name,
        'default_student_id': self.student_id,
        'default_accepted_faculty': self.accepted_faculty,
        'default_accepted_department': self.accepted_department,
        }
        

        return {
            'name': "Register Payment",
            'res_model':'student.account',
            'res_id':self.id,
            'type': 'ir.actions.act_window',
            'target':'new',
            'context':{
                'active_model':'student.account',
                'active_ids':self.ids
            },

        }    
    


