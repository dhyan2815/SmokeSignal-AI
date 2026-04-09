import sys
import os
import time
from PIL import Image
from rich.console import Console
from src.utils.tui import StatusLine
from src.services.inference_service import run_inference
from src.core.logger import setup_logger

logger = setup_logger(__name__)
console = Console()

def run_cli_inference(image_path):
    sl = StatusLine(console=console)

    def task(update_fn):
        if not os.path.exists(image_path):
            console.print(f"[bold red]Error:[/bold red] File not found: {image_path}")
            return

        update_fn("Loading Image...")
        try:
            image = Image.open(image_path)
            time.sleep(1) # Simulate some delay
            
            update_fn("Pre-processing...")
            time.sleep(0.5)

            update_fn("Running Model Inference...")
            result = run_inference(image)
            time.sleep(1.5)

            update_fn("Idle")
            
            if "error" in result:
                console.print(f"[bold red]Inference Failed:[/bold red] {result['error']}")
            else:
                label = result['label']
                conf = result['confidence']
                style = "bold red" if label == "Wildfire" else "bold green"
                
                console.print("\n" + "="*40)
                console.print(f" RESULT: [{style}]{label}[/{style}]")
                console.print(f" CONFIDENCE: {conf:.2f}")
                console.print("="*40 + "\n")

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            update_fn("Idle")

    # Run the interactive task with the status line at the bottom
    sl.run_interactive(task)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[yellow]Usage:[/yellow] python src/cli.py <image_path>")
        sys.exit(1)
    
    run_cli_inference(sys.argv[1])
