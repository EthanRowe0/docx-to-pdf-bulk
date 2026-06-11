"""
docx-to-pdf-bulk: Batch convert DOC/DOCX files to PDF from a source folder.
"""

import argparse
import sys
import time
from pathlib import Path

try:
    from docx2pdf import convert
except ImportError:
    print("[ERROR] docx2pdf is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


SUPPORTED_EXTENSIONS = {".doc", ".docx"}

BANNER = r"""
  ____  ___   ______  __  __  _____  ____  ____  ____
 / __ \/ _ \ / ___/ |/ / / /_/ __  \/ __ \/ __ \/ __/
/ /_/ / // // /__ >   < / __/ /_/ // /_/ / /_/ / _/
\____/\___/ \___//_/|_|/_/  \____/ \____/\____/_/
       Bulk DOC / DOCX  ->  PDF  Converter
"""


def print_banner():
    print(BANNER)


def find_documents(source: Path) -> list[Path]:
    """Recursively find all DOC/DOCX files in source folder."""
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(source.rglob(f"*{ext}"))
    return sorted(files)


def resolve_output_path(source_file: Path, source_root: Path, output_root: Path) -> Path:
    """Mirror the source folder structure in the output folder."""
    relative = source_file.relative_to(source_root)
    dest = output_root / relative.with_suffix(".pdf")
    dest.parent.mkdir(parents=True, exist_ok=True)
    return dest


def convert_files(
    files: list[Path],
    source_root: Path,
    output_root: Path,
    verbose: bool = False,
) -> tuple[int, int, list[tuple[Path, str]]]:
    """
    Convert a list of DOC/DOCX files to PDF.
    Returns (success_count, skip_count, failures).
    """
    success = 0
    skipped = 0
    failures: list[tuple[Path, str]] = []

    iterator = tqdm(files, unit="file", desc="Converting") if tqdm else files

    for src in iterator:
        dest = resolve_output_path(src, source_root, output_root)

        if dest.exists():
            skipped += 1
            if verbose:
                print(f"  [SKIP]  {src.name}  →  already exists")
            continue

        try:
            convert(str(src), str(dest))
            success += 1
            if verbose and not tqdm:
                print(f"  [OK]    {src.name}")
        except Exception as exc:
            failures.append((src, str(exc)))
            if verbose:
                msg = f"  [FAIL]  {src.name}: {exc}"
                if tqdm:
                    tqdm.write(msg)
                else:
                    print(msg)

    return success, skipped, failures


def print_summary(
    total: int,
    success: int,
    skipped: int,
    failures: list[tuple[Path, str]],
    elapsed: float,
    output_root: Path,
):
    width = 60
    print("\n" + "-" * width)
    print("  RESULTS")
    print("-" * width)
    print(f"  Total found   : {total}")
    print(f"  Converted     : {success}")
    print(f"  Skipped       : {skipped}  (PDF already exists)")
    print(f"  Failed        : {len(failures)}")
    print(f"  Time elapsed  : {elapsed:.1f}s")
    print(f"  Output folder : {output_root}")
    print("-" * width)

    if failures:
        print("\n  FAILURES:")
        for path, reason in failures:
            print(f"    • {path.name}")
            print(f"      {reason}")
        print()


def main():
    parser = argparse.ArgumentParser(
        prog="converter",
        description="Batch convert DOC/DOCX files to PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python converter.py ./documents
  python converter.py ./documents --output ./pdfs
  python converter.py ./documents --output ./pdfs --verbose
  python converter.py ./documents --overwrite
        """,
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Source folder containing DOC/DOCX files (searched recursively).",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output folder for PDFs. Defaults to a 'pdf_output' subfolder inside source.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-convert even if a PDF already exists.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print each file as it is processed.",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Suppress the ASCII banner.",
    )

    args = parser.parse_args()

    if not args.no_banner:
        print_banner()

    source: Path = args.source.resolve()
    if not source.exists():
        print(f"[ERROR] Source folder does not exist: {source}")
        sys.exit(1)
    if not source.is_dir():
        print(f"[ERROR] Source path is not a folder: {source}")
        sys.exit(1)

    output_root: Path = (args.output or source / "pdf_output").resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    print(f"  Source : {source}")
    print(f"  Output : {output_root}")
    print()

    files = find_documents(source)

    # Never convert files that live inside the output folder to avoid loops
    files = [f for f in files if not str(f).startswith(str(output_root))]

    if not files:
        print("  No DOC or DOCX files found in the source folder.")
        sys.exit(0)

    print(f"  Found {len(files)} file(s) to process.\n")

    if args.overwrite:
        # Treat everything as new — delete existing PDFs that mirror source files
        for src in files:
            dest = resolve_output_path(src, source, output_root)
            if dest.exists():
                dest.unlink()

    start = time.perf_counter()
    success, skipped, failures = convert_files(
        files, source, output_root, verbose=args.verbose
    )
    elapsed = time.perf_counter() - start

    print_summary(len(files), success, skipped, failures, elapsed, output_root)

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
