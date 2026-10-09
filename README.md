# DnA Techy Master Logo & Icon Library

[![Build icon library](https://github.com/dnatechy/Master-Logo-Icon-Library/actions/workflows/build-library.yml/badge.svg)](https://github.com/dnatechy/Master-Logo-Icon-Library/actions/workflows/build-library.yml)

A large, searchable SVG library for **PowerPoint, dashboards, reports, documents, websites and UI design**. It combines broad brand coverage with general-purpose interface icons and consistent presentation-ready variants.

> **DnA Techy public product.** The library is free to browse and reuse subject to upstream licenses and each brand owner's trademark/brand-usage rules.

## Library at a glance

Current generated/indexed snapshot:

| Collection | Indexed assets |
| --- | ---: |
| Brand logos | 27,090 |
| General icons — Solid | 14,007 |
| General icons — Regular | 1,911 |
| **Total** | **43,008** |

The exact count can grow as upstream collections are refreshed. `BUILD_SUMMARY.json` contains the current generated totals.

## What is included

- **Brand logos** — broad company and product coverage, with search-friendly aliases such as `power-bi`, `powerbi`, `microsoft-power-bi`, `aws`, `gcp`, etc.
- **General icons** — solid and regular icon sets for analytics, business, technology, navigation, communication, operations and more.
- **Selected product vectors** — product-specific sources for Power BI, Power Automate, Power Query, Power Apps, Dataverse, Power Pages, Google Apps Script, Python and other curated items when a stable source is available.
- **Seven SVG variants** for generated icons:
  1. `00_Raw_Source`
  2. `01_Transparent_Black`
  3. `02_Transparent_White`
  4. `03_Circle_Blue`
  5. `04_Circle_Dark`
  6. `05_Rounded_Square_Blue`
  7. `06_Rounded_Square_Dark`
- **Search UI** — `Search_Icons.html`
- **CSV + JSON index** — generated from the real library files.

## Quick start

1. Download or clone this repository.
2. Open `Search_Icons.html` in **Microsoft Edge or Google Chrome**.
3. Click **Connect local folder** and select the repository folder.
4. Search for `Power BI`, `Power Automate`, `AWS`, `GCP`, `Google`, `database`, `chart`, `location`, `automation`, etc.
5. Insert the SVG directly into PowerPoint or your design tool.

The local search mode scans the real folder. If new icons are added later, reload/refresh and they become searchable without rebuilding the HTML manually.

## Search-friendly filenames

Examples:

```text
power-bi__logo__raw-source.svg
powerbi__logo__circle-blue.svg
microsoft-power-automate__logo__square-dark.svg
gcp__logo__raw-source.svg
database__icon__transparent-black.svg
chart-line__icon__circle-blue.svg
```

## Folder structure

```text
Brand_Logos/
  00_Raw_Source/
  01_Transparent_Black/
  02_Transparent_White/
  03_Circle_Blue/
  04_Circle_Dark/
  05_Rounded_Square_Blue/
  06_Rounded_Square_Dark/

General_Icons_Solid/
  ...same seven variants...

General_Icons_Regular/
  ...same seven variants...

Featured_Color_Logos/
  SVG/
  PNG_2048/

Search_Icons.html
Icon_Index.json
Icon_Index.csv
BUILD_SUMMARY.json
```

## PowerPoint usage

SVG is recommended because it stays sharp at any size. In recent PowerPoint versions, compatible single-colour SVGs can also be recoloured using **Graphics Fill**.

For third-party brand marks, use the raw/original version when brand fidelity is important and follow the brand owner's current usage rules.

## Automatic updates

This repository includes a reproducible builder and GitHub Actions workflow. It refreshes upstream collections, regenerates the seven variants, rebuilds the indexes and commits only user-facing generated assets.

The build also runs automatically every month so the library can grow as upstream collections change.

Build logic: [`tools/build_library.py`](tools/build_library.py)

## Sources and attribution

The library uses or references third-party sources including:

- [Simple Icons](https://simpleicons.org/) — broad brand SVG collection.
- [Font Awesome Free](https://fontawesome.com/) — general and brand icons.
- [Microsoft Power BI Icons](https://github.com/microsoft/PowerBI-Icons) — selected Microsoft Power Platform / Power BI vectors.
- [Google Apps Script](https://developers.google.com/apps-script) product artwork.
- [Python Software Foundation logo resources](https://www.python.org/community/logos/).

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for licensing and trademark notes.

## Important trademark note

**DnA Techy does not own third-party brand names or logos and is not affiliated with, endorsed by, or sponsored by the companies represented in this library.** Brand marks remain the property of their respective owners.

Raw brand artwork should be used according to the relevant owner's brand guidelines. Monochrome, circle and square variants are convenience derivatives for presentation/design workflows and may **not** be permitted for every brand or every external/commercial use. When brand fidelity matters, use the raw/original asset and follow the owner's current guidelines.

## Contributing

Requests for missing logos, better aliases, corrected sources and search improvements are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request.

## License

DnA Techy-authored **code, search UI and original documentation** are licensed under the MIT License. Third-party icon/logo assets are **not relicensed by DnA Techy**; their upstream licenses and trademark restrictions continue to apply. See [`LICENSE`](LICENSE) and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Project documents

- [`CHANGELOG.md`](CHANGELOG.md) — release history
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution guide
- [`SECURITY.md`](SECURITY.md) — security reporting
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — community expectations

---

**Maintained by [DnA Techy](https://github.com/dnatechy)**
