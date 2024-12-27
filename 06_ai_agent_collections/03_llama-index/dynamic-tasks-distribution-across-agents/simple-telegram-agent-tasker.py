import os
import openai
import logging
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from distributed_agent_tasker import generate_task_list, extract_agent_task_and_tools, create_agent
from llama_index.llms.openai import OpenAI as LlamaOpenAI

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # You can set your API key in an environment variable

# Define constants from distributed tasks
MODEL_AGENT = "gpt-4o"

# Initialize LlamaOpenAI
llm = LlamaOpenAI(
    model=MODEL_AGENT, 
    system_prompt="You are a helpful assistant that can search the web, \
    read files, write to files, scrape websites, generate images, and process images. If you're given the write_file tool\
    you should always use it at the end of the task to compile the outputs of the research or other tasks. \
    When given the web_search tool, you should always use it to search the web for information relevant to the task\
    and then ALWAYS use the write_file tool to write the results of the search to a file\
    if the write_file tool is available."
)

# Start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hi Im an AI Agent, ask me to do anything.',
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages and process tasks using the distributed task system."""
    user_message = update.message.text

    try:
        # Generate task list from user message
        task_list = generate_task_list(user_message)
        print("Tasks identified: ")
        for task in task_list:
            print(task)
        
        # Process each task and collect responses
        responses = []
        for task in task_list:
            agent_task, agent_tools = extract_agent_task_and_tools(task)
            agent = create_agent(llm, agent_tools)
            response = agent.chat(agent_task)
            responses.append(response)
            
            # Send each task response to the user
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=f"Task: {agent_task}\n\nResponse: {response.response}"
            )
            
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Sorry, I couldn't process your request at the moment."
        )
        logger.error(f"Error: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.warning(f'Update "{update}" caused error "{context.error}"')


def main() -> None:
    """Start the bot."""
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == "__main__":
    main()