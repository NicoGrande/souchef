import json
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_community.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.output_parsers import PydanticOutputParser

import src.data_models.recipe as sc_recipe
import src.data_models.item as sc_item
import src.data_models.quantity as sc_quantity
import src.data_models.user as sc_user
import src.utils.types as sc_types

import datetime
import dotenv
import pprint

dotenv.load_dotenv()


class CreateRecipeAgent:
    """
    Creates recipes from a list of available items.

    This class uses a language model and various tools to generate recipes
    based on available ingredients and their quantities.

    Attributes:
        _llm: The language model used for processing.
        _create_recipe_prompt: The prompt template for recipe creation.
        _tools: A list of tools available to the agent.
        _create_recipe_agent: The agent responsible for recipe creation.
        _create_recipe_agent_executor: The executor for the recipe agent.
        _schema_parser: Parser for the recipe schema.
    """

    def __init__(
        self, model: str = "gpt-4o", temperature: float = 0.5, verbose: bool = False
    ):
        """
        Initializes the CreateRecipeAgent.

        Args:
            model (str): The name of the language model to use.
            temperature (float): The temperature setting for the language model.
            verbose (bool): Whether to enable verbose output.
        """
        self._llm = ChatOpenAI(model=model, temperature=temperature)
        self._schema_parser = PydanticOutputParser(pydantic_object=sc_recipe.Recipe)
        self._create_recipe_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a creative chef who creates recipes based on available ingredients.",
                ),
                (
                    "system",
                    "Given a list of ingredients with their quantities and nutritional information, "
                    "create a recipe that uses these ingredients in reasonable proportions.",
                ),
                (
                    "system",
                    "Make sure the recipe instructions are clear and numbered steps.",
                ),
                (
                    "system",
                    "The recipe should use realistic quantities that make sense for a meal.",
                ),
                (
                    "system",
                    "If you need additional common ingredients (salt, pepper, etc.), you can include them and include the quantity in the recipe.",
                ),
                (
                    "system",
                    "The recipe should also take into account the preferences of the user.",
                ),
                (
                    "system",
                    "The recipe should also include the nutritional facts of the recipe. Use the nutritional facts of the ingredients and the proportions used in the recipe to determine the nutritional value of the recipe.",
                ),
                (
                    "system",
                    "{format_instructions}",
                ),
                (
                    "human",
                    "Please recommend a recipe using the following available ingredients: {ingredients}. Here are my preferences: {user_preferences}. Please also include the nutritional facts of the recipe.",
                ),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        self._tools = []
        self._setup_tools()
        self._create_recipe_agent = create_openai_tools_agent(
            self._llm, self._tools, prompt=self._create_recipe_prompt
        )
        self._create_recipe_agent_executor = AgentExecutor(
            agent=self._create_recipe_agent, tools=self._tools, verbose=verbose
        )

    def _setup_tools(self):
        """
        Sets up the tools used by the agent.
        """
        google_search_api = GoogleSearchAPIWrapper()
        self._tools.append(
            Tool(
                name="google_search",
                description="Search for recipe ideas and cooking techniques.",
                func=google_search_api.run,
            )
        )

    def create_recipe(
        self, items: list[sc_item.Item], user_preferences: sc_user.UserPreferences
    ) -> sc_recipe.Recipe:
        """
        Creates a recipe from a list of available items.

        Args:
            items (list[sc_item.Item]): List of available ingredients.

        Returns:
            sc_recipe.Recipe: A generated recipe using the available ingredients.

        Raises:
            ValueError: If the output cannot be parsed into a valid recipe.
        """
        # Format ingredients for the prompt
        ingredients_info = []
        for item in items:
            ingredient_info = (
                f"{item.name}: {item.quantity.quantity} {item.quantity.unit.value}, "
                f"(per serving: {item.per_serving_macros[sc_types.Macro.CALORIES].quantity} calories, "
                f"{item.per_serving_macros[sc_types.Macro.PROTEIN].quantity}g protein, "
                f"{item.per_serving_macros[sc_types.Macro.CARB].quantity}g carbs, "
                f"{item.per_serving_macros[sc_types.Macro.FAT].quantity}g fat)"
            )
            ingredients_info.append(ingredient_info)

        output = self._create_recipe_agent_executor.invoke(
            {
                "ingredients": "\n".join(ingredients_info),
                "format_instructions": self._schema_parser.get_format_instructions(),
                "user_preferences": user_preferences.model_dump_json(),
            }
        )

        # Clean up the output text
        output_text = output["output"]

        # Find the JSON content between triple backticks
        if "```json" in output_text:
            start = output_text.find("```json") + 7
            end = output_text.rfind("```")
            output_text = output_text[start:end].strip()

        try:
            output_json = json.loads(output_text)
            recipe = sc_recipe.Recipe.model_validate(output_json)
            # recipe.populate_items(items)
            return recipe
        except Exception as e:
            raise ValueError(
                f"Failed to parse recipe output: {e}\nOutput text: {output_text}"
            )


