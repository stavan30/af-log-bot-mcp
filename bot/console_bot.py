import requests
from nlp_parse import extract_filters_from_query


API_URL = "http://localhost:8000/query"

def get_manual_input():
    print("\nEnter filter values (leave blank to skip):")
    username = input("Username: ").strip() or None
    resp_code_input = input("Response Code (e.g. 404): ").strip()
    resp_code = int(resp_code_input) if resp_code_input else None
    keyword = input("Keyword: ").strip() or None
    last_n_input = input("Look back (minutes, default 10): ").strip()
    last_n_minutes = int(last_n_input) if last_n_input else 10

    return {
        "username": username,
        "resp_code": resp_code,
        "keyword": keyword,
        "last_n_minutes": last_n_minutes
    }

def get_nlp_input():
    query = input("\nAsk your log query: ").strip()
    filters = extract_filters_from_query(query)
    print(f"\nExtracted filters: {filters}")
    return filters

def pretty_print_results(results):
    if not results:
        print("\nNo matching logs found.\n")
        return

    print(f"\nFound {len(results)} log(s):\n")
    for i, entry in enumerate(results, 1):
        print(f"[{i}] {entry['timestamp']} | {entry['username']} | {entry['resp_code']} | {entry['artifact']}")
        print(f"    Status: {entry['status']} | Action: {entry['action']} | Host: {entry['host']}")
        print()

def main():
    print("Artifactory Log Query Bot (CLI)")

    while True:
        mode = input("\nChoose mode: [1] Manual filters  [2] Natural language  > ").strip()
        if mode == "1":
            payload = get_manual_input()
        elif mode == "2":
            payload = get_nlp_input()
        else:
            print("Invalid option. Try again.")
            continue

        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                pretty_print_results(response.json().get("results", []))
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Failed to connect to MCP server: {e}")

        again = input("Run another query? (y/n): ").strip().lower()
        if again != 'y':
            break

if __name__ == "__main__":
    main()
