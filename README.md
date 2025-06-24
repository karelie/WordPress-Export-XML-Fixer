
# WordPressエクスポートXML修正ツール (WordPress Export XML Fixer)

WordPressからエクスポートしたWXR (WordPress eXtended RSS) ファイルに含まれる、破損したシリアライズデータを修正するためのPythonスクリプトです。

## 概要

WordPressサイトからコンテンツをエクスポートすると、一部のプラグイン（例: `MW WP Form`）は、その設定情報をPHPのシリアライズデータとしてXMLファイル内に保存します。このデータに日本語や絵文字などのマルチバイト文字が含まれていると、シリアライズ文字列内のバイト長の記述が不正確になることがあります。

この不整合が原因で、WordPressのインポーターが「メディアのインポートに失敗しました」というエラーや、その他のパースエラーを発生させ、データの取り込みに失敗する場合があります。

このスクリプトは、WordPressのエクスポートXMLファイルをスキャンし、`<wp:postmeta>`タグ内に含まれるシリアライズデータの文字列をすべて検索し、それぞれの文字列の正しいバイト長を再計算して、修正済みの新しいXMLファイルとして保存します。

## 主な機能

- **バイト長の自動修正**: PHPのシリアライズ文字列 (`s:長さ:"文字列";`) を検索し、「長さ」の部分を実際のUTF-8でのバイト数に修正します。
- **安全な処理**: 元のファイルは一切変更せず、修正済みの新しいファイル（例: `your-file_fixed.xml`）を生成します。
- **簡単な使い方**: シンプルなコマンドラインインターフェースを採用。入力ファイルを指定するだけで、残りの処理はスクリプトが自動で行います。
- **名前空間への対応**: WordPress固有のXML名前空間（`wp`, `content`, `excerpt`など）を正しく解釈して処理します。

## 必要なもの

- Python 3.x

## 導入方法

インストールは不要です。`fix_wordpress_xml.py` スクリプトをダウンロードするだけで準備完了です。

1.  このリポジトリをクローンするか、`fix_wordpress_xml.py` ファイルを直接ダウンロードします。
    ```bash
    git clone https://github.com/your-username/wordpress-xml-fixer.git
    cd wordpress-xml-fixer
    ```
2.  修正したいWordPressのエクスポートXMLファイル（例: `my_export.xml`）を、スクリプトと同じディレクトリに置くか、ファイルのフルパスがわかる場所に配置します。

## 使い方

ターミナル（コマンドプロンプト）からスクリプトを実行し、引数として修正したいXMLファイル名を渡します。

### 基本的な使い方

以下のコマンドを実行すると、元のファイル名に `_fixed` が付与された新しいファイル（例: `my_export_fixed.xml`）が生成されます。

```bash
python3 fix_wordpress_xml.py my_export.xml
```

**実行例:**
```
============================================================
WordPressエクスポートXML シリアライズデータ修復ツール
============================================================
入力ファイル 'my_export.xml' を読み込んでいます...
シリアライズデータのチェックと修正を開始します...
  - キー 'mw-wp-form' のデータにバイト長の不一致を発見し、修正しました。
  - キー 'mw-wp-form' のデータにバイト長の不一致を発見し、修正しました。

合計 2 箇所のシリアライズデータを修正しました。
処理が完了しました。修正済みのファイルを 'my_export_fixed.xml' として保存しました。
```

### 出力ファイル名を指定する場合

出力ファイル名を自分で指定したい場合は、2番目の引数として渡します。

```bash
python3 fix_wordpress_xml.py my_export.xml repaired_export.xml
```

### 仕組み

このスクリプトは、XMLファイル内の`<wp:meta_value>`要素に含まれるPHPシリアライズデータを対象とします。正規表現を用いて `s:長さ:"文字列";` のパターンをすべて検索し、見つかった文字列部分をUTF-8でエンコードした場合の実際のバイト長を計算します。そして、`長さ` の部分を正しい値に置換します。

例えば、以下のような破損したデータがあったとします。
```xml
<wp:meta_value><![CDATA[a:1:{s:12:"mail_subject";s:58:"株式会社の件";}]]></wp:meta_value>
```
文字列 `株式会社の件` は6文字ですが、UTF-8でのバイト長は18バイトです。このスクリプトは、不正な値 `s:58` を `s:18` に修正します。
```xml
<wp:meta_value><![CDATA[a:1:{s:12:"mail_subject";s:18:"株式会社の件";}]]></wp:meta_value>
```

## トラブルシューティング

- **`SyntaxError: invalid syntax`**: スクリプトの実行コマンドをPythonファイル内に記述していないか確認してください。コマンドはターミナルで `python3 ...` のように実行します。
- **`FileNotFoundError`**: XMLファイル名が正しいか、スクリプトと同じディレクトリにファイルが存在するか確認してください。または、ファイルのフルパスを正しく指定してください。
- **XMLパースエラー**: スクリプトがXMLのパースエラーで失敗する場合、エクスポートファイル自体がこのスクリプトでは修正できない形で破損している可能性があります。まず、ファイルが有効なXML形式であるか確認してください。

## ライセンス

このプロジェクトは [MIT License](LICENSE) のもとで公開されています。

## 免責事項

このスクリプトは現状有姿で提供され、いかなる保証もありません。スクリプトを実行する前に、必ず元のXMLファイルのバックアップを取ってください。本スクリプトの使用によって生じたいかなるデータの損失や破損についても、作者は責任を負いません。


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
