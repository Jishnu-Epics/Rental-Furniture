import frappe
from frappe import _

@frappe.whitelist()
def make_rental_details(name):
    quotation = frappe.get_doc("Quotation", name)
    customer = _make_customer(quotation.name)

    d = frappe.new_doc("Rental Details")
    d.customer = customer.name
    d.quotation = quotation.name

    for item in quotation.items:
        d.append("rental_items", {
            "item_code": item.item_code,
            "qty": item.qty,
            "rate": item.rate,
        })

    d.save()
    return d.name

def create_customer_from_lead(lead_name, ignore_permissions=False):
	from erpnext.crm.doctype.lead.lead import _make_customer

	customer = _make_customer(lead_name, ignore_permissions=ignore_permissions)
	customer.flags.ignore_permissions = ignore_permissions

	try:
		customer.insert()
		return customer
	except frappe.MandatoryError as e:
		handle_mandatory_error(e, customer, lead_name)
		
def _make_customer(source_name, ignore_permissions=False):
	quotation = frappe.db.get_value(
		"Quotation",
		source_name,
		["order_type", "quotation_to", "party_name", "customer_name"],
		as_dict=1,
	)

	if quotation.quotation_to == "Customer":
		return frappe.get_doc("Customer", quotation.party_name)

	# Check if a Customer already exists for the Lead or Prospect.
	existing_customer = None
	if quotation.quotation_to == "Lead":
		existing_customer = frappe.db.get_value("Customer", {"lead_name": quotation.party_name})
	
	if existing_customer:
		return frappe.get_doc("Customer", existing_customer)

	# If no Customer exists, create a new Customer or Prospect.
	if quotation.quotation_to == "Lead":
		return create_customer_from_lead(quotation.party_name, ignore_permissions=ignore_permissions)
	
	return None




def handle_mandatory_error(e, customer, lead_name):
	from frappe.utils import get_link_to_form

	mandatory_fields = e.args[0].split(":")[1].split(",")
	mandatory_fields = [_(customer.meta.get_label(field.strip())) for field in mandatory_fields]

	frappe.local.message_log = []
	message = _("Could not auto create Customer due to the following missing mandatory field(s):") + "<br>"
	message += "<br><ul><li>" + "</li><li>".join(mandatory_fields) + "</li></ul>"
	message += _("Please create Customer from Lead {0}.").format(get_link_to_form("Lead", lead_name))

	frappe.throw(message, title=_("Mandatory Missing"))
