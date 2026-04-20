from langchain_core.output_parsers import PydanticOutputParser  
from langchain_groq import ChatGroq
from src.models.question_schemas import MCQQuestion,FillBlankQuestion
from src.prompts.templates import mcq_prompt_template,fill_blank_prompt_template
from src.llm.groq_client import get_groq_client
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException

class QuestionGenerator:
    def __init__(self):
        self.llm=get_groq_client()
        self.logger=get_logger(self.__class__.__name__)
    
    def _retry_and_parse(self,prompt ,parser,topic,difficulty):
        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(f"Generating question for topic {topic} with difficulty {difficulty}")
                response=self.llm.invoke(prompt.format(topic=topic,difficulty=difficulty))
                parsed=parser.parse(response.content)
                self.logger.info("Successfully parsed the question")
                return parsed

            except Exception as e:
                self.logger.error(f"Error coming : {str(e)}")
                if attempt==settings.MAX_RETRIES-1:
                    raise CustomException(f"Failed to generate question after {settings.MAX_RETRIES} attempts") from e
                

    def generate_mcq(self,topic:str,difficulty:str="medium")->MCQQuestion:
        try:
            parser=PydanticOutputParser(pydantic_object=MCQQuestion)
            question=self._retry_and_parse(mcq_prompt_template,parser,topic,difficulty)
            if len(question.options) !=4 or question.correct_answer not in question.options:
                raise CustomException("Invalid question format: Options should be 4 and answer should be one of the options")
            self.logger.info("Successfully generated MCQ question")
            return question
        except Exception as e:
            self.logger.error(f"Error generating MCQ question: {str(e)}")
            raise CustomException("Failed to generate MCQ question",e)
        

    def generate_fill_blank(self,topic:str,difficulty:str="medium")->FillBlankQuestion:
        try:
            parser=PydanticOutputParser(pydantic_object=FillBlankQuestion)
            question=self._retry_and_parse(fill_blank_prompt_template,parser,topic,difficulty)
            if "_____" not in question.question:
                raise CustomException("Invalid question format: Question should contain a blank represented by _____")
            self.logger.info("Successfully generated Fill-in-the-Blank question")
            return question
        except Exception as e:
            self.logger.error(f"Error generating Fill-in-the-Blank question: {str(e)}")
            raise CustomException("Failed to generate Fill-in-the-Blank question",e)
        