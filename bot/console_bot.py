import requests

API_URL = "http://localhost:8000/query"

def get_user_input():
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
        user_query = get_user_input()
        try:
            response = requests.post(API_URL, json=user_query)
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