if __name__ == "__main__":
    # Create test items
    items = [
        sc_item.Item(
            name="Chicken Breast",
            quantity=sc_quantity.Quantity(
                quantity=1.5, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
            ),
            price=11.99,
            merchant="Trader Joe's",
            per_serving_macros={
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    quantity=31, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    quantity=3.6,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    quantity=165, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
            },
            serving_size=sc_quantity.Quantity(
                quantity=4, unit=sc_types.Unit.OUNCES, type=sc_types.UnitType.WEIGHT
            ),
            shelf_life=datetime.timedelta(days=5),
            storage=sc_types.StorageType.FRIDGE,
        ),
        sc_item.Item(
            name="Brown Rice",
            quantity=sc_quantity.Quantity(
                quantity=2, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
            ),
            price=4.99,
            merchant="Whole Foods",
            per_serving_macros={
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    quantity=5, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    quantity=45, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    quantity=2, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    quantity=216, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    quantity=0.7,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    quantity=3.5,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
            },
            serving_size=sc_quantity.Quantity(
                quantity=0.25, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
            ),
            shelf_life=datetime.timedelta(days=365),
            storage=sc_types.StorageType.PANTRY,
        ),
        sc_item.Item(
            name="Black Beans",
            quantity=sc_quantity.Quantity(
                quantity=15, unit=sc_types.Unit.OUNCES, type=sc_types.UnitType.WEIGHT
            ),
            price=1.99,
            merchant="Trader Joe's",
            per_serving_macros={
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    quantity=7, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    quantity=20, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    quantity=0.5,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    quantity=120, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    quantity=8, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
            },
            serving_size=sc_quantity.Quantity(
                quantity=0.5, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
            ),
            shelf_life=datetime.timedelta(days=730),
            storage=sc_types.StorageType.PANTRY,
        ),
        sc_item.Item(
            name="Roma Tomatoes",
            quantity=sc_quantity.Quantity(
                quantity=1, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
            ),
            price=3.99,
            merchant="Whole Foods",
            per_serving_macros={
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    quantity=1, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    quantity=4, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    quantity=0.2,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    quantity=22, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    quantity=2.5,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    quantity=1.2,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
            },
            serving_size=sc_quantity.Quantity(
                quantity=148, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            shelf_life=datetime.timedelta(days=7),
            storage=sc_types.StorageType.FRIDGE,
        ),
        sc_item.Item(
            name="Sweet Onion",
            quantity=sc_quantity.Quantity(
                quantity=1, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
            ),
            price=1.49,
            merchant="Trader Joe's",
            per_serving_macros={
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    quantity=1.1,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    quantity=9, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    quantity=0.1,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    quantity=40, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    quantity=4.2,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    quantity=1.7,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
            },
            serving_size=sc_quantity.Quantity(
                quantity=110, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            shelf_life=datetime.timedelta(days=30),
            storage=sc_types.StorageType.PANTRY,
        ),
        sc_item.Item(
            name="Garlic",
            quantity=sc_quantity.Quantity(
                quantity=6, unit=sc_types.Unit.OUNCES, type=sc_types.UnitType.WEIGHT
            ),
            price=0.99,
            merchant="Trader Joe's",
            per_serving_macros={
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    quantity=0.6,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    quantity=3, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    quantity=0, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    quantity=13, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    quantity=0.1,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    quantity=0.2,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
            },
            serving_size=sc_quantity.Quantity(
                quantity=3, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            shelf_life=datetime.timedelta(days=180),
            storage=sc_types.StorageType.PANTRY,
        ),
        sc_item.Item(
            name="Bell Peppers",
            quantity=sc_quantity.Quantity(
                quantity=1, unit=sc_types.Unit.POUNDS, type=sc_types.UnitType.WEIGHT
            ),
            price=3.99,
            merchant="Whole Foods",
            per_serving_macros={
                sc_types.Macro.PROTEIN: sc_quantity.Quantity(
                    quantity=1, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.CARB: sc_quantity.Quantity(
                    quantity=6, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
                ),
                sc_types.Macro.FAT: sc_quantity.Quantity(
                    quantity=0.3,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.CALORIES: sc_quantity.Quantity(
                    quantity=30, unit=sc_types.Unit.KCAL, type=sc_types.UnitType.ENERGY
                ),
                sc_types.Macro.SUGAR: sc_quantity.Quantity(
                    quantity=4.2,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
                sc_types.Macro.FIBER: sc_quantity.Quantity(
                    quantity=2.1,
                    unit=sc_types.Unit.GRAMS,
                    type=sc_types.UnitType.WEIGHT,
                ),
            },
            serving_size=sc_quantity.Quantity(
                quantity=148, unit=sc_types.Unit.GRAMS, type=sc_types.UnitType.WEIGHT
            ),
            shelf_life=datetime.timedelta(days=14),
            storage=sc_types.StorageType.FRIDGE,
        ),
    ]

    user_preferences = sc_user.UserPreferences(
        number_of_people=4,
        favorite_cuisines=["Italian", "Mexican", "Chinese", "Healthy", "High Protein"],
        favorite_recipes=["Chicken Alfredo", "Burrito", "Fried Rice"],
        kitchen_appliances=["Oven", "Stove", "Microwave"],
        dietary_restrictions=["Vegan", "Gluten-free"],
    )

    create_recipe_agent = CreateRecipeAgent()
    recipe = create_recipe_agent.create_recipe(items, user_preferences)
    print(recipe.model_dump_json(indent=4))
