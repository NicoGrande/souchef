import base64
import httpx
import json
import validators

from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.output_parsers import PydanticOutputParser

import src.data_models.item as sc_item
import src.data_models.item as sc_item
import src.data_models.receipt as sc_receipt


class ExtractItemsAgent:
    """
    Extracts items from a receipt and an image of the items on the receipt.

    This class uses a language model and various tools to process receipt information
    and extract detailed item data, including nutritional information.

    Attributes:
        _llm: The language model used for processing.
        _extract_items_prompt: The prompt template for item extraction.
        _tools: A list of tools available to the agent.
        _extract_items_agent: The agent responsible for item extraction.
        _extract_items_agent_executor: The executor for the extraction agent.
        _schema: The schema definition for the output data.
        _branded_items_url: URL for branded items database.
        _foundation_items_url: URL for foundation items database.
    """

    def __init__(
        self, model: str = "gpt-4o-mini", temperature: float = 0, verbose: bool = False
    ):
        """
        Initializes the ExtractItemsAgent.

        Args:
            model (str): The name of the language model to use. Defaults to "gpt-4o-mini".
            temperature (float): The temperature setting for the language model. Defaults to 0.
            verbose (bool): Whether to enable verbose output. Defaults to False.
        """
        self._llm = ChatOpenAI(model=model, temperature=temperature)
        self._schema_parser = PydanticOutputParser(pydantic_object=sc_receipt.Receipt)
        self._extract_items_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are recieving a receipt and an image of the items on the receipt for a particular supermarket purchase.",
                ),
                (
                    "system",
                    "Use the receipt and the following image to extract items. The receipt may be blurry, so use the image to help you. There should be one item per line on the receipt.",
                ),
                (
                    "system",
                    "Be sure to extract the supermarket or merchat from the top of the receipt.",
                ),
                (
                    "system",
                    "If required, extract any necessary information about each item from the merchat website.",
                ),
                (
                    "system",
                    "The per unit amount of each item is important to extract. It often appears online as 'price / unit amount'. For example if the price is '$1.99 / 100g' then the unit amount is 100g.",
                ),
                (
                    "system",
                    "{format_instructions}",
                ),
                (
                    "human",
                    [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/jpeg;base64,{receipt_data}"
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
                        },
                    ],
                ),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        self._tools = []
        self._setup_tools()
        self._extract_items_agent = create_openai_tools_agent(
            self._llm, self._tools, prompt=self._extract_items_prompt
        )
        self._extract_items_agent_executor = AgentExecutor(
            agent=self._extract_items_agent, tools=self._tools, verbose=verbose
        )
        self._branded_items_url = (
            "https://fdc.nal.usda.gov/fdc-app.html#/food-search?query=&type=Branded"
        )
        self._foundation_items_url = (
            "https://fdc.nal.usda.gov/fdc-app.html#/food-search?query=&type=Foundation"
        )

    def _setup_tools(self):
        """
        Sets up the tools used by the agent.

        This method initializes the Google Search API tool and adds it to the agent's toolkit.
        """
        google_search_api = GoogleSearchAPIWrapper()
        self._tools.append(
            Tool(
                name="google_search",
                description="Search the internet for nutritional and serving size information of food items.",
                func=google_search_api.run,
            )
        )

    def extract_items_from_receipt(
        self, receipt_url: str, image_url: str
    ) -> sc_receipt.Receipt:
        """
        Extracts items from a receipt and an image of the items.

        This method processes the receipt and image data, and uses the agent to extract
        detailed information about the items.

        Args:
            receipt_url (str): URL of the receipt image.
            image_url (str): URL of the image containing the items.

        Raises:
            ValueError: If the provided URLs are not valid.

        Returns:
            list[str]: A list of extracted items with their details.
        """
        if not validators.url(receipt_url) or not validators.url(image_url):
            raise ValueError("Invalid URL provided.")

        receipt_data = base64.b64encode(httpx.get(receipt_url).content).decode("utf-8")
        image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")

        output = self._extract_items_agent_executor.invoke(
            {
                "receipt_data": receipt_data,
                "image_data": image_data,
                "branded_items_url": self._branded_items_url,
                "foundation_items_url": self._foundation_items_url,
                "format_instructions": self._schema_parser.get_format_instructions(),
            }
        )

        # Clean up the output text by removing markdown code block syntax and newlines
        output_text = output["output"]
        if output_text.startswith("```json\n"):
            output_text = output_text[7:]  # Remove ```json\n prefix
        if output_text.endswith("\n```"):
            output_text = output_text[:-4]  # Remove \n``` suffix

        try:
            output_json = json.loads(output_text)
            receipt = sc_receipt.Receipt.model_validate(output_json)
            return receipt
        except Exception as e:
            raise ValueError(
                f"Failed to parse JSON output: {e}\nOutput text: {output_text}"
            )


