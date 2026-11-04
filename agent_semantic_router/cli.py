"""CLI for agent-semantic-router."""
import sys
import argparse
from .router import SemanticRouter


def main():
    parser = argparse.ArgumentParser(description="Agent Semantic Router")
    parser.add_argument("--query", default="calculate factorial of 10", help="Query to route")
    args = parser.parse_args()

    router = SemanticRouter()
    router.add_route("math", ["calculate sum", "multiply numbers", "factorial algebra matrix"])
    router.add_route("code", ["write python function", "debug git conflict", "implement binary search"])

    target, score = router.route(args.query)
    print(f"Query routed to: '{target}' (similarity score: {score:.3f})")
    sys.exit(0)


if __name__ == "__main__":
    main()
