import streamlit as st
from PIL import Image, ImageDraw
import io
import os
import sys
from datetime import datetime
from custom_styling import apply_custom_css

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import streamlit-image-coordinates for click detection
try:
    from streamlit_image_coordinates import streamlit_image_coordinates
    CLICK_DETECTION_AVAILABLE = True
except ImportError:
    CLICK_DETECTION_AVAILABLE = False

# Import our ingredient selector
try:
    from ingredient_selector import IngredientSelector, prepare_for_ml_identification
    INGREDIENT_SELECTOR_AVAILABLE = True
except ImportError:
    INGREDIENT_SELECTOR_AVAILABLE = False


def main():
    st.set_page_config(page_title="Recipe Recommender", page_icon="", layout="wide")

    # Apply custom styling
    apply_custom_css()

    st.title("Smart Recipe Recommender")
    st.markdown("*Take a photo, select ingredients, get recipe recommendations!*")

    # Main navigation in the content area (always visible)
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Take Photo", use_container_width=True):
            st.session_state.selected_mode = "Take Photo"
    with col2:
        if st.button("Select Ingredients", use_container_width=True):
            st.session_state.selected_mode = "Select Ingredients"
    with col3:
        if st.button("ML Analysis", use_container_width=True):
            st.session_state.selected_mode = "ML Analysis"
    with col4:
        if st.button("Recipe Recommendations", use_container_width=True):
            st.session_state.selected_mode = "Recipe Recommendations"
    
    # Initialize mode if not set
    if "selected_mode" not in st.session_state:
        st.session_state.selected_mode = "Take Photo"
    
    # Sidebar for navigation (backup)
    with st.sidebar:
        st.header("Navigation")
        sidebar_mode = st.selectbox(
            "Choose your mode:",
            [
                "Take Photo",
                "Select Ingredients",
                "ML Analysis",
                "Recipe Recommendations",
            ],
            index=["Take Photo", "Select Ingredients", "ML Analysis", "Recipe Recommendations"].index(st.session_state.selected_mode)
        )
        
        # Update selected mode if sidebar selection changes
        if sidebar_mode != st.session_state.selected_mode:
            st.session_state.selected_mode = sidebar_mode

        # Display warnings for missing dependencies
        if not CLICK_DETECTION_AVAILABLE:
            st.warning(
                "Click detection limited. "
                "Install streamlit-image-coordinates for full functionality."
            )
    
    # Use the selected mode
    mode = st.session_state.selected_mode
    st.markdown("---")

    if mode == "Take Photo":
        photo_capture_mode()
    elif mode == "Select Ingredients":
        ingredient_selection_mode()
    elif mode == "ML Analysis":
        ml_analysis_mode()
    elif mode == "Recipe Recommendations":
        recipe_recommendation_mode()


def photo_capture_mode():
    """Photo capture and basic processing mode."""
    st.header("Capture Your Ingredients")

    image_file = st.camera_input("Take a picture of your ingredients")

    if image_file:
        image = Image.open(image_file).convert("RGBA")

        # Store in session state
        st.session_state["current_image"] = image
        st.session_state["image_source"] = "camera"

        st.image(image, caption="Your ingredients photo", width="stretch")


