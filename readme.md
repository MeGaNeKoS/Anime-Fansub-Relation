# Anime Fansub Relations

This repository includes anime fansub season relation data. It is used to detect the fansub seasoning number to the correct anime.<br>

Example:
- `black clover` released from judas's fansub has `4 season` for `170 episode` whereas the anime has only `1 season`. `([Judas] Black Clover - S02E17 (068).mkv)`
- `to love ru` has `4 season` where the `season 2` has difference name with `season 1`, and `season 3` has difference name with `season 2`. `([Judas] To Love-Ru - S04E08.mkv)`


## Rule syntax
### json resource representation
```
{
  "title": { // required, alphanumeric, lowercase
    "season": { // optional, number
      "fansub_name": <anilist_id: number>, // optional
      "anilist": <anilist_id: number>, // default id if no fansub specified
    },
    "fansub_name": <anilist_id: number>, // optional
    "anilist": <anilist_id: number>, // default id if no fansub specified
  }
}
```
**All id are using anilist** `https://anilist.co/anime/{id}/{title}`

## Example
```json
{
    "to love ru": {
        "1": {
            "anilist": 30671
        },
        "2": {
            "anilist": 9181
        },
        "3": {
            "anilist": 13663
        },
        "4": {
            "judas": 21853,
            "anilist": 21853
        },
        "anilist": 30671
    }
}
```

## License
This repository is in the public domain.
