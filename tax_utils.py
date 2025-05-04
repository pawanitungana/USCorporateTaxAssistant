import requests
import pandas as pd
from bs4 import BeautifulSoup
from openai import OpenAI

# Fetch and parse tax data
def fetch_tax_data():
    url = 'https://taxfoundation.org/data/all/state/state-corporate-income-tax-rates-brackets/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        state = cols[0].text.strip()
        rate = cols[1].text.strip()
        signage = cols[2].text.strip()
        bracket = cols[3].text.strip()
        data.append([state, rate, signage, bracket])

    df = pd.DataFrame(data, columns=['State', 'Rate', 'Signage', 'Bracket'])
    df.to_csv("us_corporate_tax_rates.csv", index=False)
    return df
    #print(df)
    #return True

# if __name__ == "__main__":
#     fetch_tax_data()




# Build OpenAI prompt system role content
def build_system_prompt(df):
    df_str = df.to_string()
    system_prompt = (
        "You are a tax assistant for U.S. corporations. "
        "Explain the corporate income tax system in {state}. Include - Corporate tax rate - Any minimum or franchise taxes "
        "- Who must file - Any state-specific exemptions or thresholds. Explain it simply for a small business owner. "
        "This data frame consists of all the tax slab rates for each state. Use this information as needful. "
        "If user doesn't input the state, then ask for their state.\n\n" + df_str
    )
    return system_prompt
   #print(system_prompt)
   #return True

#
# Query OpenAI
def get_tax_response(user_input, system_prompt, api_key):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return completion.choices[0].message.content

# if __name__ == "__main__":
#     var=fetch_tax_data()
#     pt=build_system_prompt(var)
#     get_tax_response('I am from Alaska .My income is $149,000.what is my tax liability?',pt,'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')