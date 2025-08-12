# Payload App

A Django REST Framework application for managing IoT device payloads and statuses.

## Features
- Receive and store payloads from devices
- Base64 decode and validate incoming data
- Track device status (passing/failing)
- Expose RESTful API endpoints for device and payload management

## Project Structure
```
db.sqlite3
manage.py
requirements.txt
device_management/        # Django project settings and configuration
device_status/            # App for device and payload models, serializers, views, and URLs
```

## Setup
1. **Clone the repository**
2. **Create and activate a virtual environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Run the development server**
   ```sh
   python manage.py runserver
   ```

## API Overview
- **POST /api/payloads/**: Submit a new payload
- **GET /api/payloads/**: List all payloads
- **GET /api/devices/**: List all devices

### Example Payload Submission
```json
{
  "fCnt": 1,
  "device": "ABC123...",
  "data_b64": "SGVsbG8=",
  "rx_info": [{"gateway": "gw1"}],
  "tx_info": {"power": 14}
}
```

## License
MIT License
