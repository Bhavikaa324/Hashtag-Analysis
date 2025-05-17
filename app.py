
from hashtag_analysis import (
    load_data, filter_df_by_country_language,
    get_top_words_trends, get_top_cooccurrences,
    get_top_likes_shares, get_countrywise_counts, get_available_filters
)

def main():
    data_path = "C:/Users/puppa/Downloads/tweets.csv"
    df = load_data(data_path)

    filters = get_available_filters(df)
    print("Available Countries:", filters['countries'])
    print("Available Languages:", filters['languages'])
    print("Type 'all' to skip filtering.")

    while True:
        country = input("Enter country to filter (or 'all'): ").strip()
        if country.lower() == 'all':
            country = None
        elif country not in filters['countries']:
            print("Invalid country. Try again.")
            continue

        language = input("Enter language to filter (or 'all'): ").strip()
        if language.lower() == 'all':
            language = None
        elif language not in filters['languages']:
            print("Invalid language. Try again.")
            continue

        filtered_df = filter_df_by_country_language(df, country, language)
        print(f"\nFiltered dataset has {len(filtered_df)} records.")

        # Show word trends
        data, top_words = get_top_words_trends(filtered_df)
        if data.empty:
            print("No data for word trends.")
        else:
            print("\nTop words trends over dates:")
            print(data[top_words])

        # Show co-occurrence
        cooccurrences = get_top_cooccurrences(filtered_df)
        print("\nTop co-occurring word pairs:")
        for pair, count in cooccurrences:
            print(f"{pair[0]} & {pair[1]} : {count}")

        # Show top likes and shares
        top_engagement = get_top_likes_shares(filtered_df)
        print("\nTop words by likes + shares:")
        for item in top_engagement:
            print(f"{item['word']}: {item['engagement']}")

        # Show countrywise counts (only if no country filter)
        if not country:
            country_counts = get_countrywise_counts(filtered_df)
            print("\nPosts per country:")
            for item in country_counts:
                print(f"{item['country']}: {item['count']}")

        print("\n--- Analysis done ---\n")

        cont = input("Do you want to analyze another filter? (yes/no): ").strip().lower()
        if cont != 'yes':
            break

if __name__ == "__main__":
    main()
