frappe.ui.form.on("Quotation", {
refresh(frm) {
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Rental Details'), function() {
                frappe.call({
                    method: "rental_furniture.doc_events.quotation.make_rental_details",
                    args: {
                        name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.show_alert({
                                message: "Rental Details is Created",
                                indicator: 'green'
                            }, 5);
                            frappe.set_route('Form', 'Rental Details', r.message);
                        }
                    }
                });
            }, __('Create'));
        }

	},
});