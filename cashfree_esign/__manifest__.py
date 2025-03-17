# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
  'name': 'CashFree ESign',
  'version': '1.0',
  'depends': ['sign'],
  'category': 'Sales/Sign',
  'author': 'BHPR',
  'description': "Integrates Cashfree eSign API for Aadhaar-based document signing workflow.",
  'data': [
      'report/sign_log_report.xml',
      'views/res_config_settings.xml'
   ],
   'assets': {
      'web.assets_backend': [
          'cashfree_esign/static/src/**/*',
      ],
      'sign.assets_public_sign': [
          'cashfree_esign/static/src/**/*',
      ]
   },
   'license': 'OEEL-1',
}
