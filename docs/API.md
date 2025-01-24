# API Documentation

## Endpoints

### `GET /ping`

**Description:**  
Health check endpoint to verify if the service is running.

**Response:**
- `200 OK`: Returns "pong".

### `GET /apps`

**Description:**  
Retrieve all registered apps.

**Response:**
- `200 OK`: Returns a JSON array of all apps.

### `POST /apps`

**Description:**  
Register a new app with its icon.

**Request Body:**
- `name` (string): The name of the app.
- `package` (string): The package name of the app.
- `icon` (string): The URL of the app's icon.

**Response:**
- `200 OK`: Returns a success status.

### `POST /notify/app`

**Description:**  
Send a notification for an app.

**Request Body:**
- `title` (string): The title of the notification.
- `content` (string): The content of the notification.
- `from` (string): The source of the notification.
- `app` (string): The name of the app (optional).

**Response:**
- `200 OK`: Returns a success status.

### `POST /notify/sms`

**Description:**  
Send a notification for an SMS message.

**Request Body:**
- `from` (string): The sender of the SMS.
- `content` (string): The content of the SMS.

**Response:**
- `200 OK`: Returns a success status.

## Middleware

### `verify_signature`

**Description:**  
Verifies the signature of requests to `/notify/` endpoints.

### `log_request`

**Description:**  
Logs all incoming requests except to the `/ping` endpoint.

### `auth`

**Description:**  
Authenticates requests to `/apps` and `/notify` endpoints using the `Authorization` header.
