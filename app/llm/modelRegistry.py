from typing import Dict
from .modelConfiguration import OllamaModelConfig
from .modelTask import ModelTask
from langchain_community.llms import Ollama

MODEL_REGISTRY: Dict[ModelTask, OllamaModelConfig] = {
    ModelTask.GRAMMAR: OllamaModelConfig(
        name="codellama:7b-instruct",
        temperature=0.2,
        top_p=0.1,
        top_k=40,
        repeat_penalty=1.2,
        stop=[

        ],
    ),
    ModelTask.EXPERIENCE: OllamaModelConfig(
        name="codellama:7b-instruct",
        temperature=0.1,
        top_p=0.2,
        top_k=40,
        repeat_penalty=1.1,
        stop=[

        ],
    ),
    ModelTask.LAYOUT: OllamaModelConfig(
        name="wizardcoder:7b-python",
        temperature=0.3,
        stop=[
            "```"
        ]
    )
}


def get_model_for_task(task: ModelTask) -> Ollama:
    print(f"Getting model for task: {task.name}")

    if task not in MODEL_REGISTRY:
        raise KeyError(f"No model configured for task: {task}")

    config = MODEL_REGISTRY[task]
    model = config.create_model()

    print(f"Using model: {config.name}")
    return model