"""
Complete Workflow Example: From Photo to Recipe Recommendation

This script demonstrates the complete workflow of your Recipe Recommender:
1. Take/upload a photo of ingredients
2. Interactive ingredient selection (clicking on ingredients)
3. Extract and save ingredient regions
4. ML-based ingredient identification
5. Recipe recommendation based on identified ingredients

Run this with: streamlit run workflow_example.py
"""

import streamlit as st
from PIL import Image, ImageDraw
import io
import json
import os
from datetime import datetime
import random
from custom_styling import apply_custom_css

# Import your modules
from ingredient_selector import IngredientSelector, prepare_for_ml_identification, update_ml_predictions
from ml_integration import get_classifier, identify_ingredients, ingredients_to_recipe_features

# Try to import click detection
try:
    from streamlit_image_coordinates import streamlit_image_coordinates
    CLICK_DETECTION_AVAILABLE = True
except ImportError:
    CLICK_DETECTION_AVAILABLE = False

def main():
    st.set_page_config(
        page_title="Complete Recipe Recommender Workflow",
        page_icon="🍳",
        layout="wide"
    )
    
    # Apply custom styling
    apply_custom_css()
    
    st.title("Complete Recipe Recommender Workflow")
    st.markdown("*End-to-end demonstration: Photo → Ingredient Selection → ML Analysis → Recipe Recommendation*")
    
    # Initialize session state
    init_session_state()
    
    # Progress tracker
    show_progress_tracker()
    
    # Main workflow
    tab1, tab2, tab3, tab4 = st.tabs([
        "📸 1. Photo Upload", 
        "🎯 2. Ingredient Selection", 
        "🤖 3. ML Analysis", 
        "🍽️ 4. Recipe Recommendation"
    ])
    
    with tab1:
        photo_upload_step()
    
    with tab2:
        ingredient_selection_step()
    
    with tab3:
        ml_analysis_step()
    
    with tab4:
        recipe_recommendation_step()

def init_session_state():
    """Initialize session state variables."""
    defaults = {
        'workflow_step': 1,
        'current_image': None,
        'selected_coordinates': [],
        'extracted_ingredients': [],
        'ml_predictions': [],
        'session_id': f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'recipe_features': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def show_progress_tracker():
    """Show workflow progress tracker."""
    col1, col2, col3, col4 = st.columns(4)
    
    steps = [
        ("📸", "Photo", 1),
        ("🎯", "Selection", 2),
        ("🤖", "Analysis", 3),
        ("🍽️", "Recipes", 4)
    ]
    
    current_step = st.session_state.workflow_step
    
    for i, (emoji, name, step_num) in enumerate(steps):
        with [col1, col2, col3, col4][i]:
            if step_num <= current_step:
                st.success(f"{emoji} {name} ✅")
            elif step_num == current_step + 1:
                st.info(f"{emoji} {name} ⏳")
            else:
                st.empty()

def photo_upload_step():
    """Step 1: Photo upload and basic processing."""
    st.header("📸 Step 1: Upload Your Ingredients Photo")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a photo containing ingredients to analyze"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGBA")
            st.session_state.current_image = image
            st.session_state.workflow_step = max(st.session_state.workflow_step, 2)
            
            st.image(image, caption="Your ingredients photo", width="stretch")
            
            # Photo analysis info
            st.info(f"📊 Image size: {image.width}x{image.height} pixels")
        
        # Demo images option
        st.markdown("---")
        st.subheader("🎭 Or try with demo images")
        
        demo_options = [
            "None",
            "Mixed Vegetables",
            "Fresh Fruits",
            "Cooking Ingredients"
        ]
        
        demo_choice = st.selectbox("Select a demo image:", demo_options)
        
        if demo_choice != "None" and st.button(f"Load {demo_choice}"):
            # Create a demo image (for this example, we'll create colored rectangles)
            demo_image = create_demo_image(demo_choice)
            st.session_state.current_image = demo_image
            st.session_state.workflow_step = max(st.session_state.workflow_step, 2)
            st.rerun()
    
    with col2:
        st.subheader("📋 Photo Guidelines")
        st.markdown("""
        **For best results:**
        - 📷 Good lighting
        - 🔍 Clear focus
        - 📐 Ingredients well-separated
        - 🎨 Contrasting background
        - 📏 Minimum 500x500 pixels
        """)
        
        if st.session_state.current_image:
            st.success("✅ Photo loaded!")
            if st.button("➡️ Go to Ingredient Selection"):
                st.session_state.workflow_step = 2
                st.rerun()

