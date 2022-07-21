import json
import re

import anitopy  # pip install anitopy

with open('./anime-fansub-relation.json', "r+", encoding="utf-8") as input_json:
    anime_fansub_relation = json.load(input_json)


def parse(filename):
    filename = re.sub(r'(\d+)v(\d+)', r'\1 v\2 ', filename)
    """
            ReplaceString(str, 0, L"&", L"and", true, true);
            ReplaceString(str, 0, L"the animation", L"", true, true);
            ReplaceString(str, 0, L"the", L"", true, true);
            ReplaceString(str, 0, L"episode", L"", true, true);
            ReplaceString(str, 0, L"oad", L"ova", true, true);
            ReplaceString(str, 0, L"oav", L"ova", true, true);
            ReplaceString(str, 0, L"specials", L"sp", true, true);
            ReplaceString(str, 0, L"special", L"sp", true, true);
            ReplaceString(str, 0, L"(tv)", L"", true, true);
    """
    # replace the anime name where found a word with the another word only if whole word is found
    filename = re.sub(r'\b&\b', 'and', filename, flags=re.IGNORECASE)
    filename = re.sub(r'\boads?\b', 'ova', filename, flags=re.IGNORECASE)
    filename = re.sub(r'\boavs?\b', 'ova', filename, flags=re.IGNORECASE)
    # filename = re.sub(r'\bthe animation\b', '', filename, flags=re.IGNORECASE)
    # filename = re.sub(r'\bthe\b', '', filename, flags=re.IGNORECASE)
    # filename = re.sub(r'\bepisode\b', '', filename, flags=re.IGNORECASE)
    filename = re.sub(r'\bspecials?\b', 'special', filename, flags=re.IGNORECASE)
    anime = anitopy.parse(filename)
    # remove everything in bracket from the title
    anime_name = re.sub(r"[(\[{].*?[)\]}]|[-:]", ' ', anime['anime_title'])
    # replace any non-alphanumeric character with space and convert to lower case
    anime_name = re.sub(r'[^A-Za-z\d]+', ' ', anime_name).lower()

    anime["anime_title"] = anime_name.strip()
    return anime


def main() -> None:
    file_name = input("Enter file name: ")
    anime = parse(file_name)

    # check if the anime already in the list
    print(f"Checking {anime['anime_title']}")
    anime_relation = anime_fansub_relation.get(anime['anime_title'], None)
    anime_id = None
    anime_season = anime.get("anime_season", None)

    # we found in database
    if anime_relation:
        # if we have the anime season in the anime relation
        # the anime season should be a string of a number without leading zero and can't be negative
        message = anime['anime_title']
        print("Found in the anime in database")
        if anime_season:
            message += f" Season {int(anime_season)}"
            anime_relation = anime_relation.get(str(int(anime_season)), None)

        # this can be change on code above, if we have the anime season in the anime relation
        # if we don't have the anime season in the anime relation, then we want to ask the user to enter the anime id
        # optional
        if anime.get("anime_type", None):
            message += f" type \"{anime['anime_type']}\""
            anime_relation = anime_relation.get(anime.get("anime_type", "").lower(), anime_relation)

        if anime.get("anime_year", 0):
            message += f" {anime['anime_year']}"
            anime_relation = anime_relation.get(anime.get("anime_year", "").lower(), anime_relation)

        if anime_relation:
            # if the anime fansub in the anime relation
            anime_id = anime_relation.get(anime.get('release_group').lower(), None)
            # else we return the default value
            if anime_id is None:
                anime_id = anime_relation.get("anilist", None)
                print(f"Anime id for \"{message}\" are {anime_id}")
            else:
                print(f"{message} from {anime.get('release_group')} are {anime_id}")
            return
        else:
            print(f"{message} season {int(anime_season)} not in database")

    # we didn't found in database
    # add the anime to the database
    if anime_id is None:
        print(f"{anime['anime_title']} not found")
        message = anime['anime_title']
        # get the anime from anime fansub relation
        # create a new one if not exist
        try:
            this_anime = anime_fansub_relation[anime['anime_title']]
        except KeyError:
            this_anime = anime_fansub_relation[anime['anime_title']] = {}

        # ask user the correct anilist id of the anime
        anime_id = int(input("Please input the anime anilist id: "))

        if anime.get("anime_season", None):
            message += f" Season {anime['anime_season']}"
            print(f"This rule only affect Season {int(anime['anime_season'])}")
            try:
                this_anime = this_anime[str(int(anime_season))]
            except KeyError:
                this_anime[str(int(anime_season))] = {}
                this_anime = this_anime[str(int(anime_season))]

        # ask user if the rule apply for global or this fansub only
        if anime.get("release_group", None):
            print("Fansub detected as " + anime["release_group"])
            fansub_only = input("Apply the rule for this fansub only? (y/n): ")
            if fansub_only.lower() == "y":
                message += f" from \"{anime['release_group']}\""
                this_anime[anime["release_group"]] = anime_id
            else:
                this_anime["anilist"] = anime_id
        else:
            this_anime["anilist"] = anime_id
        print(f"{message} has set to id: {anime_id}")


if __name__ == "__main__":
    main()
    with open('./anime-fansub-relation.json', "w", encoding="utf-8") as output_json:
        json.dump(anime_fansub_relation, output_json, sort_keys=True)
    print("Done")
    exit()
