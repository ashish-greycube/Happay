<p>Dear {{(doc.travel_agent|replace("- NFC","")|replace("- FC", "")|replace("- CRIF", ""))}},<br><br></p>

<p>I hope this email finds you well.<br><br></p>

<p>Please find the details required to book the ticket for the upcoming trip:<br><br></p>

<p>Passenger Details:<br><br>
{% if doc.booking_for == "Self"  %}
Passenger First Name: {{doc.passenger_first_name}}<br>
Passenger Last Name: {{doc.passenger_last_name}}<br>
Passenger Gender: {{doc.passenger_gender}}<br>
Passenger Email: {{doc.owner}}<br>

{% elif doc.booking_for == "Guest" %}
<table border="1">
    <tr>
        <td>Passenger First Name</td>
        <td>Passenger Last Name</td>
        <td>Passenger Gender</td>
    </tr>
    {% for row in doc.passenger_details %}
    <tr>
        <td>{{row.passenger_first_name}}</td>
        <td>{{row.passenger_last_name}}</td>
        <td>{{row.passenger_gender}}</td>
    </tr>
    {% endfor %}
</table>
{% endif %}
<br>
<!--please add coding if booking_for=Self than upar wala otherwise ye samne wala table{{doc.passenger_details}}-->
Source: {{doc.source}}<br>
Destination: {{doc.destination}}<br>
Travel From Date: {{ doc.get_formatted("from_date")}}<br>
Time (Onward): {{doc.time_onward}}<br>
Travel To Date: {{ doc.get_formatted("to_date")}}<br>
Time (Return): {{doc.time_return}}<br>
Kindly process the booking at your earliest convenience and let me know if you require any further information.<br><br></p>

<p>Thank you in advance for your assistance.</p>
