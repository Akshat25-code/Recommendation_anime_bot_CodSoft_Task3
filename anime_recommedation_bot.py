import pandas as pd
import random
from difflib import get_close_matches

# Load the dataset
df = pd.read_csv("animes.csv")

# Preprocess
df['title'] = df['title'].fillna('')
df['genre'] = df['genre'].fillna('').str.lower()
df['synopsis'] = df['synopsis'].fillna('No synopsis available.')
df['score'] = df['score'].fillna(0)
df['link'] = df['link'].fillna('')

print("🎬 RecoBot v2: Your Personal Anime Matchmaker 💖")
print("Say 'genre', 'title', or 'surprise' to begin (or type 'exit' to quit).\n")

while True:
    user_input = input("You: ").strip().lower()

    if user_input in ['exit', 'quit', 'bye']:
        print("RecoBot: Awww 😢 OK bye-bye sweetheart! Watch something awesome 💕")
        break

    elif user_input == "genre":
        genre = input("RecoBot: What genre are you in the mood for? (e.g. action, romance, horror): ").lower()
        matches = df[df['genre'].str.contains(genre)]
        if not matches.empty:
            sampled = matches.sort_values(by='score', ascending=False).drop_duplicates(subset='title').sample(
                n=min(3, len(matches)))
            print(f"\n🎯 Top {len(sampled)} {genre.title()} Anime Recommendations:")
            for i, (_, row) in enumerate(sampled.iterrows(), 1):
                print(f"{i}. {row['title']} ({row['score']}/10)")
        else:
            print("RecoBot: Hmm... I couldn't find that genre 😞 Try something else!")

    elif user_input == "title":
        title = input("RecoBot: Tell me an anime you liked 🧐: ")
        close_titles = get_close_matches(title, df['title'].tolist(), n=1, cutoff=0.5)
        if close_titles:
            selected = close_titles[0]
            genre = df[df['title'] == selected]['genre'].values[0]
            print(f"\n💡 Based on '{selected}', here are 3 similar {genre.title()} picks:")
            matches = df[
                (df['genre'].str.contains(genre.lower())) &
                (df['title'] != selected)
                ].drop_duplicates(subset='title').sort_values(by='score', ascending=False).sample(n=3)
            for i, (_, row) in enumerate(matches.iterrows(), 1):
                print(f"{i}. {row['title']} ({row['score']}/10)")
        else:
            print("RecoBot: Hmm... I couldn’t find that title. Try a simpler name!")

    elif user_input == "surprise":
        print("🎁 Here's a surprise anime for you, no thinking required! 🎉")
        surprise = df.sample(1).iloc[0]
        print(f"🎬 {surprise['title']} ({surprise['score']}/10)")
        print(f"📖 {surprise['synopsis'][:180]}...")
        print(f"🔗 {surprise['link']}\n")

    else:
        print("RecoBot: Oops! Type 'genre', 'title', or 'surprise' to get started 💬")