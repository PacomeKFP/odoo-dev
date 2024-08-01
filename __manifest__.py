# -*- coding: utf-8 -*-
{
    'name': "Estate Account",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Pacome KFP",
    'website': "https://www.github.com/PacomeKFP",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'real_estate_old', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/estate_property_views.xml',
        # 'views/menu_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    # "application": True,

}
