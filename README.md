# OpenAI Marketing Assistant

The OpenAI Marketing Assistant is a toolkit designed to leverage OpenAI's API for various marketing tasks. Whether you need help pinpointing target audiences, crafting persuasive sales letters, or optimizing marketing emails, this toolkit harnesses the power of AI-generated content to boost the campaigns.

## Features/Tasks

- **Identify Niche Problem and Solution**
- **Define Target Audience and Create Avatar**
- **Write a Sales Letter in Story Form Using PAS Framework**

## Prerequisites

- Python 3.6 or higher
- OpenAI API key(see [OpenAI API](https://beta.openai.com/signup/) for more information)

## Usage

1. **Clone the repository:**

```bash
git clone https://github.com/rp42dev/OpenAI-Marketing-Assistant.git
```

2.  **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

Create a `.env` file in the root directory of the project and add the following environment variables but make sure to replace the values with your own.

[Environment variables example](#environment-variables-example-env)


4. **Set up configuration file:**

Create a `config.json` file in the root directory of the project and add the following configuration, use the example below as a guide.

[Configuration file example](#configuration-file-example-configjson)


5. **Run the application:**

```bash
python main.py
```

### Environment variables example (.env)

```env
OPENAI_API_TOKEN=sk-proj-1234567890...
ASSISTANT_ID_TOKEN=asst_1234567890...
```

### Configuration file example (config.json)

```json
{
    "tasks": {
        "1": {
            "name": "Identify Niche Problem and Solution",
            "instructions": "Based on user input, identify a specific problem within a niche and propose a solution that product or service addresses. Provide a brief description of both the problem and how the product or service can solve it."
        },
        "2": {
            "name": "Define Target Audience and Create Avatar",
            "instructions": "Using the information from Task 1, define the target audience and create a detailed avatar. Include demographics, psychographics, and any other relevant details."
        },
        "3": {
            "name": "Write a Sales Letter in Story Form Using PAS Framework",
            "instructions": "Write a sales letter in the form of a story using the Problem-Agitate-Solution (PAS) framework. The story should address the problem identified in Tasks 1 and 2 and demonstrate how the product or service can provide a solution."
        },
        "4": {
            "name": "Create a Landing Page for the Product or Service",
            "instructions": "Create a landing page for the product or service that includes a headline, subheadline, call-to-action, and any other relevant information. The landing page should be designed to convert visitors into leads or customers."
        }
    },
    "functions": {
        "1": {
            "name": "Task Correction",
            "instructions": "Make corrections to the previous response based on user input"
        }
    }
}
```

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug fixes, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

