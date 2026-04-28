# Data-Re-visualization

# Immigrants in the U.S. — Stories Behind the Numbers

An interactive Streamlit app visualizing immigration data for 59 origin countries,
with human context behind every number.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## Deploy to Streamlit Community Cloud (free public link)

1. Push this folder to a GitHub repository (public or private)
2. Go to https://share.streamlit.io and sign in with GitHub
3. Click **New app** → select your repo → set **Main file path** to `app.py`
4. Click **Deploy** — you'll get a public URL like `https://yourname-appname.streamlit.app`

That's it. Anyone with the link can view the app — no account needed on their end.

## Features

- **World bubble map** — all 59 countries, bubbles sized by immigrant population,
  colored by pathway type (Humanitarian / Legal / Mixed). Hover for full story.
- **Filter by pathway** — isolate Humanitarian, Legal, or Mixed routes
- **Country search** — find any country and read its full migration context
- **Bar charts** — top countries and reason breakdown, both interactive
- **Slider** — control how many countries show in the ranking

## Updating data

The data is embedded directly in `app.py` in the `load_data()` function.
To update, edit the list of dictionaries — each entry has:
- `country`, `immigrants`, `pathway_type`, `reason`, `pathways`, `context`
- `lat`, `lon` (for map placement)

## For slides (Google Slides / PowerPoint)

Live embed: Insert → Iframe/embed with your Streamlit public URL
Screenshots: Run locally, filter to the pathway/region you want, screenshot
Screen record a walkthrough for a video slide
