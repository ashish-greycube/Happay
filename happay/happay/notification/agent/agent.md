Dear {{(doc.travel_agent|replace("- NFC","")|replace("- FC", "")|replace("- CRIF", ""))}},<br><br>

I hope this email finds you well.<br><br>

Please find the details required to book the ticket for the upcoming trip:<br><br>

Passenger Details:<br><br>
Passenger First Name: {{doc.passenger_first_name}}<br>
Passenger Last Name: {{doc.passenger_last_name}}<br>
Passenger Gender: {{doc.passenger_gender}}<br>
Passenger Email: {{doc.owner}}<br>
<!--please add coding if booking_for=Self than upar wala otherwise ye samne wala table{{doc.passenger_details}}-->
Source: {{doc.source}}<br>
Destination: {{doc.destination}}<br>
Travel From Date: {{ doc.get_formatted("from_date")}}<br>
Time (Onward): {{doc.time_onward}}<br>
Travel To Date: {{ doc.get_formatted("to_date")}}<br>
Time (Return): {{doc.time_return}}<br>
Kindly process the booking at your earliest convenience and let me know if you require any further information.<br><br>

Thank you in advance for your assistance.