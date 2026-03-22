import requests
from deepeval import assert_test
from deepeval.metrics import GEval, SummarizationMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams


class TestAISummarize:
    """DeepEval tests for the /ai/summarize Workers AI endpoint."""

    def test_summarize_preserves_key_points(self, ai_summarize_url, eval_model):
        """Test that summaries preserve the key points of the input text."""
        input_text = (
            "Cloudflare Workers is a serverless platform that allows developers to run code "
            "at the edge of Cloudflare's global network. Workers can handle HTTP requests, "
            "modify responses, and integrate with other Cloudflare services like KV storage, "
            "Durable Objects, and R2 object storage. Workers Containers extends this by allowing "
            "developers to run Docker containers alongside their Workers, enabling more complex "
            "workloads that require full server environments."
        )
        response = requests.post(
            ai_summarize_url,
            json={"text": input_text},
            timeout=30,
        )
        assert response.status_code == 200
        data = response.json()
        actual_output = data["summary"]

        test_case = LLMTestCase(
            input=input_text,
            actual_output=actual_output,
        )
        metric = SummarizationMetric(threshold=0.5, model=eval_model)
        assert_test(test_case, [metric])

    def test_summarize_is_shorter_than_input(self, ai_summarize_url, eval_model):
        """Test that the summary is shorter than the original text."""
        input_text = (
            "Machine learning is a subset of artificial intelligence that focuses on building "
            "systems that learn from data. Unlike traditional programming where rules are explicitly "
            "coded, machine learning algorithms identify patterns in data and make decisions with "
            "minimal human intervention. There are three main types: supervised learning, where the "
            "model is trained on labeled data; unsupervised learning, where the model finds hidden "
            "patterns in unlabeled data; and reinforcement learning, where the model learns through "
            "trial and error by receiving rewards or penalties."
        )
        response = requests.post(
            ai_summarize_url,
            json={"text": input_text},
            timeout=30,
        )
        assert response.status_code == 200
        data = response.json()
        actual_output = data["summary"]

        assert len(actual_output) < len(input_text), (
            f"Summary ({len(actual_output)} chars) should be shorter than input ({len(input_text)} chars)"
        )

        test_case = LLMTestCase(
            input=input_text,
            actual_output=actual_output,
        )
        coherence_metric = GEval(
            name="Coherence",
            model=eval_model,
            criteria="Determine whether the summary is coherent and reads naturally as a standalone text.",
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ],
            threshold=0.5,
        )
        assert_test(test_case, [coherence_metric])

    def test_summarize_factual_consistency(self, ai_summarize_url, eval_model):
        """Test that the summary does not hallucinate or introduce facts not in the original text."""
        input_text = (
            "Python 3.12 was released on October 2, 2023. Key features include improved error "
            "messages with more helpful suggestions, performance improvements through specialization "
            "of the adaptive interpreter, support for the Linux perf profiler, and the new type "
            "parameter syntax using PEP 695."
        )
        response = requests.post(
            ai_summarize_url,
            json={"text": input_text},
            timeout=30,
        )
        assert response.status_code == 200
        data = response.json()
        actual_output = data["summary"]

        test_case = LLMTestCase(
            input=input_text,
            actual_output=actual_output,
        )
        factual_metric = GEval(
            name="Factual Consistency",
            model=eval_model,
            criteria="Determine whether the summary only contains facts present in the original input text and does not introduce new information.",
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ],
            threshold=0.5,
        )
        assert_test(test_case, [factual_metric])
