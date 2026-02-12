import requests
import pandas as pd

def buscar_oportunidades_nba(probabilidade_minima=0.75):
    url = "https://gamma-api.polymarket.com/events"
    params = {"limit": 20, "active": "true", "tag": "NBA"}

    try:
        response = requests.get(url, params=params)
        eventos = response.json()
        oportunidades = []

        for evento in eventos:
            titulo = evento.get('title')
            for mercado in evento.get('markets', []):
                if "Winner" in mercado.get('groupItemTitle', '') or "Moneyline" in mercado.get('title', ''):
                    outcomes = mercado.get('outcomePrices', [])
                    if outcomes:
                        prob_time_1 = float(outcomes[0])
                        prob_time_2 = float(outcomes[1]) if len(outcomes) > 1 else 0
                        nomes_times = mercado.get('outcomes', ["Time A", "Time B"])

                        if prob_time_1 >= probabilidade_minima:
                            oportunidades.append([titulo, nomes_times[0], prob_time_1])
                        elif prob_time_2 >= probabilidade_minima:
                            oportunidades.append([titulo, nomes_times[1], prob_time_2])

        df = pd.DataFrame(oportunidades, columns=['Jogo', 'Favorito', 'Probabilidade'])
        if not df.empty:
            print(f"\n🎯 OPORTUNIDADES NBA (>{probabilidade_minima*100}%):")
            print(df.sort_values(by='Probabilidade', ascending=False).to_string(index=False))
        else:
            print(f"\nNenhum jogo com probabilidade > {probabilidade_minima*100}% encontrado.")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    buscar_oportunidades_nba(0.75)