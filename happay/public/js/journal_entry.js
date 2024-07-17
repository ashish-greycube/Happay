frappe.ui.form.on("Journal Entry", {
  onload: function (frm) {
    frm.set_query("party", "accounts", function (doc, cdt, cdn) {
      let query = "",
        party_type = locals[cdt][cdn]["party_type"];
      if (party_type == "Customer")
        query = "happay.api.customer_query";
      else if (party_type == "Supplier")
        query = "happay.api.supplier_query";
      return {
        query: query,
        filters: {
          company: frm.doc.company,
        },
      };
    });
  },
});