import re
import xml.etree.ElementTree as ET
import os
import sys # コマンドライン引数を扱うためにインポート

def fix_serialized_string_length(match):
    """
    正規表現にマッチした部分の文字列のバイト長を修正するコールバック関数。
    """
    string_content = match.group(2)
    # 文字列をUTF-8でエンコードして実際のバイト数を計算
    actual_length = len(string_content.encode('utf-8'))
    # 宣言されている長さ
    declared_length = int(match.group(1))

    # 実際のバイト長と宣言されている長さが異なる場合のみ修正
    if actual_length != declared_length:
        return f's:{actual_length}:"{string_content}"'
    else:
        # 長さが合っていれば変更しない
        return match.group(0)

def fix_serialized_data(data):
    """
    PHPのシリアライズデータ全体を修正する。
    """
    # 正規表現: s:長さ:"文字列" のパターンにマッチ
    regex = re.compile(r's:(\d+):"((?:\\.|[^"])*)"')
    return regex.sub(fix_serialized_string_length, data)

def process_wordpress_xml(input_file, output_file):
    """
    WordPressのXMLファイルを処理し、シリアライズデータを修正する。
    """
    print(f"入力ファイル '{input_file}' を読み込んでいます...")

    if not os.path.exists(input_file):
        print(f"エラー: ファイル '{input_file}' が見つかりません。")
        return False

    try:
        # XMLファイルから名前空間を自動的に取得して登録
        namespaces = {k: v for _, (k, v) in ET.iterparse(input_file, events=['start-ns'])}
        if not namespaces: # 名前空間が見つからない場合のフォールバック
            namespaces = {
                'wp': 'http://wordpress.org/export/1.2/',
                'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
                'content': 'http://purl.org/rss/1.0/modules/content/',
                'wfw': 'http://wellformedweb.org/CommentAPI/',
                'dc': 'http://purl.org/dc/elements/1.1/'
            }
        
        for prefix, uri in namespaces.items():
            if prefix:
                ET.register_namespace(prefix, uri)

        tree = ET.parse(input_file)
        root = tree.getroot()
        
        wp_namespace_uri = namespaces.get('wp', 'http://wordpress.org/export/1.2/')
        
        print("シリアライズデータのチェックと修正を開始します...")
        fix_count = 0
        
        # すべての <wp:postmeta> タグを検索
        for postmeta in root.iter(f'{{{wp_namespace_uri}}}postmeta'):
            meta_value_element = postmeta.find(f'{{{wp_namespace_uri}}}meta_value')
            
            if meta_value_element is not None and meta_value_element.text:
                original_data = meta_value_element.text
                if original_data.strip().startswith(('a:', 's:')):
                    fixed_data = fix_serialized_data(original_data)
                    
                    if original_data != fixed_data:
                        meta_key_element = postmeta.find(f'{{{wp_namespace_uri}}}meta_key')
                        key_name = meta_key_element.text if meta_key_element is not None else "不明なキー"
                        print(f"  - キー '{key_name}' のデータにバイト長の不一致を発見し、修正しました。")
                        meta_value_element.text = fixed_data
                        fix_count += 1

        if fix_count > 0:
            print(f"\n合計 {fix_count} 箇所のシリアライズデータを修正しました。")
        else:
            print("\n修正が必要な箇所は見つかりませんでした。ファイルは正常です。")

        tree.write(output_file, encoding='UTF-8', xml_declaration=True)
        print(f"処理が完了しました。修正済みのファイルを '{output_file}' として保存しました。")
        return True

    except ET.ParseError as e:
        print(f"エラー: XMLファイルのパースに失敗しました: {e}")
        return False
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return False

def main():
    """
    メインの実行関数。コマンドライン引数を処理する。
    """
    print("=" * 60)
    print("WordPressエクスポートXML シリアライズデータ修復ツール")
    print("=" * 60)

    # コマンドライン引数をチェック
    if len(sys.argv) < 2:
        print("使い方: python3 fix_wordpress_xml.py <入力ファイル名.xml> [出力ファイル名.xml]")
        print("例: python3 fix_wordpress_xml.py WordPress.2025-06-23.xml")
        sys.exit(1) # エラーで終了

    # 入力ファイル名を取得
    input_filename = sys.argv[1]

    # 出力ファイル名が指定されているかチェック
    if len(sys.argv) > 2:
        output_filename = sys.argv[2]
    else:
        # 指定されていない場合、入力ファイル名に "_fixed" を付けて自動生成
        base, ext = os.path.splitext(input_filename)
        output_filename = f"{base}_fixed{ext}"

    process_wordpress_xml(input_filename, output_filename)


if __name__ == "__main__":
    main()