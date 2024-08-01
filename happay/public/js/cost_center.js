frappe.ui.form.on("Cost Center",{
    setup: function (frm) {
        console.log("OK")
        console.log(frm.doc.company)
        debugger

		frm.set_query("custom_bank_ledger", function () {
			return {
				filters: {
					company: frm.doc.company,
					account_type: 'Bank',
				},
			};
		})
    }
})