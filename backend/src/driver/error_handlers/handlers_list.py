from driver.app import app
from core.exceptions import external_exceptions, recognizer_exceptions
from driver.error_handlers import external_errors_handlers
from driver.error_handlers import recognizer_errors_handlers

# external exception
app.add_exception_handler(external_exceptions.ExternalException, external_errors_handlers.database_exception_handler)

# recognizer exceptions
app.add_exception_handler(recognizer_exceptions.LexicalException,
                          recognizer_errors_handlers.recognizer_lex_exception_handler)
app.add_exception_handler(recognizer_exceptions.GrammarException,
                          recognizer_errors_handlers.recognizer_grammar_exception_handler)
