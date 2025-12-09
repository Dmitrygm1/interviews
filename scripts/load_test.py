import argparse
import concurrent.futures
import json
import random
import string
import time
from typing import Tuple

import requests


def random_session_id(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def run_single_interview(
    base_url: str,
    interview_id: str,
    num_turns: int,
    min_delay: float,
    max_delay: float,
) -> Tuple[int, float]:
    """
    Simulate a single interview session:
    - GET /<interview_id>/<session_id> to start
    - Loop: POST /next with dummy user_message

    Returns:
        (total_requests, total_duration_seconds)
    """
    session_id = random_session_id()
    start_time = time.time()
    total_requests = 0

    # Start interview (landing page)
    url_landing = f"{base_url.rstrip('/')}/{interview_id}/{session_id}"
    resp = requests.get(url_landing)
    total_requests += 1
    resp.raise_for_status()

    # Conversation turns
    url_next = f"{base_url.rstrip('/')}/next"
    for turn in range(num_turns):
        payload = {
            "session_id": session_id,
            "interview_id": interview_id,
            "user_message": f"Dummy answer turn {turn}",
        }
        resp = requests.post(url_next, json=payload)
        total_requests += 1
        resp.raise_for_status()

        try:
            _ = resp.json()
        except json.JSONDecodeError:
            raise RuntimeError(f"Non-JSON response for session {session_id}: {resp.text}")

        if turn < num_turns - 1 and max_delay > 0:
            time.sleep(random.uniform(min_delay, max_delay))

    duration = time.time() - start_time
    return total_requests, duration


def main():
    parser = argparse.ArgumentParser(description="Simple load tester for the interview app.")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="Base URL of the running Flask app (default: http://127.0.0.1:8000).",
    )
    parser.add_argument(
        "--interview-id",
        default="STOCK_MARKET",
        help="Interview configuration key to use (default: STOCK_MARKET).",
    )
    parser.add_argument(
        "--users",
        type=int,
        default=20,
        help="Number of concurrent simulated interviewees.",
    )
    parser.add_argument(
        "--turns",
        type=int,
        default=10,
        help="Number of Q&A turns per interviewee (calls to /next).",
    )
    parser.add_argument(
        "--min-delay",
        type=float,
        default=1.0,
        help="Minimum delay (seconds) between user turns for each interviewee.",
    )
    parser.add_argument(
        "--max-delay",
        type=float,
        default=3.0,
        help="Maximum delay (seconds) between user turns for each interviewee.",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=None,
        help="Maximum worker threads (default: same as --users).",
    )

    args = parser.parse_args()
    max_workers = args.max_workers or args.users

    print(
        f"Starting load test: {args.users} users, {args.turns} turns each, "
        f"delays {args.min_delay}-{args.max_delay}s, base_url={args.base_url}"
    )

    global_start = time.time()
    total_requests = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                run_single_interview,
                args.base_url,
                args.interview_id,
                args.turns,
                args.min_delay,
                args.max_delay,
            )
            for _ in range(args.users)
        ]

        for future in concurrent.futures.as_completed(futures):
            reqs, _ = future.result()
            total_requests += reqs

    total_duration = time.time() - global_start
    rps = total_requests / total_duration if total_duration > 0 else 0.0

    print(f"\nLoad test complete.")
    print(f"Total requests: {total_requests}")
    print(f"Total wall-clock time: {total_duration:.2f} s")
    print(f"Average throughput: {rps:.2f} requests/s")


if __name__ == "__main__":
    main()

