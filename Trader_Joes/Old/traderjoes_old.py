import requests
import json
import pandas as pd

def fetch_all_items(category_id, max_page_size):
    url = "https://www.traderjoes.com/api/graphql"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    current_page = 1
    all_items = []

    while True:
        query = """
        query SearchProducts($categoryId: String, $currentPage: Int, $pageSize: Int, $storeCode: String, $availability: String = "1", $published: String = "1") {
          products(
            filter: {store_code: {eq: $storeCode}, published: {eq: $published}, availability: {match: $availability}, category_id: {eq: $categoryId}}
            currentPage: $currentPage
            pageSize: $pageSize
          ) {
            items {
              sku
              item_title
              category_hierarchy {
                id
                name
                __typename
              }
              primary_image
              primary_image_meta {
                url
                metadata
                __typename
              }
              sales_size
              sales_uom_description
              price_range {
                minimum_price {
                  final_price {
                    currency
                    value
                    __typename
                  }
                  __typename
                }
                __typename
              }
              retail_price
              fun_tags
              item_characteristics
              __typename
            }
            total_count
            pageInfo: page_info {
              currentPage: current_page
              totalPages: total_pages
              __typename
            }
            aggregations {
              attribute_code
              label
              count
              options {
                label
                value
                count
                __typename
              }
              __typename
            }
            __typename
          }
        }
        """

        variables = {
            "categoryId": category_id,
            "currentPage": current_page,
            "pageSize": max_page_size,
            "storeCode": 546,
        }

        payload = json.dumps({"query": query, "variables": variables})

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()

            if 'errors' in data:
                print(f"API Error: {data['errors']}")
                break
            
            items = data['data']['products']['items']
            all_items.extend(items)  # Add items to the list
            
            # Get total pages from response
            total_pages = data['data']['products']['pageInfo']['totalPages']

            # Break if there are no more pages
            if current_page >= total_pages:
                break
            
            current_page += 1

        except requests.RequestException as e:
            print(f"Error fetching items: {e}")
            break

    return all_items

def save_to_csv(items, filename):
    # Convert items to a DataFrame
    df = pd.DataFrame(items)
    
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    category_id = "8"  # Set this to the desired category ID
    max_page_size = 100  # Use the maximum allowed page size
    filename = "traderjoes.csv"

    all_items = fetch_all_items(category_id, max_page_size)

    # Save the results to a CSV file
    save_to_csv(all_items, filename)

if __name__ == "__main__":
    main()
