# -*- coding: utf-8 -*-
{
    'name': "Knance",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "PacomeKFP",
    'website': "https://github.com/PacomeKFP",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "license": "LGPL-3",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'mail', 'project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'data/sequences.xml',


        'views/knance_collector_views.xml',
        'views/knance_transaction_views.xml',
        'views/knance_customer_views.xml',
        'views/menu_views.xml',
    ],
    "application": True,
}

