from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import joblib
import os
# Initialize FastAPI app
app = FastAPI()

# Get the absolute path to the parent of /src
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Point to ../static and ../templates
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Load model and data once
try:
    pipeline = joblib.load("../models/knn_wardrobe_pipeline.pkl")  # Make sure file exists
    data = pd.read_csv("../data/Dataset/_Wardrobe Assistant.csv")        # Replace with .pkl for better speed if needed
except Exception as e:
    raise RuntimeError(f"❌ Failed to load model or dataset: {e}")

# Define input features
feature_columns = [
    'main_category', 'Category Style', 'occasion', 'season', 'Gender',
    'fit_type', 'fabric', 'color_category'
]

# Extract dropdown values once
category_styles = data["Category Style"].dropna().unique().tolist()
main_category = data["main_category"].dropna().unique().tolist()
occasions = data["occasion"].dropna().unique().tolist()
seasons = data["season"].dropna().unique().tolist()
genders = data["Gender"].dropna().unique().tolist()
fit_types = data["fit_type"].dropna().unique().tolist()
fabrics = data["fabric"].dropna().unique().tolist()
color_categories = data["color_category"].dropna().unique().tolist()

# Prepare full dataset for KNN - Do preprocessing only ONCE
X = data[feature_columns]
try:
    transformed_X = pipeline.named_steps['preprocessor'].transform(X)
except Exception as e:
    raise RuntimeError(f"❌ Failed to preprocess X: {e}")

@app.get("/documentation", response_class=HTMLResponse)
async def documentation(request: Request):
    return templates.TemplateResponse("documentation.html", {"request": request})

@app.get("/features", response_class=HTMLResponse)
async def documentation(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})

@app.get("/howitworks", response_class=HTMLResponse)
async def how_it_works(request: Request):
    return templates.TemplateResponse("howitworks.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def how_it_works(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

# Route: Show Form
@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "category_styles": category_styles,
        "main_category": main_category,
        "occasions": occasions,
        "seasons": seasons,
        "genders": genders,
        "fit_types": fit_types,
        "fabrics": fabrics,
    })

# Route: Recommend Items
@app.post("/recommend", response_class=HTMLResponse)
async def get_recommendations(
    request: Request,
    main_category: str = Form(...),
    category_style: str = Form(...),
    occasion: str = Form(...),
    season: str = Form(...),
    Gender: str = Form(...),
    fit_type: str = Form(...),
    fabric: str = Form(...),
):
    try:
        # Prepare input
        input_data = {
            'main_category': main_category,
            'Category Style': category_style,
            'occasion': occasion,
            'season': season,
            'Gender': Gender,
            'fit_type': fit_type,
            'fabric': fabric,
            'color_category': 'Default'  
        }

        input_df = pd.DataFrame([input_data])

        # Transform input
        transformed_input = pipeline.named_steps['preprocessor'].transform(input_df)

        # Use precomputed transformed_X
        distances, indices = pipeline.named_steps['knn'].kneighbors(transformed_input)
        recommended_indices = indices[0]

        # Filter recommendations
        recommendations_df = data.iloc[recommended_indices]
        recommendations_df = recommendations_df[recommendations_df['Gender'] == Gender]

        # Prepare output
        recommendations = recommendations_df[[ 
            'product_name', 'main_category', 'Category Style', 'occasion',
            'season', 'Gender', 'fit_type', 'fabric', 'color_category',
            'Image URL-src', 'Products-href',
            'web-scraper-start-url', 'shoe_color', 'shoe_style',
            'price_pkr', 'discount', 'work_details',
        ]].dropna().to_dict(orient="records")

    except Exception as e:
        print(f"❌ Error generating recommendations: {e}")
        recommendations = []

    return templates.TemplateResponse("recommended.html", {
        "request": request,
        "recommendations": recommendations
    })

