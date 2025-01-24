# Bark Proxy for SmsForwarder

This project aims to improve the forwarding of notifications from Android devices to Mac, iPhone, and iPad.

## Features

- Closer to the original notification content in Android
- Support for displaying the APP icon
- Support for copying the verification code in the SMS message

## Dependencies

- [Bark](https://github.com/Finb/Bark): Integrate with the Apple push service.
- [SmsForwarder](https://github.com/pppscn/SmsForwarder): Forward messages from Android to Bark Proxy.

## Usage

1. Set up the Bark app on your device. Get the API key and encryption key (Optional) from the app.

2. Create the `.env` file by copying the `.env.example` file and filling in the necessary information.

    | Configuration Name | Description                                                  |
    |--------------------|--------------------------------------------------------------|
    | DEBUG              | `True\|False` (Optional) Enable or disable debug mode        |
    | BASE_URL           | The base URL for the Bark Proxy                              |
    | BARK_ENDPOINT      | (Optional) The endpoint for the Bark service                 |
    | BARK_APIKEY        | API key for the Bark service                                 |
    | BARK_ENCRYPT_KEY   | (Optional) Encryption key for securing data                  |
    | SIGN_SECRET        | (Optional) Secret key used for signing data                  |
    | SIGN_EXPIRE        | (Optional) Expiration time for signed data (in milliseconds) |
    | API_AUTH_KEY       | (Optional) Authentication key for accessing the API          |

3. Run the following command to start the server:

    ```bash
    docker compose up -d
    ```
   
4. Configure the forwarding channels in `SmsForwarder` app using Webhook.
    
   1. For SMS
      - Endpoint: `http://[host]:[port]/notify/sms`
      - Method: `POST`
      - Message Template:
        ```json
        {
          "from": "[from]",
          "content": "[sms]",
          "timestamp": "[timestamp]",
          "sign": "[sign]",
          "device_mark": "[device_mark]"
        }
        ```
      - Sign: {SIGN_SECRET}
      - Headers:
        - `Content-Type: application/json`
        - `Authorization`: Bearer {API_AUTH_KEY}

   2. For App Notification
      - Endpoint: `http://[host]:[port]/notify/app`
      - Method: `POST`
      - Message Template:
        ```json
        {
           "from": "[from]",
           "app": "{{app_name}}",
           "title": "{{title}}",
           "content": "{{MSG}}",
           "timestamp": "[timestamp]",
           "sign": "[sign]",
           "device_mark": "[device_mark]"
         }
         ```
      - Sign: {SIGN_SECRET}
      - Headers:
        - `Content-Type: application/json`
        - `Authorization`: Bearer {API_AUTH_KEY}
