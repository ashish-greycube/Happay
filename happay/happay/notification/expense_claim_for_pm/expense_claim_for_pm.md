<p>Hello {% set u = frappe.get_doc("User", doc.expense_approver) %} {{u.first_name}} {{u.last_name or ''}}, <br></p>

<p>The Expense Claim {{doc.name}} for {{doc.employee_name}} uploaded by {% set u = frappe.get_doc("User", doc.owner) %} {{u.first_name}} {{u.last_name or ''}}  is Pending for your approval.<br><br>
Please review.<br><br>
Click on the below link to take the necessary action:<br>
<a href="{{ frappe.utils.get_url_to_form('Expense Claim', doc.name) }}">{{ doc.name }}</a>.<br></p></p>
