import os
import sys
import shutil
import zipfile
import tarfile


def normalize(filename):
    translit_map = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "h",
        "ґ": "g",
        "д": "d",
        "е": "e",
        "є": "ie",
        "ж": "zh",
        "з": "z",
        "и": "y",
        "і": "i",
        "ї": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ю": "iu",
        "я": "ia",
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "H",
        "Ґ": "G",
        "Д": "D",
        "Е": "E",
        "Є": "Ye",
        "Ж": "Zh",
        "З": "Z",
        "И": "Y",
        "І": "I",
        "Ї": "Yi",
        "Й": "Y",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "Kh",
        "Ц": "Ts",
        "Ч": "Ch",
        "Ш": "Sh",
        "Щ": "Shch",
        "Ю": "Yu",
        "Я": "Ya",
    }

    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    normalized = ""
    for char in filename:
        if char.isalpha() and char in translit_map:
            normalized += translit_map[char]
        elif char in valid_chars:
            normalized += char
        else:
            normalized += "_"
    return normalized


def extract_archive(archive_path, destination_folder):
    try:
        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(destination_folder)
        elif tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, "r") as tar_ref:
                tar_ref.extractall(destination_folder)
        else:
            print(f"Unsupported archive format: {archive_path}")
    except Exception as e:
        print(f"Error extracting archive {archive_path}: {str(e)}")


def process_folder(folder_path):
    image_extensions = ("JPEG", "PNG", "JPG", "SVG")
    video_extensions = ("AVI", "MP4", "MOV", "MKV")
    document_extensions = ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX")
    audio_extensions = ("MP3", "OGG", "WAV", "AMR")
    archive_extensions = ("ZIP", "GZ", "TAR")

    known_extensions = set()
    unknown_extensions = set()

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            extension = os.path.splitext(filename)[1][1:].upper()  # Розширення файлу
            known_extensions.add(extension)

            source_file_path = os.path.join(root, filename)
            normalized_filename = normalize(filename)
            destination_folder = None

            # Категорія файлу за розширенням
            if extension in image_extensions:
                destination_folder = "images"
            elif extension in video_extensions:
                destination_folder = "videos"
            elif extension in document_extensions:
                destination_folder = "documents"
            elif extension in audio_extensions:
                destination_folder = "audio"
            elif extension in archive_extensions:
                destination_folder = "archives"
                archive_name = os.path.splitext(normalized_filename)[
                    0
                ]  # Розширення з імені архіву
                destination_folder = os.path.join(
                    destination_folder, archive_name
                )  # Підпапка з іменем архіву
                os.makedirs(os.path.join(root, destination_folder), exist_ok=True)
                extract_archive(
                    source_file_path, os.path.join(root, destination_folder)
                )
            else:
                unknown_extensions.add(extension)
                continue

            destination_folder_path = os.path.join(root, destination_folder)
            os.makedirs(destination_folder_path, exist_ok=True)

            new_filename = f"{normalized_filename}.{extension}"
            destination_file_path = os.path.join(destination_folder_path, new_filename)
            shutil.move(source_file_path, destination_file_path)

        # Видалення порожніх папок
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    return known_extensions, unknown_extensions


def main():
    if len(sys.argv) < 2:
        print("Usage: python clean.py <folder_path>")
        return

    folder_path = sys.argv[1]
    known_extensions, unknown_extensions = process_folder(folder_path)

    print("Known Extensions:")
    print(known_extensions)

    print("Unknown Extensions:")
    print(unknown_extensions)


if __name__ == "__main__":
    main()