class ValidateItemsAgent:
    """
    Validates items extracted from a receipt.
    """

    def __init__(
        self, model: str = "gpt-4o-mini", temperature: float = 0, verbose: bool = False
    ):
        self._llm = ChatOpenAI(model=model, temperature=temperature)
        self._schema_parser = PydanticOutputParser(pydantic_object=sc_item.Item)
        self._validate_items_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are recieving a list of items extracted from a reciept.",
                ),
                (
                    "system",
                    "For each of the items, search online to find nutritional information and provide any additional information that is missing on the item.",
                ),
                (
                    "system",
                    "The nutritial information that is important to extract is the serving size as well as the calories, protein, fat, carbohydrates, fiber and sugars per serving.",
                ),
                (
                    "system",
                    "For each macro (calories, protein, fat, carbohydrates, fiber, sugars), ensure you include both the quantity and unit, as well as the type field. For example: 'quantity': 140, 'unit': 'kcal', 'type': 'energy'",
                ),
                (
                    "system",
                    "Valid values for the type field are 'energy', 'weight', and 'volume' depending on the unit of the macro.",
                ),
                (
                    "system",
                    "A good query for nutritional information is '{merchant} [ITEM NAME] nutrition facts' for each of the items in {items}.",
                ),
                (
                    "system",
                    "{format_instructions}",
                ),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        self._tools = []
        self._setup_tools()
        self._validate_items_agent = create_openai_tools_agent(
            self._llm, self._tools, prompt=self._validate_items_prompt
        )
        self._validate_items_agent_executor = AgentExecutor(
            agent=self._validate_items_agent, tools=self._tools, verbose=verbose
        )

    def _setup_tools(self):
        """
        Sets up the tools used by the agent.

        This method initializes the Google Search API tool and adds it to the agent's toolkit.
        """
        google_search_api = GoogleSearchAPIWrapper()
        self._tools.append(
            Tool(
                name="google_search",
                description="Search the internet for nutritional and serving size information of food items.",
                func=google_search_api.run,
            )
        )

    def validate_items(self, receipt: sc_receipt.Receipt) -> list[sc_item.Item]:
        """
        Validates items extracted from a receipt.

        This method processes the receipt and image data, and uses the agent to extract
        detailed information about the items.

        Args:
            items (list[sc_item.Item]): A list of items to validate.

        Raises:
            ValueError: If the output JSON is not valid.

        Returns:
            list[str]: A list of extracted items with their details.
        """

        items_str = [item.name for item in receipt.items]
        output = self._validate_items_agent_executor.invoke(
            {
                "items": items_str,
                "merchant": receipt.merchant,
                "format_instructions": self._schema_parser.get_format_instructions(),
            }
        )

        # Clean up the output text by removing markdown code block syntax and newlines
        output_text = output["output"]
        if output_text.startswith("```json\n"):
            output_text = output_text[7:]  # Remove ```json\n prefix
        if output_text.endswith("\n```"):
            output_text = output_text[:-4]  # Remove \n``` suffix

        try:
            output_json = json.loads(output_text)
            validated_items = []
            for index, item in enumerate(output_json["items"]):
                validated_item = sc_item.Item.model_validate(item)
                validated_item.price = receipt.items[index].price
                validated_items.append(validated_item)

            return validated_items
        except Exception as e:
            raise ValueError(
                f"Failed to parse JSON output: {e}\nOutput text: {output_text}"
            )
