import requests
import json

url = "http://localhost:8000/api/Create_Invoice_"
for i in range(1000):
  print(i)
  payload = json.dumps({
    "payment_form": {
      "payment_form_id": 1,
      "payment_method_id": 10,
      "payment_due_date": "2022-03-22",
      "duration_measure": "0"
    },
    "invoice_lines": {
      "number": 52,
      "prefix": "FE",
      "code": 50001,
      "quanty": 1,
      "description": "Teclado",
      "price": 100,
      "tax": 19,
      "notes": "Proof of electronic billing",
      "date": "2022-03-22",
      "ipo": 0,
      "discount": 0,
      "client": 900166483,
      "company": request.session['nit_company']
    }
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)
