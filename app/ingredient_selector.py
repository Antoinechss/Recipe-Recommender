import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import io
import os
import json
from typing import List, Tuple, Dict, Optional
from datetime import datetime
from custom_styling import apply_custom_css


class IngredientSelector:
    """
    Interactive ingredient selection system for Streamlit.
    Allows users to click on ingredients in photos to extract and identify them.
    """
    
    def __init__(self):
        self.ingredients_dir = "extracted_ingredients"
        self.metadata_file = "ingredients_metadata.json"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.ingredients_dir, exist_ok=True)
    
    def load_metadata(self) -> Dict:
        """Load ingredient metadata from file."""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading metadata: {e}")
        return {"sessions": []}
    
    def save_metadata(self, metadata: Dict):
        """Save ingredient metadata to file."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            st.error(f"Error saving metadata: {e}")
    
    def process_click_coordinates(self, image: Image.Image, click_coords: Tuple[int, int], 
                                 selection_size: int = 100) -> Image.Image:
        """
        Extract a region around the clicked coordinates.
        
        Args:
            image: The original image
            click_coords: (x, y) coordinates of the click
            selection_size: Size of the square to extract around the click
            
        Returns:
            Extracted image region
        """
        x, y = click_coords
        half_size = selection_size // 2
        
        # Calculate bounding box, ensuring it's within image bounds
        left = max(0, x - half_size)
        top = max(0, y - half_size)
        right = min(image.width, x + half_size)
        bottom = min(image.height, y + half_size)
        
        # Extract the region
        extracted = image.crop((left, top, right, bottom))
        return extracted
    
    def save_ingredient(self, image: Image.Image, session_id: str, 
                       ingredient_id: str, click_coords: Tuple[int, int]) -> str:
        """
        Save an extracted ingredient image.
        
        Args:
            image: The extracted ingredient image
            session_id: Unique session identifier
            ingredient_id: Unique ingredient identifier
            click_coords: Original click coordinates
            
        Returns:
            Path to saved image
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{session_id}_{ingredient_id}_{timestamp}.png"
        filepath = os.path.join(self.ingredients_dir, filename)
        
        # Save original extracted image
        image.save(filepath)
        
        # Update metadata
        metadata = self.load_metadata()
        ingredient_data = {
            "id": ingredient_id,
            "session_id": session_id,
            "timestamp": timestamp,
            "click_coordinates": click_coords,
            "image_path": filepath,
            "ml_prediction": None,  # To be filled by ML script later
            "confidence": None
        }
        
        # Find or create session
        session_found = False
        for session in metadata["sessions"]:
            if session["session_id"] == session_id:
                session["ingredients"].append(ingredient_data)
                session_found = True
                break
        
        if not session_found:
            metadata["sessions"].append({
                "session_id": session_id,
                "created_at": timestamp,
                "ingredients": [ingredient_data]
            })
        
        self.save_metadata(metadata)
        return filepath
    
    def get_session_ingredients(self, session_id: str) -> List[Dict]:
        """Get all ingredients for a specific session."""
        metadata = self.load_metadata()
        for session in metadata["sessions"]:
            if session["session_id"] == session_id:
                return session["ingredients"]
        return []
    
    def create_annotated_image(self, image: Image.Image, 
                              selected_points: List[Tuple[int, int]], 
                              selection_size: int = 100) -> Image.Image:
        """
        Create an annotated version of the image showing selected regions.
        
        Args:
            image: Original image
            selected_points: List of (x, y) coordinates
            selection_size: Size of selection squares
            
        Returns:
            Annotated image
        """
        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)
        
        half_size = selection_size // 2
        
        for i, (x, y) in enumerate(selected_points):
            # Draw selection rectangle
            left = x - half_size
            top = y - half_size
            right = x + half_size
            bottom = y + half_size
            
            # Draw rectangle
            draw.rectangle([left, top, right, bottom], 
                         outline="red", width=3)
            
            # Draw number
            draw.text((x-10, y-10), str(i+1), fill="red")
        
        return annotated

