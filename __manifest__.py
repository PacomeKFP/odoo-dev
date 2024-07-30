# -*- coding: utf-8 -*-
{
    'name': 'Real Estate Old',
    'version': '1.0',

    'summary': "The real estate module as presented in the documentation",

    'description': """
        This  module covers a business area which is very specific and therefore not included in the standard set of modules: real estate. It is worth noting that before developing a new module, it is good practice to verify that Odoo doesn’t already provide a way to answer the specific business case.
    """,

    'author': "Pacome Kengali F.",
    'website': "https://PacomeKFP.github.io/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'license': "LGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
}
