import frappe
from frappe import _


def get_data():
	return {
		"fieldname": "custom_rental_details",
		
		"transactions": [
			
            {"label": _("Related"), "items": ["Delivery Note", "Sales Invoice"]},		
		],
    }