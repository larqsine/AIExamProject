"""
Model Registry Module

This module manages the configuration and selection of different Ollama models
for specific AI tasks in the CV Helper application.

The registry implements task-specific model optimization:
- Different models are optimized for different types of feedback
- Each model has custom parameters (temperature, top_p, etc.)
- Centralized model management for easy maintenance and updates
"""
from typing import Dict
from .modelConfiguration import OllamaModelConfig
from .modelTask import ModelTask
from langchain_community.llms import Ollama

# Model Registry: Maps each task type to its optimized model configuration
# This allows for task-specific model selection and parameter tuning
MODEL_REGISTRY: Dict[ModelTask, OllamaModelConfig] = {
    # Grammar Task: Lower temperature for more consistent, precise corrections
    ModelTask.GRAMMAR: OllamaModelConfig(
        name="codellama:7b-instruct",  # Good at detailed analysis and corrections
        temperature=0.2,               # Low creativity, high precision
        top_p=0.1,                    # Conservative token selection
        top_k=40,                     # Limited vocabulary consideration
        repeat_penalty=1.2,           # Avoid repetitive feedback
        stop=[],                      # No custom stop tokens needed
    ),
    
    # Experience Task: Balanced parameters for constructive career advice
    ModelTask.EXPERIENCE: OllamaModelConfig(
        name="codellama:7b-instruct",  # Same model, different parameters
        temperature=0.1,               # Very low creativity for factual feedback
        top_p=0.2,                    # Slightly more token variety than grammar
        top_k=40,                     # Consistent vocabulary range
        repeat_penalty=1.1,           # Minimal repetition penalty
        stop=[],                      # No custom stop tokens
    ),
    
    # Layout Task: Higher creativity for design and structure suggestions
    ModelTask.LAYOUT: OllamaModelConfig(
        name="wizardcoder:7b-python",  # Different model specialized in structure
        temperature=0.3,               # Higher creativity for layout suggestions
        stop=["```"]                   # Stop at code blocks if generated
    )
}


def get_model_for_task(task: ModelTask) -> Ollama:
    """
    Retrieve and configure the appropriate Ollama model for a specific task.
    
    This function implements the factory pattern for model creation:
    1. Validates the requested task exists in registry
    2. Retrieves the task-specific configuration
    3. Creates and returns a configured Ollama model instance
    
    Args:
        task: The ModelTask enum specifying which type of feedback is needed
        
    Returns:
        Configured Ollama model instance ready for use
        
    Raises:
        KeyError: If the requested task is not configured in the registry
    """
    print(f"Getting model for task: {task.name}")

    # Validate task exists in registry
    if task not in MODEL_REGISTRY:
        raise KeyError(f"No model configured for task: {task}")

    # Get configuration and create model instance
    config = MODEL_REGISTRY[task]
    model = config.create_model()

    print(f"Using model: {config.name}")
    return model