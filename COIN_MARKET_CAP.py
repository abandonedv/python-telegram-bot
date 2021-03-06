def price_of_crypto(crypto, currency):
    try:
        crypto = crypto.lower()
        currency = currency.upper()

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
            'slug': f'{crypto}',
            'convert': f'{currency}'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '881ca7de-a5a6-4971-885a-3d800be10159',
        }

        session = requests.Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        with open("updates.json", "w") as file:
            json.dump(response.json(), file, indent=2, ensure_ascii=False)
        data = json.loads(response.text)
        for k in data["data"]:
            id = k
            print(k)
        price = data["data"][f"{id}"]["quote"][f'{currency}']["price"]
        return price
    except Exception as e:
        print(e)