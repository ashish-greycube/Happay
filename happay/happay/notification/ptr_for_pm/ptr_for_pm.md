<p>Hello {% set u = frappe.get_doc("User", doc.project_manager) %} {{u.first_name}} {{u.last_name or ''}}, <br></p>

<p>The Project Travel Request {{doc.name}} for guest uploaded by {% set u = frappe.get_doc("User", doc.owner) %} {{u.first_name}} {{u.last_name or ''}}  is Pending for your approval.<br><br>
Please review.<br><br>
Click on the below link to take the necessary action:<br>
<a href="{{ frappe.utils.get_url_to_form('Project Travel Request', doc.name) }}">{{ doc.name }}</a>.<br></p></p>
