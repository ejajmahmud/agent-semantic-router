"""Tests for agent-semantic-router."""
import unittest
from agent_semantic_router.router import SemanticRouter


class TestSemanticRouter(unittest.TestCase):
    def setUp(self):
        self.router = SemanticRouter(confidence_threshold=0.2)
        self.router.add_route("coding", ["write python script", "debug rust memory", "build dockerfile"])
        self.router.add_route("database", ["select sql query", "postgres table schema", "join databases"])

    def test_routing_accuracy(self):
        route, score = self.router.route("write a python script to parse csv")
        self.assertEqual(route, "coding")
        self.assertGreater(score, 0.2)

    def test_fallback_to_default(self):
        route, score = self.router.route("what is the weather today?", default_route="fallback")
        self.assertEqual(route, "fallback")


if __name__ == "__main__":
    unittest.main()