def ingredient_selection_step():
    """Step 2: Interactive ingredient selection."""
    st.header("🎯 Step 2: Select Individual Ingredients")
    
    if not st.session_state.current_image:
        st.warning("⚠️ Please upload a photo first!")
        return
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🖱️ Click on Ingredients")
        
        image = st.session_state.current_image
        
        # Create annotated image
        display_image = create_annotated_image(image, st.session_state.selected_coordinates)
        
        # Interactive image
        if CLICK_DETECTION_AVAILABLE:
            value = streamlit_image_coordinates(
                display_image,
                key="ingredient_selector_demo"
            )
            
            if value is not None and "x" in value and "y" in value:
                new_coord = (int(value["x"]), int(value["y"]))
                if new_coord not in st.session_state.selected_coordinates:
                    st.session_state.selected_coordinates.append(new_coord)
                    st.rerun()
        else:
            st.image(display_image, width="stretch")
            st.info("💡 Click detection not available. Use manual input below.")
    
    with col2:
        st.subheader("⚙️ Selection Controls")
        
        # Selection size
        selection_size = st.slider(
            "Selection Size", 
            min_value=50, max_value=200, value=100,
            help="Size of the area to extract around each click"
        )
        
        # Manual input fallback
        if not CLICK_DETECTION_AVAILABLE:
            with st.expander("📝 Manual Input"):
                x = st.number_input("X coordinate", 0, image.width, image.width//4)
                y = st.number_input("Y coordinate", 0, image.height, image.height//4)
                if st.button("➕ Add"):
                    st.session_state.selected_coordinates.append((x, y))
                    st.rerun()
        
        # Controls
        if st.button("🗑️ Clear All Selections"):
            st.session_state.selected_coordinates = []
            st.rerun()
        
        st.metric("Selected", len(st.session_state.selected_coordinates))
        
        # Extract ingredients
        if st.session_state.selected_coordinates:
            if st.button("✂️ Extract Ingredients"):
                extract_and_save_ingredients(selection_size)
                st.session_state.workflow_step = max(st.session_state.workflow_step, 3)
                st.rerun()
    
    # Preview selected ingredients
    show_ingredient_previews(selection_size)

def ml_analysis_step():
    """Step 3: ML-based ingredient identification."""
    st.header("🤖 Step 3: AI Ingredient Analysis")
    
    if not st.session_state.extracted_ingredients:
        st.warning("⚠️ Please extract ingredients first!")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔬 Analysis Results")
        
        # Run ML analysis
        if not st.session_state.ml_predictions:
            if st.button("🚀 Run AI Analysis"):
                run_ml_analysis()
                st.rerun()
        else:
            show_ml_results()
    
    with col2:
        st.subheader("⚙️ Analysis Settings")
        
        # Model configuration
        use_mock = st.radio(
            "Analysis Mode",
            ["Demo Mode (Mock)", "Real ML Model"],
            help="Demo mode uses simulated predictions"
        )
        
        confidence_threshold = st.slider(
            "Confidence Threshold",
            0.0, 1.0, 0.5, 0.05,
            help="Minimum confidence for accepting predictions"
        )
        
        # Analysis info
        if st.session_state.extracted_ingredients:
            st.metric("Ingredients to Analyze", len(st.session_state.extracted_ingredients))
        
        if st.session_state.ml_predictions:
            high_conf = len([p for p in st.session_state.ml_predictions 
                           if p['confidence'] >= confidence_threshold])
            st.metric("High Confidence Predictions", high_conf)
            
            if st.button("➡️ Go to Recipe Recommendations"):
                st.session_state.workflow_step = max(st.session_state.workflow_step, 4)
                st.rerun()

def recipe_recommendation_step():
    """Step 4: Recipe recommendation based on identified ingredients."""
    st.header("🍽️ Step 4: Recipe Recommendations")
    
    if not st.session_state.ml_predictions:
        st.warning("⚠️ Please run ML analysis first!")
        return
    
    # Convert predictions to recipe features
    if not st.session_state.recipe_features:
        st.session_state.recipe_features = ingredients_to_recipe_features(
            st.session_state.ml_predictions
        )
    
    features = st.session_state.recipe_features
    
    # Show identified ingredients
    st.subheader("🥕 Your Identified Ingredients")
    ingredient_cols = st.columns(len(features['ingredients']))
    
    for i, ingredient in enumerate(features['ingredients']):
        with ingredient_cols[i]:
            st.metric(
                ingredient.title(), 
                f"{features['confidence_weights'][i]:.1%}",
                delta="confidence"
            )
    
    # Recipe recommendations
    st.subheader("👨‍🍳 Recommended Recipes")
    
    # Generate mock recipes based on identified ingredients
    recipes = generate_recipe_recommendations(features['ingredients'])
    
    for i, recipe in enumerate(recipes):
        with st.expander(f"🍽️ {recipe['name']} ⭐ {recipe['rating']}/5"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Ingredients used:** {', '.join(recipe['matching_ingredients'])}")
                st.markdown(f"**Prep time:** {recipe['prep_time']}")
                st.markdown(f"**Difficulty:** {recipe['difficulty']}")
                st.markdown(f"**Match score:** {recipe['match_score']:.1%}")
                
                if recipe.get('description'):
                    st.markdown(f"**Description:** {recipe['description']}")
            
            with col2:
                if st.button(f"🍴 Cook This Recipe", key=f"cook_{i}"):
                    st.success("🎉 Great choice! Enjoy cooking!")
    
    # Workflow completion
    st.success("✅ Workflow Complete! You can start over or try with a different photo.")
    
    if st.button("🔄 Start Over"):
        # Reset session state
        for key in ['current_image', 'selected_coordinates', 'extracted_ingredients', 
                   'ml_predictions', 'recipe_features']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.workflow_step = 1
        st.rerun()

# Helper functions

def create_demo_image(demo_type):
    """Create a demo image for testing."""
    width, height = 600, 400
    image = Image.new('RGB', (width, height), color='lightgray')
    draw = ImageDraw.Draw(image)
    
    colors = {
        "Mixed Vegetables": [(255, 0, 0), (0, 255, 0), (255, 165, 0), (128, 0, 128)],
        "Fresh Fruits": [(255, 0, 0), (255, 255, 0), (0, 255, 0), (255, 165, 0)],
        "Cooking Ingredients": [(139, 69, 19), (255, 255, 255), (255, 0, 0), (0, 100, 0)]
    }
    
    # Draw colored circles representing ingredients
    positions = [(150, 150), (450, 150), (150, 300), (450, 300)]
    for i, (x, y) in enumerate(positions):
        if i < len(colors[demo_type]):
            color = colors[demo_type][i]
            draw.ellipse([x-50, y-50, x+50, y+50], fill=color)
    
    return image.convert('RGBA')

def create_annotated_image(image, coordinates):
    """Create annotated version of image with selections marked."""
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    
    for i, (x, y) in enumerate(coordinates):
        # Draw circle
        radius = 20
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], outline="red", width=3)
        # Draw number
        draw.text((x-5, y-5), str(i+1), fill="red")
    
    return annotated

def extract_and_save_ingredients(selection_size):
    """Extract and save ingredient regions."""
    if not st.session_state.selected_coordinates:
        return
    
    selector = IngredientSelector()
    image = st.session_state.current_image
    
    extracted = []
    
    with st.spinner("Extracting ingredients..."):
        for i, (x, y) in enumerate(st.session_state.selected_coordinates):
            # Extract region
            half_size = selection_size // 2
            left = max(0, x - half_size)
            top = max(0, y - half_size)
            right = min(image.width, x + half_size)
            bottom = min(image.height, y + half_size)
            
            ingredient_img = image.crop((left, top, right, bottom))
            
            # Save ingredient
            filepath = selector.save_ingredient(
                ingredient_img,
                st.session_state.session_id,
                f"ingredient_{i+1}",
                (x, y)
            )
            
            extracted.append({
                'id': f"ingredient_{i+1}",
                'coordinates': (x, y),
                'image': ingredient_img,
                'filepath': filepath
            })
    
    st.session_state.extracted_ingredients = extracted
    st.success(f"✅ Extracted {len(extracted)} ingredients!")

def show_ingredient_previews(selection_size):
    """Show previews of selected ingredients."""
    if not st.session_state.selected_coordinates:
        return
    
    st.subheader("👀 Ingredient Previews")
    
    image = st.session_state.current_image
    cols = st.columns(min(len(st.session_state.selected_coordinates), 4))
    
    for i, (x, y) in enumerate(st.session_state.selected_coordinates):
        with cols[i % len(cols)]:
            # Extract preview
            half_size = selection_size // 2
            left = max(0, x - half_size)
            top = max(0, y - half_size)
            right = min(image.width, x + half_size)
            bottom = min(image.height, y + half_size)
            
            preview = image.crop((left, top, right, bottom))
            st.image(preview, caption=f"#{i+1}")

def run_ml_analysis():
    """Run ML analysis on extracted ingredients."""
    predictions = []
    
    with st.spinner("Running AI analysis..."):
        for ingredient in st.session_state.extracted_ingredients:
            # Mock ML prediction
            ingredient_classes = [
                "tomato", "onion", "carrot", "potato", "bell_pepper",
                "garlic", "mushroom", "lettuce", "cucumber", "apple"
            ]
            
            prediction = random.choice(ingredient_classes)
            confidence = random.uniform(0.6, 0.95)
            
            predictions.append({
                'ingredient_id': ingredient['id'],
                'prediction': prediction,
                'confidence': confidence,
                'coordinates': ingredient['coordinates']
            })
    
    st.session_state.ml_predictions = predictions

def show_ml_results():
    """Display ML analysis results."""
    predictions = st.session_state.ml_predictions
    
    for i, pred in enumerate(predictions):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if i < len(st.session_state.extracted_ingredients):
                st.image(st.session_state.extracted_ingredients[i]['image'], width=100)
        
        with col2:
            st.write(f"**{pred['ingredient_id']}**")
            st.write(f"Prediction: **{pred['prediction']}**")
            st.progress(pred['confidence'])
            st.write(f"Confidence: {pred['confidence']:.1%}")
        
        with col3:
            # Manual correction
            corrected = st.text_input("Correct:", key=f"correct_{i}", placeholder="Optional")
            if corrected:
                pred['prediction'] = corrected

def generate_recipe_recommendations(ingredients):
    """Generate mock recipe recommendations based on ingredients."""
    # This is where you'd integrate with your actual recipe database
    base_recipes = [
        {
            "name": "Mediterranean Vegetable Medley",
            "prep_time": "25 minutes",
            "difficulty": "Easy",
            "rating": 4.5,
            "description": "Fresh vegetables sautéed with herbs and olive oil"
        },
        {
            "name": "Garden Fresh Salad",
            "prep_time": "10 minutes",
            "difficulty": "Very Easy",
            "rating": 4.2,
            "description": "Crisp vegetables with a light vinaigrette"
        },
        {
            "name": "Roasted Vegetable Soup",
            "prep_time": "45 minutes",
            "difficulty": "Medium",
            "rating": 4.7,
            "description": "Hearty soup with roasted seasonal vegetables"
        },
        {
            "name": "Stir-Fried Vegetables",
            "prep_time": "15 minutes",
            "difficulty": "Easy",
            "rating": 4.3,
            "description": "Quick and healthy vegetable stir-fry"
        }
    ]
    
    # Add matching ingredients and scores
    for recipe in base_recipes:
        # Mock matching logic
        matching = random.sample(ingredients, min(len(ingredients), random.randint(2, 4)))
        recipe['matching_ingredients'] = matching
        recipe['match_score'] = len(matching) / len(ingredients)
    
    # Sort by match score
    return sorted(base_recipes, key=lambda x: x['match_score'], reverse=True)

if __name__ == "__main__":
    main()
