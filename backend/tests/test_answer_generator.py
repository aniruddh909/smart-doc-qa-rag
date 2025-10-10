# backend/tests/test_answer_generator.py

import pytest
from unittest.mock import Mock, patch
from backend.services.answer_generator import AnswerGenerator, answer_generator

def test_answer_generator_initialization():
    """Test that answer generator initializes correctly."""
    generator = AnswerGenerator()
    assert generator.model_name == "google/flan-t5-base"
    # Note: pipeline might be None if model fails to load in test environment

def test_generate_answer_with_context():
    """Test answer generation with valid context."""
    generator = AnswerGenerator()
    
    # Mock the pipeline to avoid loading actual model in tests
    mock_pipeline = Mock()
    mock_pipeline.return_value = [{"generated_text": "Machine learning is a subset of AI."}]
    generator.pipeline = mock_pipeline
    
    query = "What is machine learning?"
    context = "Machine learning is a subset of artificial intelligence that enables computers to learn from data."
    
    answer = generator.generate_answer(query, context)
    
    assert isinstance(answer, str)
    assert len(answer) > 0
    assert "machine learning" in answer.lower() or "ai" in answer.lower()
    mock_pipeline.assert_called_once()

def test_generate_answer_empty_context():
    """Test answer generation with empty context."""
    generator = AnswerGenerator()
    generator.pipeline = Mock()  # Mock pipeline
    
    query = "What is AI?"
    context = ""
    
    answer = generator.generate_answer(query, context)
    
    assert "don't have enough context" in answer.lower()

def test_generate_answer_no_pipeline():
    """Test answer generation when pipeline is not available."""
    generator = AnswerGenerator()
    generator.pipeline = None
    
    query = "What is AI?"
    context = "AI is artificial intelligence."
    
    answer = generator.generate_answer(query, context)
    
    assert "not available" in answer.lower()

def test_create_prompt():
    """Test prompt creation."""
    generator = AnswerGenerator()
    
    query = "What is Python?"
    context = "Python is a programming language."
    
    prompt = generator._create_prompt(query, context)
    
    assert "Question: What is Python?" in prompt
    assert "Context: Python is a programming language." in prompt
    assert "Answer:" in prompt

def test_post_process_answer():
    """Test answer post-processing."""
    generator = AnswerGenerator()
    
    # Test removing Answer: prefix
    answer = "Answer: Python is a programming language"
    processed = generator._post_process_answer(answer)
    assert processed == "Python is a programming language."
    
    # Test adding punctuation
    answer = "Python is great"
    processed = generator._post_process_answer(answer)
    assert processed == "Python is great."
    
    # Test removing artifacts
    answer = "Python is useful</s>"
    processed = generator._post_process_answer(answer)
    assert processed == "Python is useful."

def test_context_truncation():
    """Test that very long context gets truncated."""
    generator = AnswerGenerator()
    
    query = "What is this about?"
    long_context = "This is a test. " * 200  # Very long context
    
    prompt = generator._create_prompt(query, long_context)
    
    # Should be truncated
    assert len(prompt) < len(long_context) + 100

def test_is_available():
    """Test availability check."""
    generator = AnswerGenerator()
    
    # Test with pipeline
    generator.pipeline = Mock()
    assert generator.is_available() is True
    
    # Test without pipeline
    generator.pipeline = None
    assert generator.is_available() is False

@patch('backend.services.answer_generator.pipeline')
def test_fallback_model_loading(mock_pipeline):
    """Test fallback model loading when main model fails."""
    # Simulate main model failure, then successful fallback
    mock_pipeline.side_effect = [Exception("Main model failed"), Mock()]
    
    generator = AnswerGenerator()
    
    # Should have called pipeline twice (main + fallback)
    assert mock_pipeline.call_count == 2

def test_global_instance():
    """Test that global answer_generator instance is available."""
    assert answer_generator is not None
    assert isinstance(answer_generator, AnswerGenerator)

def test_generate_answer_with_error():
    """Test answer generation when pipeline raises an error."""
    generator = AnswerGenerator()
    
    # Mock pipeline that raises an error
    mock_pipeline = Mock()
    mock_pipeline.side_effect = Exception("Model error")
    generator.pipeline = mock_pipeline
    
    query = "What is AI?"
    context = "AI is artificial intelligence."
    
    answer = generator.generate_answer(query, context)
    
    assert "error while generating" in answer.lower()
    assert "Model error" in answer

def test_answer_post_processing_edge_cases():
    """Test edge cases in answer post-processing."""
    generator = AnswerGenerator()
    
    # Test empty answer
    processed = generator._post_process_answer("")
    assert processed == ""
    
    # Test answer already ending with punctuation
    answer = "This is correct."
    processed = generator._post_process_answer(answer)
    assert processed == "This is correct."
    
    # Test answer with multiple Answer: prefixes
    answer = "Answer: The Answer: is this"
    processed = generator._post_process_answer(answer)
    assert processed == "is this."

def test_prompt_creation_with_long_context():
    """Test prompt creation with context longer than max length."""
    generator = AnswerGenerator()
    
    query = "What is this?"
    # Create context longer than max_context_length (1000)
    long_context = "This is a very long context. " * 50
    
    prompt = generator._create_prompt(query, long_context)
    
    # Check that context was truncated
    assert "..." in prompt
    # Ensure query is still there
    assert "What is this?" in prompt

def test_generate_answer_parameters():
    """Test that generate_answer passes correct parameters to pipeline."""
    generator = AnswerGenerator()
    
    mock_pipeline = Mock()
    mock_pipeline.return_value = [{"generated_text": "Test answer"}]
    generator.pipeline = mock_pipeline
    
    query = "Test question?"
    context = "Test context"
    max_length = 128
    
    answer = generator.generate_answer(query, context, max_length=max_length)
    
    # Verify pipeline was called with correct parameters
    call_args = mock_pipeline.call_args
    assert call_args[1]['max_length'] == max_length
    assert call_args[1]['min_length'] == 20
    assert call_args[1]['do_sample'] is False
    assert call_args[1]['temperature'] == 0.7
    assert call_args[1]['num_return_sequences'] == 1