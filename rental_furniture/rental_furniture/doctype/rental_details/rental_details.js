// Copyright (c) 2025, jishnu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Details", {
refresh(frm) {
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Sales Invoice'), function() {
                frappe.call({
                    method: "rental_furniture.rental_furniture.doctype.rental_details.rental_details.make_sales_invoice",
                    args: {
                        name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.show_alert({
                                message: "sales Invoice is Created",
                                indicator: 'green'
                            }, 5);
                            frappe.set_route('Form', 'Sales Invoice', r.message);
                        }
                    }
                });
            }, __('Create'));
        }

	},
});
