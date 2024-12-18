<p>{% set supplier_name = (doc.supplier|replace("- NFC","")|replace("- FC", "")|replace("- CRIF", "")) %}</p>

<p>Dear {{supplier_name}},<br></p>

<p>We hope this email finds you well.<br></p>

<p>We are writing to confirm that the payment for your invoice no. {{doc.supplier_invoice_number}} dated {{ doc.get_formatted("supplier_invoice_date") }} for the Invoice amount of {{doc.bill_amount}}, after deducting the TDS {{doc.tds_computed_amount}} ( TDS {{doc.tds_rate}} on {{doc.tds_amount}} ) Net payment Rs {{doc.net_payable_amount}}</p>

<p><p>Thank you for your cooperation.</p><br><br>

{{doc.company}}</p>
