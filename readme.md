# Anime Fansub Relations

This repository includes anime fansub season relation data. It is used to detect the fansub seasoning number to the
correct anime.<br>

Example:

- `black clover` released from judas's fansub has `4 season` for `170 episode` whereas the anime has only `1 season`
  . `([Judas] Black Clover - S02E17 (068).mkv)`
- `to love ru` has `4 season` where the `season 2` has difference name with `season 1`, and `season 3` has difference
  name with `season 2`. `([Judas] To Love-Ru - S04E08.mkv)`

## Rule syntax

## Nodes.

Since the difference season can have same title, So we have a node for that title. <br>
All node that mark as `required` mean if it in the `anime filename` but not in the `fansub relation`, then it
returns `not detected`. <br>
In the case the `optional` node doesn't exist, then continue from the last entered node. <br>
A node can have another sub node as long the deepest node have `fansub_name` or `anilist` id. <br>

A node structure as follows:

```
Detected title // required
    Season // required
        Anime Type // optional
            Anime Year // optional
                // at least one of the following must be present:
                fansub_name, anilist // required
```

**All id are using anilist** `https://anilist.co/anime/{id}/{title}` <br>
**All key should be `lowercase, alphanumeric, without any leading or trailing spaces` string**

## Naming Rule

All anime detection should be:

- If there is any `ova, oad, oav` should be replaced with `ova`. (No plural like `ovas, oads, oavs`) <br>
- Remove anything inside bracket, square bracket, parenthesis, etc. <br>
- `{title}` should be in lowercase, alphanumeric, without any leading or trailing spaces. <br>

## Example

```json
{
  "86 eighty six": {
    "2021": {
      "judas": 131586
    }
  },
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
      "anilist": 21853
    },
    "anilist": 30671
  }
}
```

## License

This repository is in the public domain.
