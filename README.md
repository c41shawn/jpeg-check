# jpeg-check

A free, read-only command-line tool that checks a folder of your JPEGs for the things that make your photos look like potato: a missing color profile, crushed blacks, or blown-out whites, and missing steps in the shadows (a precursor to (*gasp) banding).

It is READ-ONLY. 

**it never changes, renames, nor tags your files.** It only reads and prints a table.

Made for photographers who work dark, but real, and for those of us for whom "presets" are for car stereos and TVs, and if you also think that "recipes" belong in a kitchen/campground/cookoouts.

## What it reports

Every number is measured on the full-size image, !!!!XXXX ** no shrinking first ** XXXX!!!!  Other apps, scripts, etc. shrink first, destroying the very data meant to bemeasured.

| Column       | What it means |
|--------------|---------------|
| **PROFILE**  | The color profile embedded in the file. `none` means untagged. |
| **BLACK%**   | Percent of pixels at pure black (brightness level 0-000000). |
| **WHITE%**   | Percent of pixels at pure white (level 255-ffffff). |
| **GAPS**     | Brightness levels that are missing inside the shadow range. `0` = smooth. Higher = fewer steps = more banding risk. |
| **MEDIAN**   | The middle brightness level, 0-255 (128 is mid-grey), plus its hex grey. |
| **DARK%**    | Percent of pixels in the shadows (levels 0-63, `#000000`-`#3f3f3f`). |
| **LIGHT%**   | Percent of pixels in the highlights (levels 192-255, `#c0c0c0`-`#ffffff`). |

Hex values are brightness written as a grey (level 63 = `#3f3f3f`). They are not the photo's colors.

## Install

You probably, hopefully already have these:
You need py3 ( Python 3 ) and two free libraries:

```
pip install pillow numpy
```

Then download `jpeg_check.py`.

## Use

```
python3 jpeg_check.py /path/to/your/folder
```

Optional switches:

| Switch |  Does |
|--------|-------|
| `--subfolders` | Also check JPEGs inside folders within the folder |
| `--no-light`   | Hide the LIGHT% column |
| `--no-hex`     | Hide the hex values |

    
The table is wide, so widen your terminal window first.

Files are grouped into sets with a blank line between sets. A set is every file whose name starts the same, up to the first `-`, `_`, space or dot (so `03-siste.jpg` and `03-siste-final.jpg` sit together).

## Example output

(Made from synthetic test images, not real photos.)

```
                                                                                                       DARK%        LIGHT%
                                                                              GAPS                     levels       levels
                                                   BLACK%       WHITE%      missing       MEDIAN        0-63       192-255
                             PROFILE             pure black   pure white  shadow steps middle level   #000000-     #c0c0c0-
FILE                         (none = untagged)   (level 0)   (level 255)   0 = smooth  0-255 + hex    #3f3f3f      #ffffff
===========================================================================================================================
01-crushed.jpg               none                   5.73         0.00          0        30 #1e1e1e      97.4         0.0
01-crusher0-1.jpg            none                   5.15         0.00          0        39 #272727      80.6         0.0
01-crushiest                 none                   4.34         0.00          0        50 #323232      63.9         0.0

02-c41shawn-1500.jpg         none                   3.75         0.00          0        59 #3b3b3b      53.5         0.0
02-c41shawn-full.jpg         none                   3.12         0.00          0        70 #464646      45.6         0.0

03-siste-3000.jpg            none                   2.79         0.00          0        80 #505050      39.7         0.0
03-siste-full.jpg            none                   2.25         0.00          0        89 #595959      35.5         0.3

04-svartvatten-2903.jpg      none                   2.23         0.00          0        99 #636363      31.9         4.4
```

## What it can and can't tell you

- It measures levels, clipping, and profile. It **cannot** see blocky chunked shittified compression damage from a low JPEG quality setting, and a clean row means "no measurable problem," it does NOT mean that it "looks good."
- There is no pass/fail number nor a grade nor stars or smiley faces. Compare photos to each other and look at the outliers with your own eyes.
- **JPEG only.** PNGs and 8-bit TIFFs would likely work with a small change or 50 changes, but 16-bit TIFFs would spit wrong numbers, and raws such as DNGs are just a no-go.

## License

MIT. Free to use, copy, and change. See `LICENSE`.

Made by c41shawn - [c41shawn.com](https://c41shawn.com)
I hope this helps you out!
# ------------------------------------------------------------------
# --------------*@@@@@@@@@@@@@@@@@@@@@@*--*@@@@@@@@@@@
# --------***@@@@@@@@@@@@@@@@@@@@@@@@@--*@@@@@@@@@@@@@
# ------*@@@@@@@@@@@@@@@@@@@@@@@@@@*--*@@@@@@@@@@@@@@@
# ----*@@@@@@@@@@@@@@@@@@@@@@@@@@---*@@@@@@@@@@@@@@@@@
# ---@@@@@@@@@@@@@@@*-------------*@@@@@@@@@@@@@@@@@@@
# -*@@@@@@@@@@@*---------------**@@@@@@@@@**-@@@@@@@@@
# -@@@@@@@@@@*---------------*@@@@@@@@@@@*---@@@@@@@@@
# *@@@@@@@@@*--------------*@@@@@@@@@@@------@@@@@@@@@
# @@@@@@@@@@-------------*@@@@@@@@@@@@@@@@@--@@@@@@@@@
# @@@@@@@@@@----------**@@@@@@@@@@@@@@@@@@@--@@@@@@@@@
# @@@@@@@@@@---------@@@@@@@@@@@@@@@@@@@@@@--@@@@@@@@@
# *@@@@@@@@@*-----------------------@@@@@@@--@@@@@@@@@
# -@@@@@@@@@@@*---------------------@@@@@@@--@@@@@@@@@
# --@@@@@@@@@@@***------------------@@@@@@@--@@@@@@@@@
# ---*@@@@@@@@@@@@@@@@@@@@@@@@***---@@@@@@@--@@@@@@@@@
# -----@@@@@@@@@@@@@@@@@@@@@@@@@@*--@@@@@@@--@@@@@@@@@
# -------@@@@@@@@@@@@@@@@@@@@@@@@@--@@@@@@@--@@@@@@@*-
# ---------***@@@@@@@@@@@@@@@@@@@@--@@@@@@@--@@@@**---
# ----------------*@@@@@@@@@@@@@@*--*@@@@@@--*@*------
#
#   c41shawn  -  film photographer
#   web        c41shawn.com
#   X          @C41Shawn
#   instagram  @c41shawn_dotcom
#   github     github.com/c41shawn

