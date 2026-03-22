import requests
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams


class TestAIChat:
    """DeepEval tests for the /ai/chat Workers AI endpoint."""

    def test_chat_relevancy(self, ai_chat_url, eval_model):
        """Test that chat responses are relevant to the user's question."""
        user_message = "What is the capital of France?"
        response = requests.post(
            ai_chat_url,
            json={"message": user_message},
            timeout=30,
        )
        assert response.status_code == 200
        data = response.json()
        actual_output = data["response"]

        test_case = LLMTestCase(
            input=user_message,
            actual_output=actual_output,
            expected_output="Paris is the capital of France.",
        )
        metric = AnswerRelevancyMetric(threshold=0.5, model=eval_model)
        assert_test(test_case, [metric])

    def test_chat_correctness(self, ai_chat_url, eval_model):
        """Test that chat responses are factually correct."""
        user_message = "What programming language was created by Guido van Rossum?"
        response = requests.post(
            ai_chat_url,
            json={"message": user_message},
            timeout=30,
        )
        assert response.status_code == 200
        data = response.json()
        actual_output = data["response"]

        test_case = LLMTestCase(
            input=user_message,
            actual_output=actual_output,
            expected_output="Python was created by Guido van Rossum.",
        )
        correctness_metric = GEval(
            name="Correctness",
            model=eval_model,
            criteria="Determine whether the actual output is factually correct and matches the expected output.",
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT,
            ],
            threshold=0.5,
        )
        assert_test(test_case, [correctness_metric])

    def test_chat_conciseness(self, ai_chat_url, eval_model):
        """Test that chat responses are concise as instructed by the system prompt."""
        user_message = "What is 2 + 2?"
        response = requests.post(
            ai_chat_url,
            json={"message": user_message},
            timeout=30,
        )
        assert response.status_code == 200
        data = response.json()
        actual_output = data["response"]

        test_case = LLMTestCase(
            input=user_message,
            actual_output=actual_output,
        )
        conciseness_metric = GEval(
            name="Conciseness",
            model=eval_model,
            criteria="Determine whether the response is concise and to the point without unnecessary verbosity.",
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ],
            threshold=0.5,
        )
        assert_test(test_case, [conciseness_metric])
