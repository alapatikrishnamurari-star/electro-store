# Volt & Co. Electronics Store

A small Flask electronics storefront demo with product availability checks and an owner restock-alert panel.

## Features

- Product catalog across Mobiles, Laptops, Soundbars, Printers, and TVs.
- Search and category filters.
- `POST /api/check-item` returns product availability and details.
- Out-of-stock checks create a restock alert visible in the owner panel and through `GET /api/owner/notifications`.
- Responsive storefront styling with Tailwind CSS via CDN.

## Run locally

Requirements: Python 3.10 or newer.

Create and activate a virtual environment:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the dependencies and start Flask:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000/> in a browser. Keep the terminal running while using the site.

## API examples

Check an item:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/check-item -Method Post -ContentType "application/json" -Body '{"product_id":2}'
```

View owner restock alerts:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/owner/notifications
```

## Demo limitations

The catalog is mock data in `app.py`, and restock alerts are stored in memory. Alerts are cleared when the Flask server restarts. This demo does not send email or persist inventory/alerts to a database. Tailwind and the display font load from external CDNs.
