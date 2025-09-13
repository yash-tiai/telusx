#!/usr/bin/env python3
"""
Simple script to test model loading from main.py
"""
import joblib
import sys
import os

# Add the current directory to Python path
sys.path.append('.')

def test_model_loading():
    """Test loading the model directly"""
    try:
        # Load model directly
        model = joblib.load("risk_engine_iforest.pkl")
        print("✅ Model loaded successfully from 'risk_engine_iforest.pkl'")
        print(f"Model type: {type(model)}")
        print(f"Model contamination: {model.contamination}")
        print(f"Model random state: {model.random_state}")
        print(f"Model n_estimators: {model.n_estimators}")
        return model
    except FileNotFoundError:
        print("❌ Model file 'risk_engine_iforest.pkl' not found")
        return None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def test_model_from_main():
    """Test loading model using the load_model function from main.py"""
    try:
        # Import just the load_model function
        from app.main import load_model
        model = load_model()
        if model is not None:
            print("✅ Model loaded successfully using load_model() from main.py")
            return model
        else:
            print("❌ load_model() returned None")
            return None
    except Exception as e:
        print(f"❌ Error importing from main.py: {e}")
        return None

if __name__ == "__main__":
    print("Testing model loading...")
    print("=" * 50)
    
    print("\n1. Testing direct model loading:")
    model1 = test_model_loading()
    
    print("\n2. Testing model loading from main.py:")
    model2 = test_model_from_main()
    
    print("\n" + "=" * 50)
    if model1 is not None and model2 is not None:
        print("✅ Both methods work! Model is ready to use.")
    else:
        print("❌ Some issues with model loading.")
