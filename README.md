# OpenAI Marketing Assistant

The OpenAI Marketing Assistant is a toolkit designed to leverage OpenAI's API for various marketing tasks. Whether you need help pinpointing target audiences, crafting persuasive sales letters, or optimizing marketing emails, this toolkit harnesses the power of AI-generated content to boost your campaigns.

## Features

- **Target Audience Identification:** Utilize AI to identify and analyze target audiences based on provided criteria.
- **Sales Letter Generation:** Automatically generate persuasive sales letters tailored to your audience.
- **Email Marketing Optimization:** Optimize marketing emails with AI-generated content for increased engagement and conversion rates.

## Usage

1. Install dependencies by running `pip install -r requirements.txt`.
2. Set up your OpenAI API key and other environment variables.
3. Run `main.py` to start the OpenAI Marketing Assistant toolkit.

## Configuration file example

```json
{
    "tasks": {
        "1": {
            "name": "find an ideal customer",
            "instructions": "based on user input, find a ideal customer for the user in niche market. (keep it short and simple)",
            "role": "user"
        },
        "2": {
            "name": "name goes here",
            "instructions": "instructions goes here",
            "role": "user"
        },
        "3": {
            "name": "name goes here",
            "instructions": "instructions goes here",
            "role": "user"
        }
    }
}
```
## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug fixes, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

