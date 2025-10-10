# backend/services/answer_generator.py

import logging
from typing import Optional
from transformers import pipeline, Pipeline
import torch

logger = logging.getLogger(__name__)

class AnswerGenerator:
    """Service for generating answers using Hugging Face models."""
    
    def __init__(self, model_name: str = "google/flan-t5-base"):
        self.model_name = model_name
        self.pipeline: Optional[Pipeline] = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Hugging Face model pipeline."""
        try:
            # Use CPU or GPU based on availability
            device = 0 if torch.cuda.is_available() else -1
            
            self.pipeline = pipeline(
                "text2text-generation",
                model=self.model_name,
                device=device,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            logger.info(f"Initialized {self.model_name} on {'GPU' if device == 0 else 'CPU'}")
            
        except Exception as e:
            logger.error(f"Failed to initialize model {self.model_name}: {e}")
            # Fallback to a smaller model
            try:
                self.pipeline = pipeline(
                    "text2text-generation",
                    model="google/flan-t5-small",
                    device=-1  # Force CPU for smaller model
                )
                logger.info("Fallback to flan-t5-small on CPU")
            except Exception as fallback_error:
                logger.error(f"Fallback model also failed: {fallback_error}")
                self.pipeline = None
    
    def generate_answer(self, query: str, context: str, max_length: int = 256) -> str:
        """Generate an answer based on query and context."""
        if not self.pipeline:
            return "Sorry, the answer generation service is not available at the moment."
        
        if not context.strip():
            return "I don't have enough context to answer this question. Please try uploading relevant documents first."
        
        # Create a structured prompt for the model
        prompt = self._create_prompt(query, context)
        
        try:
            # Generate answer
            response = self.pipeline(
                prompt,
                max_length=max_length,
                min_length=20,
                do_sample=False,
                temperature=0.7,
                num_return_sequences=1
            )
            
            answer = response[0]['generated_text'].strip()
            
            # Post-process the answer
            answer = self._post_process_answer(answer)
            
            return answer
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"I apologize, but I encountered an error while generating an answer: {str(e)}"
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create a structured prompt for the model."""
        # Truncate context if too long (keep within model limits)
        max_context_length = 1000
        if len(context) > max_context_length:
            context = context[:max_context_length] + "..."
        
        prompt = f"""Answer the question based on the provided context. Be concise and accurate.

Context: {context}

Question: {query}

Answer:"""
        
        return prompt
    
    def _post_process_answer(self, answer: str) -> str:
        """Clean up and format the generated answer."""
        # Remove any prompt repetition
        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()
        
        # Remove common artifacts
        answer = answer.replace("</s>", "").strip()
        
        # Ensure answer ends with proper punctuation
        if answer and not answer.endswith(('.', '!', '?')):
            answer += '.'
        
        return answer
    
    def is_available(self) -> bool:
        """Check if the answer generator is available."""
        return self.pipeline is not None

# Global service instance
answer_generator = AnswerGenerator()