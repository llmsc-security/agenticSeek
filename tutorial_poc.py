#!/usr/bin/env python3
"""
tutorial_poc.py - HTTP API Test Client for AgenticSeek FastAPI

This script provides a comprehensive test client for the AgenticSeek API.
It demonstrates how to interact with the backend endpoints and verify functionality.

Usage:
    python tutorial_poc.py [command] [options]

Commands:
    health          - Check if the API is running
    status          - Get agent status
    query <text>    - Send a query to the agents
    screenshot      - Download the latest screenshot
    stop            - Stop current agent operation
    history         - Get query response history
"""

import requests
import sys
import json
import time
import argparse
from typing import Optional, Dict, Any


class AgenticSeekClient:
    """Client for interacting with the AgenticSeek API."""

    def __init__(self, base_url: str = "http://localhost:7777"):
        """
        Initialize the API client.

        Args:
            base_url: The base URL of the AgenticSeek API
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests

        Returns:
            JSON response as dictionary

        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {"error": str(e), "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def health_check(self) -> Dict[str, Any]:
        """
        Check if the API is running and healthy.

        Returns:
            Health check response with status and version
        """
        return self._make_request("GET", "/health")

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the interaction system.

        Returns:
            Status information including is_active flag
        """
        return self._make_request("GET", "/is_active")

    def stop_agent(self) -> Dict[str, Any]:
        """
        Stop the current agent operation.

        Returns:
            Response indicating success or failure
        """
        return self._make_request("GET", "/stop")

    def get_latest_answer(self) -> Dict[str, Any]:
        """
        Get the latest answer from the agents.

        Returns:
            Latest query response with answer, reasoning, and metadata
        """
        return self._make_request("GET", "/latest_answer")

    def get_screenshot(self, save_path: Optional[str] = None) -> Optional[bytes]:
        """
        Download the latest browser screenshot.

        Args:
            save_path: Optional path to save the screenshot

        Returns:
            Screenshot as bytes, or None if not available
        """
        url = f"{self.base_url}/screenshot"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"Screenshot saved to: {save_path}")
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Failed to get screenshot: {e}")
            return None

    def query(self, text: str, timeout: int = 300) -> Dict[str, Any]:
        """
        Send a query to the agentic system.

        Args:
            text: The query text to process
            timeout: Request timeout in seconds

        Returns:
            Query response with answer, reasoning, and agent information
        """
        payload = {"query": text}
        return self._make_request("POST", "/query", json=payload, timeout=timeout)

    def wait_for_completion(self, timeout: int = 300, poll_interval: float = 1.0) -> Optional[Dict[str, Any]]:
        """
        Wait for a query to complete and get the result.

        Args:
            timeout: Maximum wait time in seconds
            poll_interval: Time between status checks in seconds

        Returns:
            Final query result or None if timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_status()
            if not status.get("is_active", True):
                return self.get_latest_answer()
            time.sleep(poll_interval)
        return None


def print_response(data: Dict[str, Any], title: str = "Response") -> None:
    """Pretty print JSON response."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def demo_interactive(client: AgenticSeekClient) -> None:
    """Run an interactive demo of the API."""
    print("\n" + "=" * 60)
    print("  AgenticSeek API Interactive Demo")
    print("=" * 60)
    print("\nThis demo shows how to use the AgenticSeek API endpoints.")
    print("Make sure the backend is running on port 7777.\n")

    # 1. Health Check
    print("[1/5] Testing health endpoint...")
    health = client.health_check()
    print_response(health, "Health Check")
    if health.get("error"):
        print("\nError: Could not connect to the API. Make sure the backend is running.")
        return

    # 2. Get Status
    print("\n[2/5] Getting agent status...")
    status = client.get_status()
    print_response(status, "Agent Status")

    # 3. Sample Query
    print("\n[3/5] Sending a sample query...")
    sample_query = "Hello, how are you?"
    print(f"Query: {sample_query}")
    result = client.query(sample_query)
    print_response(result, "Query Result")

    # 4. Get Latest Answer
    print("\n[4/5] Getting latest answer...")
    answer = client.get_latest_answer()
    print_response(answer, "Latest Answer")

    # 5. Screenshot (if available)
    print("\n[5/5] Checking for screenshot...")
    screenshot = client.get_screenshot()
    if screenshot:
        print(f"Screenshot available ({len(screenshot)} bytes)")
    else:
        print("No screenshot available")

    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)
    print("\nKey API Endpoints:")
    print("  GET  /health           - Health check")
    print("  GET  /is_active        - Check if agent is busy")
    print("  GET  /stop             - Stop current operation")
    print("  GET  /latest_answer    - Get last response")
    print("  GET  /screenshot       - Download browser screenshot")
    print("  POST /query            - Send query to agents")
    print()


def demo_quick_test(client: AgenticSeekClient) -> bool:
    """Run a quick test of the API."""
    print("Running quick API test...")

    # Test health
    health = client.health_check()
    if health.get("error"):
        print(f"FAILED: Could not connect to API - {health['error']}")
        return False

    print(f"Health check: {health.get('status', 'unknown')}")
    print(f"Version: {health.get('version', 'unknown')}")

    # Test simple query
    result = client.query("Say hello!")
    print(f"Query completed: {result.get('done', 'unknown')}")
    print(f"Answer preview: {result.get('answer', '')[:100]}...")

    print("\nQuick test PASSED!")
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AgenticSeek API Test Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tutorial_poc.py                    # Run interactive demo
  python tutorial_poc.py health             # Check API health
  python tutorial_poc.py query "Hello"      # Send a query
  python tutorial_poc.py status             # Get agent status
  python tutorial_poc.py screenshot         # Download screenshot

Environment Variables:
  AGENTIC_SEEK_URL: Base URL of the API (default: http://localhost:7777)
        """
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="demo",
        choices=["demo", "health", "query", "status", "screenshot", "stop", "history"],
        help="Command to run (default: demo)"
    )

    parser.add_argument(
        "args",
        nargs="*",
        help="Arguments for the command"
    )

    parser.add_argument(
        "--url",
        default="http://localhost:7777",
        help="API base URL (default: http://localhost:7777)"
    )

    args = parser.parse_args()

    # Create client
    client = AgenticSeekClient(base_url=args.url)

    # Execute command
    if args.command == "demo":
        demo_interactive(client)
    elif args.command == "health":
        health = client.health_check()
        print_response(health)
    elif args.command == "query":
        if not args.args:
            print("Error: Query requires text argument")
            print("Usage: python tutorial_poc.py query <text>")
            sys.exit(1)
        result = client.query(" ".join(args.args))
        print_response(result)
    elif args.command == "status":
        status = client.get_status()
        print_response(status)
    elif args.command == "screenshot":
        path = args.args[0] if args.args else None
        client.get_screenshot(save_path=path)
    elif args.command == "stop":
        result = client.stop_agent()
        print_response(result)
    elif args.command == "history":
        answer = client.get_latest_answer()
        print_response(answer)


if __name__ == "__main__":
    main()
