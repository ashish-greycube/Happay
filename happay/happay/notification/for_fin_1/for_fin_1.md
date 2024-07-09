<p>Hello,<br>

<p>The vendor invoice {{doc.name}} for {{(doc.supplier|replace("- NFC","")|replace("- FC", "")|replace("- CRIF", ""))}} uploaded by {% set u = frappe.get_doc("User", doc.owner) %} {{u.first_name}} {{u.last_name or ''}} is Pending for FIN 1 approval.<br><br>
Please review.<br><br>
Click on the below link to take the necessary action:<br>
<a href="{{ frappe.utils.get_url_to_form('Vendor Invoice', doc.name) }}">{{ doc.name }}</a>.<br></p></p>
