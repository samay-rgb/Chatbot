from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

from chatterbot.response_selection import get_random_response
import spacy
nlp = spacy.load("en_core_web_sm")


def remove_hyphens(statement):
    """
    Remove hypnens.
    """
    statement.text = statement.text.replace('-', '')
    return statement


bot = ChatBot(name='Anakin', read_only=True,
              response_selection_method=get_random_response,
              storage_adapter='chatterbot.storage.SQLStorageAdapter',
              database_uri='sqlite:///database.sqlite3',
              logic_adapters=[
                  {
                      'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                      'input_text': 'empty',
                      'output_text': ''
                  },
                  {
                      'import_path': 'chatterbot.logic.BestMatch',
                      'default_response': 'i honestly have no idea how to respond to that',
                      'maximum_similarity_threshold': 0.9
                  },
                  {
                      'import_path': 'chatterbot.logic.MathematicalEvaluation'
                  }

              ]

              )
bot.preprocessors.append(
    remove_hyphens
)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train(
    "./greetings.yml",
    "./ecom.yml"
)
while True:
    request = input('you :')
    if request.lower() == 'bye' or request.lower() == 'thanks' or request.lower() == 'get lost':
        print("Bot:Hope I was able to help you.Thank you.Have a good day")
        break
    else:
        response = bot.get_response(request)
        print('Bot:', response)
