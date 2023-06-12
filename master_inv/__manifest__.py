# -*- coding: utf-8 -*-

# This module captures stock moves done in receipts and deliveries after they are validated,
# captures its inward and outward quantities, the from and to location of the move,
# Shows the overall inventory value.

{
    'name': 'Product Inventory Master',
    'version': "16.0",
    'summary': 'Inventory Master report captures the stock moves of all receipts and deliveries after its validation',
    'sequence': -1,
    'description': """Inventory Moves Master""",
    'author': 'PMCPL',
    'website': "www.primeminds.co",
    'category': 'Inventory',
    'depends': ['base', 'stock', 'contacts', 'account', 'purchase', 'product','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/inv_master_data.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3'
}

