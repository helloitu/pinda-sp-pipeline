import subprocess
import json
import os
import pandas as pd
import time

API_KEY = os.environ.get("API_TOKEN", "YOUR_API_KEY")
BASE_URL = "https://www.pindamonhangaba.sp.leg.br/jsonweb/web-aplicativo.php"

def get_api_data(service, params=None):
    """
    Fetches data from the Pindamonhangaba API using curl.
    """
    url = f"{BASE_URL}?keysoft={API_KEY}&call={service}"
    if params:
        for key, value in params.items():
            url += f"&{key}={value}"

    all_data = []
    page = 1
    previous_page_content = None
    while True:
        time.sleep(3)
        paginated_url = f"{url}&pagina={page}"
        print(f"Fetching data from: {paginated_url}")
        try:
            result = subprocess.run(['curl', '-s', paginated_url], capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)

            if not data or (isinstance(data, dict) and not data.get('registros')):
                break

            records = []
            if isinstance(data, dict) and data.get('registros'):
                records = data['registros']
            elif isinstance(data, list):
                records = data

            if not records:
                break

            current_page_content = json.dumps(records)
            if current_page_content == previous_page_content:
                break

            all_data.extend(records)
            previous_page_content = current_page_content
            page += 1
        except subprocess.CalledProcessError as e:
            print(f"Error fetching data from {paginated_url}: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {paginated_url}: {e}")
            break

    return all_data

def save_to_csv(data, filename):
    """
    Saves a list of dictionaries to a CSV file.
    """
    if not data:
        print(f"No data to save for {filename}")
        return
    df = pd.DataFrame(data)
    df.to_csv(f"seeds/{filename}", index=False)

def main():
    """
    Main function to fetch data from all services and save it to CSV files.
    """
    services = [
        "vereadores",
        "proposicoes",
        "legislacoes",
        "bairros",
        "pautas",
        "noticias",
        "tvcamara",
    ]

    for service in services:
        print(f"Fetching data for {service}...")
        try:
            if service == "proposicoes":
                tipos_proposicoes = get_api_data("proposicoes")
                if tipos_proposicoes:
                    for tipo in tipos_proposicoes:
                        proposicoes_por_tipo = get_api_data("proposicoes", params={"tipo": tipo['contract']})
                        save_to_csv(proposicoes_por_tipo, f"proposicoes_{tipo['contract']}.csv")
            elif service == "legislacoes":
                tipos_legislacoes = get_api_data("legislacoes")
                if tipos_legislacoes:
                    for tipo in tipos_legislacoes:
                        legislacoes_por_tipo = get_api_data("legislacoes", params={"tipo": tipo['contract']})
                        save_to_csv(legislacoes_por_tipo, f"legislacoes_{tipo['contract']}.csv")
            else:
                data = get_api_data(service)
                save_to_csv(data, f"{service}.csv")
            print(f"Data for {service} saved successfully.")
        except Exception as e:
            print(f"Error fetching data for {service}: {e}")

if __name__ == "__main__":
    main()
