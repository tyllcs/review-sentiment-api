import httpx2


def main():
    with httpx2.Client(http1=False, http2=True, base_url='http://127.0.0.1:8000') as client:
        try:
            response = client.post('/predict', json = {'text': "I bought it, but I don't use it"})

            print('POST status:', response.status_code)
            print('POST response body:', response.json())
            print(response.http_version)
        except httpx2.ConnectError as e:
            print("Failed to connect to the server")

if __name__ == '__main__':
    main()