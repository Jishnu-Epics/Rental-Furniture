# Copyright (c) 2025, jishnu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class RentalDetails(Document):
	pass


@frappe.whitelist()
def make_dn(name):
    rental = frappe.get_doc("Rental Details", name)

    dn = frappe.get_doc({
        "doctype": "Delivery Note",
        "customer": rental.customer,
        "custom_rental_details": rental.name
    })
    for item in rental.rental_items:
        dn_item = dn.append("items", {})
        dn_item.item_code = item.item_code
        dn_item.item_name = item.item
        dn_item.qty = item.qty
        dn_item.rate = item.rate
       
    dn.insert(ignore_permissions=True)

    return dn.name

