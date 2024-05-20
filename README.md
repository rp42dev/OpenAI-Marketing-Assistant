# OpenAI Marketing Assistant

The OpenAI Marketing Assistant is a toolkit designed to leverage OpenAI's API for various marketing tasks. Whether you need help pinpointing target audiences, crafting persuasive sales letters, or optimizing marketing emails, this toolkit harnesses the power of AI-generated content to boost the campaigns.

## Features

- **Target Audience Identification:** Utilize AI to identify and analyze target audiences based on provided criteria.
- **Sales Letter Generation:** Automatically generate persuasive sales letters tailored to the audience.
- **Email Marketing Optimization:** Optimize marketing emails with AI-generated content for increased engagement and conversion rates.

## Usage

1. Install dependencies by running `pip install -r requirements.txt`.
2. Set up the OpenAI API key and other environment variables.
3. Run `main.py` to start the OpenAI Marketing Assistant toolkit.

## Configuration file example

```json
{
    "tasks": {
        "1": {
            "name": "Identify Niche Problem and solution",  
            "instructions": "Task 1: Based on user input, identify a niche problem and solution that the product or service can address. Provide a brief description of the problem and how the product or service can solve it.",
            "role": "user"
        },
        "2": {
            "name": "Define Target Audience and create Avatar",
            "instructions": "Task 2: based on previous task, define the target audience and create an avatar for the target audience. Include demographics, psychographics, and any other relevant information.",
            "role": "user"
        },
        "3": {
            "name": "Write a Sales Letter in the form of a Story PAS",
            "instructions": "task 3: Write a sales letter in the form of a story using the Problem-Agitate-Solution (PAS) framework. The story should address the problem identified in task 1 and how the product or service can solve it.",
            "role": "user"
        }
    }
}
```
## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug fixes, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