def ingredient_selection_mode():
    """Interactive ingredient selection mode."""
    st.header("Select Your Ingredients")

    if (
        "current_image" not in st.session_state
        or st.session_state["current_image"] is None
    ):
        st.warning("Please take or upload a photo first!")
        return

    # Initialize session state
    if "selected_ingredients" not in st.session_state:
        st.session_state["selected_ingredients"] = []
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = (
            f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

    image = st.session_state["current_image"]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Click on Ingredients You Want To Use")

        # Create annotated image
        display_image = image.copy()
        if st.session_state["selected_ingredients"]:
            draw = ImageDraw.Draw(display_image)
            for i, (x, y) in enumerate(st.session_state["selected_ingredients"]):
                # Draw a circle on each of the selected ingredients
                radius = 20
                draw.ellipse(
                    [x - radius, y - radius, x + radius, y + radius],
                    outline="red",
                    width=3,
                )
                # Draw ingredient number inside circle
                draw.text((x - 5, y - 5), str(i + 1), fill="red")

        # Interactive image (with click detection if available)
        if CLICK_DETECTION_AVAILABLE:
            value = streamlit_image_coordinates(
                display_image, key="ingredient_selector"
            )

            if value is not None and "x" in value and "y" in value:
                new_point = (int(value["x"]), int(value["y"]))
                if new_point not in st.session_state["selected_ingredients"]:
                    st.session_state["selected_ingredients"].append(new_point)
                    st.rerun()
        else:
            # Fallback: display image and manual coordinate input
            st.image(display_image, width="stretch")
            st.info("Click detection not available. Use manual input below.")

    with col2:
        st.subheader("Controls")

        # Selection size
        selection_size = st.slider(
            "Selection Size", min_value=50, max_value=200, value=100
        )

        # Manual coordinate input (fallback)
        if not CLICK_DETECTION_AVAILABLE:
            with st.expander("Add Coordinates"):
                x_coord = st.number_input("X", 0, image.width, image.width // 2)
                y_coord = st.number_input("Y", 0, image.height, image.height // 2)
                if st.button("➕ Add Point"):
                    st.session_state["selected_ingredients"].append((x_coord, y_coord))
                    st.rerun()

        # Clear selections
        if st.button("Clear All"):
            st.session_state["selected_ingredients"] = []
            st.rerun()

        # Statistics
        st.metric("Selected Ingredients", len(st.session_state["selected_ingredients"]))

        # Extract ingredients
        if st.session_state["selected_ingredients"]:
            st.subheader("Extraction")
            
            if st.button("Extract All Ingredients", use_container_width=True):
                extract_ingredients(
                    image, st.session_state["selected_ingredients"], selection_size
                )

    # Show selected ingredients
    if st.session_state["selected_ingredients"]:
        st.subheader("Your Ingredients :")

        cols = st.columns(min(len(st.session_state["selected_ingredients"]), 4))

        for i, (x, y) in enumerate(st.session_state["selected_ingredients"]):
            with cols[i % len(cols)]:
                # Extract preview
                half_size = selection_size // 2
                left = max(0, x - half_size)
                top = max(0, y - half_size)
                right = min(image.width, x + half_size)
                bottom = min(image.height, y + half_size)

                extracted = image.crop((left, top, right, bottom))
                st.image(extracted, caption=f"Ingredient #{i+1}")


def extract_ingredients(image, coordinates, selection_size):
    """Extract and save ingredients from image."""
    if not INGREDIENT_SELECTOR_AVAILABLE:
        st.error("Ingredient selector not available!")
        return

    selector = IngredientSelector()
    session_id = st.session_state["session_id"]

    saved_ingredients = []

    with st.spinner("Extracting ingredients..."):
        for i, (x, y) in enumerate(coordinates):
            # Extract ingredient region
            half_size = selection_size // 2
            left = max(0, x - half_size)
            top = max(0, y - half_size)
            right = min(image.width, x + half_size)
            bottom = min(image.height, y + half_size)

            extracted = image.crop((left, top, right, bottom))

            # Save ingredient
            filepath = selector.save_ingredient(
                extracted, session_id, f"ingredient_{i+1}", (x, y)
            )

            saved_ingredients.append(
                {
                    "index": i + 1,
                    "coordinates": (x, y),
                    "filepath": filepath,
                    "image": extracted,
                }
            )

    st.session_state["extracted_ingredients"] = saved_ingredients
    st.success(f"Extracted and saved {len(saved_ingredients)} ingredients!")


def ml_analysis_mode():
    """ML analysis and ingredient identification mode."""
    st.header("AI Ingredient Analysis")

    if "extracted_ingredients" not in st.session_state or not st.session_state.get(
        "extracted_ingredients"
    ):
        st.warning("Please extract ingredients first!")
        st.info(
            "Go to 'Select Ingredients' mode to mark individual ingredients in your photo."
        )

        st.subheader("How AI Analysis Works:")
        st.markdown(
            """
        1. First, capture a photo and select individual ingredients
        2. The system extracts each ingredient region
        3. AI models analyze each ingredient image
        4. Get confidence scores and ingredient names
        5. Use results for recipe recommendations
        """
        )
        return

    st.info("This section will integrate your ML model for ingredient identification.")

    # Display extracted ingredients
    ingredients = st.session_state["extracted_ingredients"]

    st.subheader(f"Analyzing {len(ingredients)} Ingredients")

    cols = st.columns(min(len(ingredients), 3))

    # Simulate ML analysis
    if st.button("Analyze Ingredients (Simulated)"):
        with st.spinner("Running AI analysis..."):
            # This is where you'll integrate your actual ML model
            simulated_results = []

            for ingredient in ingredients:
                # Simulated ML prediction
                fake_predictions = [
                    "tomato",
                    "onion",
                    "carrot",
                    "potato",
                    "bell_pepper",
                    "garlic",
                    "mushroom",
                    "lettuce",
                    "cucumber",
                ]
                import random

                prediction = random.choice(fake_predictions)
                confidence = round(random.uniform(0.7, 0.95), 2)

                simulated_results.append(
                    {
                        "ingredient_id": f"ingredient_{ingredient['index']}",
                        "prediction": prediction,
                        "confidence": confidence,
                    }
                )

            st.session_state["ml_results"] = simulated_results
            st.success("Analysis complete!")

    # Display results if available
    if "ml_results" in st.session_state:
        results = st.session_state["ml_results"]

        st.subheader(" Identification Results")

        for i, result in enumerate(results):
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                if i < len(ingredients):
                    st.image(ingredients[i]["image"], width=100)

            with col2:
                st.write(f"**Ingredient #{i+1}**")
                st.write(f"Prediction: **{result['prediction']}**")
                st.progress(result["confidence"])
                st.write(f"Confidence: {result['confidence']:.1%}")

            with col3:
                # Manual correction option
                correct_name = st.text_input(f"Correct if wrong:", key=f"correct_{i}")
                if st.button("Confirm", key=f"confirm_{i}"):
                    if correct_name:
                        result["prediction"] = correct_name
                        st.success("Updated!")


def recipe_recommendation_mode():
    """Recipe recommendation based on identified ingredients."""
    st.header("Recipe Recommendations")

    if "ml_results" not in st.session_state or not st.session_state.get("ml_results"):
        st.warning("Please run ingredient analysis first!")
        st.info(
            "Complete the previous steps: Take Photo → Select Ingredients → ML Analysis"
        )

        st.subheader("Recipe Recommendation Process:")
        st.markdown(
            """
        1. Capture photo of your ingredients
        2. Select individual ingredients by clicking
        3. Run AI analysis to identify ingredients
        4. Get personalized recipe recommendations
        5. Cook delicious meals!
        """
        )
        return

    # Get identified ingredients
    identified_ingredients = [
        result["prediction"] for result in st.session_state["ml_results"]
    ]

    st.subheader("Your Identified Ingredients")
    st.write(", ".join(identified_ingredients))

    # This is where you'll integrate with your recipe dataset
    st.info("This will integrate with your recipe recommendation system.")

    # Simulated recipe recommendations
    st.subheader("Recommended Recipes")

    # Mock recipes based on ingredients
    mock_recipes = [
        {
            "name": "Mediterranean Vegetable Stir-Fry",
            "ingredients_used": identified_ingredients[:3],
            "prep_time": "20 minutes",
            "difficulty": "Easy",
            "rating": 4.5,
        },
        {
            "name": "Fresh Garden Salad",
            "ingredients_used": identified_ingredients[1:4],
            "prep_time": "10 minutes",
            "difficulty": "Very Easy",
            "rating": 4.2,
        },
        {
            "name": "Roasted Vegetable Medley",
            "ingredients_used": identified_ingredients,
            "prep_time": "35 minutes",
            "difficulty": "Medium",
            "rating": 4.7,
        },
    ]

    for recipe in mock_recipes:
        with st.expander(f"{recipe['name']} {recipe['rating']}"):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(
                    f"**Using ingredients:** {', '.join(recipe['ingredients_used'])}"
                )
                st.write(f"**Prep time:** {recipe['prep_time']}")
                st.write(f"**Difficulty:** {recipe['difficulty']}")

            with col2:
                if st.button(f"View Recipe", key=f"view_{recipe['name']}"):
                    st.info("This will open the full recipe details!")


if __name__ == "__main__":
    main()
