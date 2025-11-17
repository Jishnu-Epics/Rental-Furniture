# Copyright (c) 2025, jishnu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentalDetails(Document):
	pass


@frappe.whitelist()
def make_sales_invoice(name):
    rental = frappe.get_doc("Rental Details", name)

    si = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": rental.customer,
    })
    for item in rental.rental_items:
        si_item = si.append("items", {})
        si_item.item_code = item.item_code
        si_item.item_name = item.item
        si_item.qty = item.qty
        si_item.rate = item.rental_rate
       
    si.insert(ignore_permissions=True)
    si.submit()

    frappe.msgprint(f"Sales Invoice {si.name} created successfully")

    return si.name
