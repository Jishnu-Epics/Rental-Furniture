import frappe
from frappe import _


def get_data():
	return {
		"fieldname": "custom_rental_details",
		"internal_links": {
			"Quotation": "quotation",
			
        },
		
		"transactions": [
			{"label": _("Reference"), "items": ["Quotation"]},	
            {"label": _("Related"), "items": ["Delivery Note", "Sales Invoice"]},		
		],
    }