import asyncio
import aiofiles
from pathlib import Path
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def read_folder(source: Path, output: Path):
    """
    Асинхронно читає всі файли у вихідній папці та її підпапках.
    """
    tasks = []
    for item in source.rglob('*'):
        if item.is_file():
            tasks.append(copy_file(item, output))
    
    await asyncio.gather(*tasks)

async def copy_file(file_path: Path, output: Path):
    """
    Копіює файл у відповідну підпапку на основі розширення файлу.
    """
    try:
        extension = file_path.suffix.lstrip('.').lower() or "no_extension"
        destination_folder = output / extension
        destination_folder.mkdir(parents=True, exist_ok=True)
        
        destination_path = destination_folder / file_path.name
        
        async with aiofiles.open(file_path, 'rb') as src_file:
            async with aiofiles.open(destination_path, 'wb') as dst_file:
                await dst_file.write(await src_file.read())
        
        logging.info(f"Копійовано: {file_path} -> {destination_path}")
    except Exception as e:
        logging.error(f"Помилка копіювання {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Сортування файлів на основі розширення")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("output", type=str, help="Шлях до цільової папки")

    args = parser.parse_args()

    source_path = Path(args.source)
    output_path = Path(args.output)

    if not source_path.is_dir():
        logging.error("Вказаний шлях до вихідної папки не існує або не є папкою")
        return
    
    output_path.mkdir(parents=True, exist_ok=True)

    asyncio.run(read_folder(source_path, output_path))

if __name__ == "__main__":
    main()