def display_ingredient_selector():
    """
    Main function to display the ingredient selection interface in Streamlit.
    """
    # Apply custom styling
    apply_custom_css()
    
    st.header("Interactive Ingredient Selector")
    
    # Initialize session state
    if 'selector' not in st.session_state:
        st.session_state.selector = IngredientSelector()
    if 'session_id' not in st.session_state:
        st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if 'selected_points' not in st.session_state:
        st.session_state.selected_points = []
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    
    selector = st.session_state.selector
    
    # Configuration
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("⚙️ Settings")
        selection_size = st.slider(
            "Selection Size", 
            min_value=50, max_value=200, value=100, step=10,
            help="Size of the area to extract around each click"
        )
        
        # Session info
        st.subheader("📊 Session Info")
        st.text(f"Session ID: {st.session_state.session_id}")
        st.text(f"Selected ingredients: {len(st.session_state.selected_points)}")
        
        if st.button("🔄 Start New Session"):
            st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.selected_points = []
            st.rerun()
        
        if st.button("🗑️ Clear Selections"):
            st.session_state.selected_points = []
            st.rerun()
    
    with col1:
        # Image input
        uploaded_file = st.file_uploader(
            "Upload your ingredient photo", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a photo containing ingredients to select from"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGBA")
            st.session_state.current_image = image
            
            # Display image with selections
            if st.session_state.selected_points:
                annotated_image = selector.create_annotated_image(
                    image, st.session_state.selected_points, selection_size
                )
                st.image(annotated_image, caption="Click on ingredients to select them", 
                        use_container_width=True)
            else:
                st.image(image, caption="Click on ingredients to select them", 
                        use_container_width=True)
            
            # Note: In a real Streamlit app, we'd need to use a component like streamlit-image-coordinates
            # for actual click detection. For now, we'll simulate with input boxes.
            
            st.info("💡 **Note**: Click coordinates will be captured here. "
                   "In production, this would use an interactive image component.")
            
            # Simulated click input (replace with actual image click component)
            with st.expander("🖱️ Add Click Coordinates (Simulation)"):
                col_x, col_y, col_add = st.columns([1, 1, 1])
                with col_x:
                    click_x = st.number_input("X coordinate", min_value=0, max_value=image.width, value=image.width//2)
                with col_y:
                    click_y = st.number_input("Y coordinate", min_value=0, max_value=image.height, value=image.height//2)
                with col_add:
                    if st.button("➕ Add Point"):
                        st.session_state.selected_points.append((click_x, click_y))
                        st.rerun()
    
    # Process selected ingredients
    if st.session_state.selected_points and st.session_state.current_image:
        st.subheader("🎯 Selected Ingredients")
        
        cols = st.columns(min(len(st.session_state.selected_points), 4))
        
        for i, (x, y) in enumerate(st.session_state.selected_points):
            with cols[i % len(cols)]:
                # Extract ingredient
                extracted = selector.process_click_coordinates(
                    st.session_state.current_image, (x, y), selection_size
                )
                
                st.image(extracted, caption=f"Ingredient #{i+1}")
                st.text(f"Position: ({x}, {y})")
                
                # Save button
                if st.button(f"💾 Save #{i+1}", key=f"save_{i}"):
                    filepath = selector.save_ingredient(
                        extracted,
                        st.session_state.session_id,
                        f"ingredient_{i+1}",
                        (x, y),
                        auto_bg_removal
                    )
                    st.success(f"✅ Saved to {filepath}")
                    
                    # TODO: Here you would call your ML identification function
                    st.info("🤖 Ready for ML identification (to be implemented)")
        
        # Batch processing
        st.subheader("⚡ Batch Processing")
        if st.button("💾 Save All Ingredients"):
            saved_paths = []
            for i, (x, y) in enumerate(st.session_state.selected_points):
                extracted = selector.process_click_coordinates(
                    st.session_state.current_image, (x, y), selection_size
                )
                filepath = selector.save_ingredient(
                    extracted,
                    st.session_state.session_id,
                    f"ingredient_{i+1}",
                    (x, y),
                    auto_bg_removal
                )
                saved_paths.append(filepath)
            
            st.success(f"✅ Saved {len(saved_paths)} ingredients!")
            
            # TODO: Call ML batch identification
            st.info("🤖 Ready for batch ML identification (to be implemented)")
    
    # Display session history
    if st.checkbox("📜 Show Session History"):
        metadata = selector.load_metadata()
        if metadata["sessions"]:
            for session in metadata["sessions"]:
                with st.expander(f"Session: {session['session_id']} ({len(session['ingredients'])} ingredients)"):
                    for ingredient in session["ingredients"]:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            if os.path.exists(ingredient["image_path"]):
                                img = Image.open(ingredient["image_path"])
                                st.image(img, width=100)
                        with col2:
                            st.text(f"ID: {ingredient['id']}")
                            st.text(f"Click: {ingredient['click_coordinates']}")
                            st.text(f"Prediction: {ingredient['ml_prediction'] or 'Not analyzed'}")


# Integration function for the ML pipeline
def prepare_for_ml_identification(session_id: str) -> List[Dict]:
    """
    Prepare extracted ingredients for ML identification.
    
    Args:
        session_id: Session to process
        
    Returns:
        List of ingredient data ready for ML processing
    """
    selector = IngredientSelector()
    ingredients = selector.get_session_ingredients(session_id)
    
    ml_ready_data = []
    for ingredient in ingredients:
        if os.path.exists(ingredient["image_path"]):
            # Load image
            image = Image.open(ingredient["image_path"])
            
            # Convert to format expected by ML model
            ml_ready_data.append({
                "id": ingredient["id"],
                "image": image,
                "image_path": ingredient["image_path"],
                "background_removed_path": ingredient["background_removed_path"],
                "click_coordinates": ingredient["click_coordinates"],
                "metadata": ingredient
            })
    
    return ml_ready_data

def update_ml_predictions(session_id: str, predictions: List[Dict]):
    """
    Update metadata with ML predictions.
    
    Args:
        session_id: Session ID
        predictions: List of predictions with format:
                   [{"ingredient_id": "ingredient_1", "prediction": "tomato", "confidence": 0.95}, ...]
    """
    selector = IngredientSelector()
    metadata = selector.load_metadata()
    
    # Find session and update predictions
    for session in metadata["sessions"]:
        if session["session_id"] == session_id:
            for ingredient in session["ingredients"]:
                for prediction in predictions:
                    if ingredient["id"] == prediction["ingredient_id"]:
                        ingredient["ml_prediction"] = prediction["prediction"]
                        ingredient["confidence"] = prediction["confidence"]
            break
    
    selector.save_metadata(metadata)

if __name__ == "__main__":
    # For testing
    display_ingredient_selector()
