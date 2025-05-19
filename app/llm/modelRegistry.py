from .modelConfiguration import OllamaModelConfig
from .modelTask import ModelTask
from langchain_community.llms import Ollama


# Define model configurations for each task
MODEL_REGISTRY: Dict[ModelTask, OllamaModelConfig] = {
    ModelTask.GRAMMAR: OllamaModelConfig(
        name="codellama:7b-instruct",
        temperature=0.2,  # Lower temperature for more consistent output
        top_p=0.1,       # More focused sampling
        top_k=40,
        repeat_penalty=1.2,
        stop=[

        ],
    ),
    ModelTask.EXPERIENCE: OllamaModelConfig(
        name="codellama:7b-instruct",
        temperature=0.1,  # Slight randomness for better translations
        top_p=0.2,
        top_k=40,
        repeat_penalty=1.1,
        stop=[

        ],
    ),
    ModelTask.LAYOUT: OllamaModelConfig(
        name="wizardcoder:7b-python",  # WizardCoder is good for explanations too
        temperature=0.3,  # Slightly higher temperature for natural explanations
        stop=[
            "```"           # Stops the model from including examples in explanation
                            # This keeps explanations as natural language only
        ]
    )
}

def get_model_for_task(task: ModelTask) -> Ollama:
    """
    Get the appropriate LLM model for a specific task.
    """
    print(f"Getting model for task: {task.name}")
    
    if task not in MODEL_REGISTRY:
        raise KeyError(f"No model configured for task: {task}")
    
    config = MODEL_REGISTRY[task]
    model = config.create_model()
    
    print(f"Using model: {config.name}")
    return model