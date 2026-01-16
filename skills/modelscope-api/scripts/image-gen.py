#!/usr/bin/env python3
"""
ModelScope Image Generation Script

This script handles image generation through ModelScope API with async task polling.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any, Union, Tuple

import requests
from PIL import Image
from io import BytesIO
import yaml
import re


class ModelScopeImageGenerator:
    """ModelScope API image generation client."""

    BASE_URL = "https://api-inference.modelscope.cn/"

    def __init__(self, config_path: Optional[str] = None):
        """Initialize with configuration from local file."""
        # Try multiple config locations in order
        config_candidates = []
        if config_path:
            config_candidates.append(config_path)
        # Global config location
        config_candidates.append(os.path.expanduser("~/.claude/modelscope-image-gen.local.md"))
        # Local project config
        config_candidates.append(".claude/modelscope-image-gen.local.md")

        for candidate in config_candidates:
            try:
                self.api_key, self.config = self._load_config(candidate)
                # Initialize headers after successfully loading config
                self.headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
                return
            except (FileNotFoundError, ValueError):
                continue

        raise FileNotFoundError(
            f"Configuration file not found in any of these locations:\n"
            f"  - {config_path}\n"
            f"  - {os.path.expanduser('~/.claude/modelscope-image-gen.local.md')}\n"
            f"  - .claude/modelscope-image-gen.local.md\n"
            "Please run /modelscope-config to set up your API token."
        )

    def _load_config(self, config_path: str) -> Tuple[str, Dict[str, Any]]:
        """Load API key and configuration from local file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract YAML frontmatter
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                config = yaml.safe_load(match.group(1))
                api_key = config.get('api_key')
                if not api_key:
                    raise ValueError("api_key not found in configuration")
                return api_key, config

            raise ValueError("Invalid configuration file format")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}\n"
                "Please run /modelscope-config to set up your API token."
            )

    def _get_default(self, key: str, default: Any = None) -> Any:
        """Get configuration value with default fallback."""
        return self.config.get(key, default)

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        loras: Optional[Union[str, Dict[str, float]]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        timeout: Optional[int] = None
    ) -> Tuple[bytes, str]:
        """
        Generate an image with the given prompt.

        Returns:
            tuple: (image_data, task_id)
        """
        # Apply defaults from config
        model = model or self._get_default("default_model", "Tongyi-MAI/Z-Image-Turbo")
        timeout = timeout or self._get_default("poll_timeout", 300)
        width = width or self._get_default("default_width", 1024)
        height = height or self._get_default("default_height", 1024)

        # Build request payload
        payload = {
            "model": model,
            "prompt": prompt,
        }

        # Add LoRA configuration if provided
        if loras:
            payload["loras"] = loras

        # Submit generation request
        print(f"Submitting image generation request: {prompt[:50]}...")
        response = requests.post(
            f"{self.BASE_URL}v1/images/generations",
            headers={**self.headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8')
        )
        response.raise_for_status()

        task_id = response.json().get("task_id")
        if not task_id:
            raise ValueError("No task_id in response")

        print(f"Task submitted: {task_id}")

        # Poll for completion
        return self._poll_task(task_id, timeout)

    def _poll_task(self, task_id: str, timeout: int) -> Tuple[bytes, str]:
        """Poll task status until completion or timeout."""
        start_time = time.time()

        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(f"Task {task_id} timed out after {timeout} seconds")

            result = requests.get(
                f"{self.BASE_URL}v1/tasks/{task_id}",
                headers={**self.headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            result.raise_for_status()
            data = result.json()

            # API returns task_status, normalize to lowercase
            status = data.get("task_status") or data.get("status")
            if not status:
                print(f"Debug response: {json.dumps(data, indent=2, ensure_ascii=False)}")
                raise ValueError(f"No status field in response: {data}")
            status = status.lower()
            print(f"Task status: {status} (elapsed: {int(elapsed)}s)")

            if status in ["succeeded", "succeed"]:
                # API returns image URLs in output_images array
                output_images = data.get("output_images", [])
                if not output_images:
                    raise ValueError("No image URL in successful response")
                image_url = output_images[0]

                # Download image
                print(f"Downloading image from: {image_url}")
                image_response = requests.get(image_url)
                image_response.raise_for_status()

                return image_response.content, task_id

            elif status == "failed":
                error = data.get("error", "Unknown error")
                raise Exception(f"Generation failed: {error}")

            elif status in ["pending", "running", "processing"]:
                time.sleep(3)
            else:
                raise Exception(f"Unknown status: {status}")

    def save_image(self, image_data: bytes, output_path: str) -> str:
        """Save image data to file."""
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        img = Image.open(BytesIO(image_data))

        # Generate filename if not provided
        if output_dir.suffix:
            filepath = output_dir
        else:
            timestamp = int(time.time())
            filepath = output_dir / f"image_{timestamp}.png"

        img.save(str(filepath))
        print(f"Image saved to: {filepath}")
        return str(filepath)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate images using ModelScope API"
    )
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--model", help="Model ID (default: from config or Tongyi-MAI/Z-Image-Turbo)")
    parser.add_argument("--loras", help="LoRA configuration (single repo ID or JSON)")
    parser.add_argument("--output", default="./generated-images/", help="Output directory")
    parser.add_argument("--filename", help="Output filename (without extension)")
    parser.add_argument("--width", type=int, help="Image width")
    parser.add_argument("--height", type=int, help="Image height")
    parser.add_argument("--count", type=int, default=1, help="Number of images to generate")
    parser.add_argument("--timeout", type=int, help="Polling timeout in seconds")
    parser.add_argument("--batch", help="Batch prompts file (one per line)")

    args = parser.parse_args()

    try:
        generator = ModelScopeImageGenerator()

        if args.batch:
            # Batch generation
            with open(args.batch, 'r', encoding='utf-8') as f:
                prompts = [line.strip() for line in f if line.strip()]

            for i, prompt in enumerate(prompts, 1):
                print(f"\n=== Generating image {i}/{len(prompts)} ===")
                image_data, task_id = generator.generate(
                    prompt=prompt,
                    model=args.model,
                    loras=args.loras,
                    width=args.width,
                    height=args.height,
                    timeout=args.timeout
                )

                output_path = args.output
                if args.count > 1:
                    output_path = f"{args.output}/image_{i:03d}.png"
                elif args.filename:
                    output_path = f"{args.output}/{args.filename}.png"

                generator.save_image(image_data, output_path)

        else:
            # Single or multiple generation
            for i in range(args.count):
                if args.count > 1:
                    print(f"\n=== Generating image {i + 1}/{args.count} ===")

                image_data, task_id = generator.generate(
                    prompt=args.prompt,
                    model=args.model,
                    loras=args.loras,
                    width=args.width,
                    height=args.height,
                    timeout=args.timeout
                )

                output_path = args.output
                if args.count > 1:
                    output_path = f"{args.output}/image_{i + 1:03d}.png"
                elif args.filename:
                    output_path = f"{args.output}/{args.filename}.png"

                generator.save_image(image_data, output_path)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
