import httpx


def main():
    with httpx.Client(base_url='http://127.0.0.1:8000') as client:
        try:
            response = client.post('/predict', json = {'text': "I bought it, but I don't use it"})

            print('POST status:', response.status_code)
            print('POST response body:', response.json())
        except httpx.ConnectError as e:
            print("Failed to connect to the server")

if __name__ == '__main__':
    main()