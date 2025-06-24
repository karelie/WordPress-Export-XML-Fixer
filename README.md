
# WordPress Export XML Fixer

A Python script to fix broken serialized data in WordPress eXtended RSS (WXR) export files.

## Overview

When you export content from a WordPress site, some plugins (like `MW WP Form`) store their settings as PHP serialized data within the XML file. If this data contains multi-byte characters (such as Japanese, Chinese, or emojis), the byte-length count in the serialized string can be incorrect. This causes the WordPress Importer to fail with an error like "Failed to import media" or other parsing errors, because it cannot correctly unserialize the data.

This script scans a WordPress export XML file, finds all serialized data strings within `<wp:postmeta>` tags, recalculates the correct byte length for each string, and saves a new, corrected XML file.

## Features

- **Automatic Byte-Length Correction**: Scans for PHP serialized strings (`s:size:"string";`) and corrects the `size` to match the actual UTF-8 byte length of the `string`.
- **Safe and Non-Destructive**: Creates a new corrected file (e.g., `your-file_fixed.xml`) and leaves the original file untouched.
- **Easy to Use**: Simple command-line interface. Just provide the input file, and it does the rest.
- **Namespace Aware**: Correctly parses the XML file by handling WordPress-specific namespaces (`wp`, `content`, `excerpt`, etc.).

## Requirements

- Python 3.x

## Installation

No installation is needed. Just download the `fix_wordpress_xml.py` script.

1.  Clone this repository or download the `fix_wordpress_xml.py` file.
    ```bash
    git clone https://github.com/your-username/wordpress-xml-fixer.git
    cd wordpress-xml-fixer
    ```
2.  Place your WordPress export XML file (e.g., `my_export.xml`) in the same directory as the script, or provide the full path to the file.

## Usage

Run the script from your terminal, providing the name of the XML file you want to fix as an argument.

### Basic Usage

This will create a new file with `_fixed` appended to the original filename (e.g., `my_export_fixed.xml`).

```bash
python3 fix_wordpress_xml.py my_export.xml
```

**Example Output:**

```
============================================================
WordPress Export XML Serialized Data Repair Tool
============================================================
Reading input file 'my_export.xml'...
Starting check and fix for serialized data...
  - Found and fixed a byte length mismatch in data for key 'mw-wp-form'.
  - Found and fixed a byte length mismatch in data for key 'mw-wp-form'.

Total of 2 serialized data entries have been fixed.
Processing complete. The corrected file has been saved as 'my_export_fixed.xml'.
```

### Specifying an Output File

You can also specify a custom name for the output file as a second argument.

```bash
python3 fix_wordpress_xml.py my_export.xml repaired_export.xml
```

### How It Works

The script specifically targets `<wp:meta_value>` elements that contain serialized PHP data. It uses a regular expression to find all occurrences of `s:size:"string";`. For each match, it calculates the actual byte length of the string content when encoded in UTF-8 and replaces `size` with the correct value.

For example, a broken entry like:
```xml
<wp:meta_value><![CDATA[a:1:{s:12:"mail_subject";s:58:"株式会社の件";}]]></wp:meta_value>
```
The string `株式会社の件` is 6 characters, but its UTF-8 byte length is 18 bytes. The script will correct `s:58` (or whatever incorrect value is there) to `s:18`, resulting in:
```xml
<wp:meta_value><![CDATA[a:1:{s:12:"mail_subject";s:18:"株式会社の件";}]]></wp:meta_value>
```

## Troubleshooting

- **`SyntaxError: invalid syntax`**: Make sure you are running the script with a `python3` command and not trying to execute the command inside the Python script file itself.
- **`FileNotFoundError`**: Ensure that the XML file name is spelled correctly and that it is in the same directory as the script, or provide the full path to the file.
- **XML Parsing Errors**: If the script fails with an XML parsing error, your export file might be corrupted in a way that this script cannot handle. Ensure the file is a valid XML file to begin with.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This script is provided "as is" without warranty of any kind. Always back up your original XML file before running the script. The author is not responsible for any data loss or corruption.
