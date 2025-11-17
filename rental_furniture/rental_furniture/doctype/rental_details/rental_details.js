// Copyright (c) 2025, jishnu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Details", {
refresh(frm) {
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Delivery Note'), function() {
                frappe.call({
                    method: "rental_furniture.rental_furniture.doctype.rental_details.rental_details.make_dn",
                    args: {
                        name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.show_alert({
                                message: "Delivery Note is Created",
                                indicator: 'green'
                            }, 5);
                            frappe.set_route('Form', 'Delivery Note', r.message);
                        }
                    }
                });
            }, __('Create'));
        }

	},
    start_date: function(frm) {
        calculate_days(frm);
    },
    end_date: function(frm) {
        calculate_days(frm);
    },
 
});
function calculate_days(frm) {
    if (frm.doc.start_date && frm.doc.end_date) {
        let start = frappe.datetime.str_to_obj(frm.doc.start_date);
        let end = frappe.datetime.str_to_obj(frm.doc.end_date);

        let diff = frappe.datetime.get_day_diff(end, start) + 1;

        if (diff < 0) {
            frappe.msgprint("End Date must be after Start Date");
            frm.set_value("total_rent_days", 0);
            return;
        }

        frm.set_value("total_rent_days", diff);
    }
}

frappe.ui.form.on("Rental Items", {
    qty: function(frm, cdt, cdn) {
        calculate_total(frm)
    },
    rate: function(frm, cdt, cdn) {
        calculate_total(frm)
    },
    rental_items_remove: function(frm, cdt, cdn) {
        calculate_total(frm)
    }
});

function calculate_total(frm) {
    let total = 0;
    let qty = 0;
   
    frm.doc.rental_items.forEach(row => {
        row.amount = (row.qty || 0) * (row.rate || 0);
        total += row.amount;
        qty += row.qty || 0; 
    });

    frm.set_value("total_amount", total);
    frm.set_value("total_qty", qty);
    frm.refresh_fields();
}
