# Maintenance tools

`build_library.py` is the reproducible source-of-truth builder for the generated logo/icon folders and search indexes.

The GitHub Actions workflow runs it automatically when the builder/workflow changes and on the monthly schedule. It downloads current upstream vector collections, generates the standard seven SVG variants, overlays selected product-specific vectors, and rebuilds `Icon_Index.json` / `Icon_Index.csv`.

For a local rebuild:

```bash
python -m pip install cairosvg
python tools/build_library.py
```

Do not hand-edit thousands of generated files when the change belongs in source mappings, aliases, naming, or variant-generation logic.
