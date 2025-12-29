# Enhanced Recipe Recommender - Ingredient Selection Workflow

## 🚀 New Features

### Interactive Ingredient Selection
- **Click-to-select**: Click directly on ingredients in your photo
- **Visual feedback**: Selected ingredients are highlighted with red circles
- **Background removal**: Automatically remove backgrounds for better ML accuracy
- **Batch processing**: Extract and analyze multiple ingredients at once

### ML Integration Ready
- **Modular design**: Easy to integrate your trained ML models
- **Mock mode**: Test the workflow without a trained model
- **Confidence scoring**: Filter results based on prediction confidence
- **Manual correction**: Override ML predictions when needed

### Complete Workflow
1. **📸 Photo Capture**: Take or upload ingredient photos
2. **🎯 Ingredient Selection**: Click to select individual ingredients
3. **🤖 ML Analysis**: AI-powered ingredient identification
4. **🍽️ Recipe Recommendation**: Get recipes based on detected ingredients

## 🔧 Technical Architecture

### Core Components

```
app/
├── app.py                      # Main Streamlit application
├── ingredient_selector.py      # Interactive selection & storage
├── ml_integration.py          # ML model interface
├── workflow_example.py        # Complete workflow demo
└── object_clipping.py         # Original clipping utility
```

### Key Classes

- **`IngredientSelector`**: Handles clicking, extraction, and storage
- **`MockIngredientClassifier`**: Demo ML classifier
- **`RealIngredientClassifier`**: Template for your actual model

### Data Flow

```
Photo → Click Coordinates → Extracted Regions → ML Predictions → Recipe Features → Recommendations
```

## 🛠️ Usage Examples

### Basic Workflow
```python
from ingredient_selector import IngredientSelector
from ml_integration import get_classifier

# Initialize components
selector = IngredientSelector()
classifier = get_classifier(use_mock=True)

# Process image
image = Image.open("ingredients.jpg")
coordinates = [(100, 150), (300, 200)]  # Click coordinates

# Extract ingredients
for i, (x, y) in enumerate(coordinates):
    extracted = selector.process_click_coordinates(image, (x, y))
    prediction, confidence = classifier.predict(extracted)
    print(f"Ingredient {i+1}: {prediction} ({confidence:.1%})")
```

### Integration with Your ML Model
```python
# Replace mock with your trained model
class YourIngredientClassifier(RealIngredientClassifier):
    def load_model(self):
        self.model = torch.load('your_model.pth')
        self.class_names = ['tomato', 'onion', ...]  # Your classes
        self.model_loaded = True
    
    def predict(self, image):
        # Your prediction logic
        processed = self.preprocess_image(image)
        output = self.model(processed)
        return class_name, confidence
```

## 📁 File Structure

### Generated Files
```
extracted_ingredients/           # Saved ingredient images
├── session_20241229_160030_ingredient_1_20241229_160045.png
├── session_20241229_160030_ingredient_2_20241229_160045.png
└── ...

ingredients_metadata.json       # Session and prediction metadata
```

### Metadata Format
```json
{
  "sessions": [
    {
      "session_id": "session_20241229_160030",
      "created_at": "20241229_160030",
      "ingredients": [
        {
          "id": "ingredient_1",
          "click_coordinates": [150, 200],
          "image_path": "extracted_ingredients/...",
          "ml_prediction": "tomato",
          "confidence": 0.92
        }
      ]
    }
  ]
}
```

## 🎯 ML Model Integration Guide

### 1. Prepare Your Model
- Train on ingredient images (224x224 recommended)
- Export in PyTorch (.pth), ONNX (.onnx), or TensorFlow format
- Create class labels list

### 2. Implement RealIngredientClassifier
```python
def load_model(self):
    self.model = torch.load(self.model_path)
    self.class_names = load_class_names()  # Your implementation

def predict(self, image):
    # Preprocess
    tensor = self.preprocess_image(image)
    
    # Predict
    with torch.no_grad():
        output = self.model(tensor)
        probs = torch.softmax(output, dim=1)
        confidence, predicted = torch.max(probs, 1)
    
    return self.class_names[predicted], confidence.item()
```

### 3. Update Main App
```python
# In app.py, replace mock with real classifier
classifier = get_classifier(use_mock=False, model_path="path/to/model.pth")
```

## 🔗 Recipe Database Integration

### Connect Your Recipe Data
```python
def get_recipe_recommendations(ingredients, confidence_weights):
    # Your recipe matching logic
    # Could use:
    # - Jaccard similarity
    # - TF-IDF matching  
    # - Embedding similarity
    # - Database queries
    
    return matching_recipes
```

### Example Recipe Matching
```python
# Simple ingredient matching
def find_recipes_by_ingredients(ingredients):
    recipes = load_recipe_database()
    
    scored_recipes = []
    for recipe in recipes:
        # Calculate overlap score
        overlap = len(set(ingredients) & set(recipe['ingredients']))
        score = overlap / len(recipe['ingredients'])
        
        if score > 0.5:  # At least 50% ingredient match
            scored_recipes.append((recipe, score))
    
    return sorted(scored_recipes, key=lambda x: x[1], reverse=True)
```

## 🚦 Running the Application

### Development Mode
```bash
# With full functionality (Python 3.12)
source .venv-py312/bin/activate
streamlit run app/workflow_example.py
```

### Production Mode
```bash
# Auto-detects best environment
./run.sh
```

### Demo Mode
```bash
# Test with mock ML predictions
streamlit run app/workflow_example.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Click detection not working**
   - Install: `pip install streamlit-image-coordinates`
   - Fallback to manual coordinate input

2. **Background removal failing**
   - Requires Python ≤3.12
   - Install: `pip install rembg onnxruntime`

3. **ML predictions failing**
   - Check model path and format
   - Verify input image preprocessing
   - Use mock mode for testing

### Performance Tips

1. **Image optimization**
   - Resize large images before processing
   - Use JPEG for faster loading, PNG for quality

2. **ML optimization**
   - Batch process multiple ingredients
   - Cache model loading
   - Use GPU if available

3. **Storage optimization**
   - Set maximum storage per session
   - Clean up old sessions automatically

## 📊 Next Steps

1. **Train your ingredient classifier** on your specific ingredients
2. **Integrate your recipe database** with the recommendation engine  
3. **Add user feedback** to improve predictions over time
4. **Deploy to production** using the provided Docker/cloud configs

Your object clipping workflow is now transformed into a complete ingredient-to-recipe pipeline! 🎉
