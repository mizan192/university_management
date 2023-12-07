{
    'name':'University Management System',
    'summary': 'Student Registration and Migration system for University',
    'description': 'A module for managing student registration, department switching and related processes in a university system.',
    'category': 'Education',
    'version':'16.0.1.1',
    'author':'Mizan',
    'depends':["base"],
    'data':[
        'security/ir.model.access.csv',
        'views/student_registration_view.xml',
        'views/department_information_view.xml',
        'views/engineering_faculty_view.xml',
        'views/business_faculty_view.xml',
        'views/arts_faculty_view.xml',
        'views/student_profile_view.xml',
        'views/course_list_view.xml',
        'views/department_migration_view.xml',
        'views/menu.xml',
    ],
    
    'installable': True,
    'application': True,
    'license':'LGPL-3',
    'images': ['static/description/icon.png'],
    'sequence': -1,

}
