import pandas as pd
import re

def categorize_colors(df: pd.DataFrame, column_name: str = "color") -> pd.DataFrame:
    COLOR_FAMILIES = {
        "Black & Greys": [
            r"\bblack\b", r"\bdark black\b", r"\bmatte black\b",
            r"\bgrey\b", r"\bgray\b", r"\bcharcoal\b", r"\bash grey\b",
            r"\bsteel grey\b", r"\biy? icy grey\b", r"\bmidnight dark grey\b"
        ],
        "White & Off‑Whites": [
            r"\bwhite\b", r"\bpure white\b", r"\boff white\b", r"\bivory\b",
            r"\bcream\b", r"\bvanila\b", r"\bpure cream\b", r"\bbeige\b",
            r"\boat beige\b"
        ],
        "Blues": [
            r"\bnavy\b", r"\bmidnight blue\b", r"\broyal blue\b",
            r"\b(prussian|powder|sky|baby|azure|sea|pastel dark) blue\b",
            r"\bteal blue\b", r"\bpeacock blue\b", r"\bturquoise blue\b",
            r"\baqua blue\b", r"\bfirozi\b", r"\bink blue\b"
        ],
        "Greens": [
            r"\bgreen\b", r"\bdark green\b", r"\bolive\b", r"\bpistachio\b",
            r"\bmint\b", r"\bseafoam\b", r"\bsage\b", r"\bfern\b",
            r"\bapple\b", r"\bliril\b", r"\bparrot\b", r"\bme(h|hn)di\b",
            r"\bmoss\b", r"\bceladon\b", r"\bcastleton\b", r"\bpeacock green\b",
            r"\bemerald\b", r"\bpure green\b", r"\bbright green\b"
        ],
        "Reds": [
            r"\bred\b", r"\bdeep red\b", r"\bcherry red\b", r"\bruby\b",
            r"\btomato\b", r"\bchilly red\b", r"\bbrick red\b", r"\bwine\b",
            r"\bmaroon\b", r"\bburgundy\b", r"\brani\b"
        ],
        "Purples & Mauves": [
            r"\bpurple\b", r"\bplum\b", r"\bmauve\b", r"\blavender\b",
            r"\bviolet\b", r"\bmagenta\b", r"\btyrian\b"
        ],
        "Pinks": [
            r"\bpink\b", r"\bpale pink\b", r"\bdusty pink\b", r"\bbaby pink\b",
            r"\bblush pink\b", r"\bcoral pink\b", r"\bbubble gum\b",
            r"\brani pink\b", r"\btaffy pink\b"
        ],
        "Yellows": [
            r"\byellow\b", r"\bmustard\b", r"\bturmeric\b", r"\bpale yellow\b",
            r"\blight yellow\b", r"\bpure yellow\b", r"\btrombone yellow\b",
            r"\blemon yellow\b", r"\byellow beige\b"
        ],
        "Oranges": [
            r"\borange\b", r"\blight orange\b", r"\bpure orange\b",
            r"\bsalmon\b", r"\bcoral\b", r"\bcarrot\b", r"\brust orange\b",
            r"\btomato red\b", r"\bdusty orange\b", r"\bgradient.*orange\b"
        ],
        "Browns": [
            r"\bbrown\b", r"\bcoffee\b", r"\bchik+k?o?\b", r"\bcopper\b",
            r"\bcinnamon\b", r"\bchocolate\b"
        ],
        "Golds & Metallics": [
            r"\bgold\b", r"\bpure gold\b", r"\bgolden\b", r"\bsilver\b"
        ],
        "Multi / Mixed & Others": []  # fallback
    }

    COMPILED = {
        family: re.compile("|".join(patterns), flags=re.IGNORECASE)
        if patterns else None
        for family, patterns in COLOR_FAMILIES.items()
    }

    def assign_family(color_str: str) -> str:
        if pd.isna(color_str):
            return "Unknown"
        s = color_str.lower().strip()
        for family, regex in COMPILED.items():
            if regex and regex.search(s):
                return family
        return "Multi / Mixed & Others"

    df = df.copy()
    df[column_name + "_category"] = df[column_name].apply(assign_family)
    return df


def Sort_column(df: pd.DataFrame) -> pd.DataFrame:
    column_order = [
        "product_name", "main_category", "Category Style", "categorize_outfit", "occasion", "season",
        "Gender", "fit_type", "fabric", "work_details",
        "color_category", "shoe_color", "shoe_style",
        "price_pkr", "discount", "Image URL-src", "Products-href", "web-scraper-start-url"
    ]
    
    return df[column_order]
